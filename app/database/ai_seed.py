import datetime
import json
import os
import random
import re
import time
from pathlib import Path
import ollama
import psycopg2
from dotenv import load_dotenv

# ==========================
# Configuration
# ==========================

MODEL_NAME = "qwen2.5:14b"
MAX_RETRIES = 3

# Define your timeframe here
START_DATE = datetime.date(2025, 1, 1)
END_DATE = datetime.date(2030, 1, 1)  # 5 Years

# ==========================
# Database Connection
# ==========================

def connect_db():
    load_dotenv()
    base_dir = Path(__file__).resolve().parents[2]
    password_path = base_dir / "secrets" / "postgres_password.txt"
    db_password = password_path.read_text().strip()

    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", 5432)),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=db_password,
    )

# ==========================
# Inventory Loading
# ==========================

def load_inventory(cur):
    cur.execute("SELECT slot_key, slot_name, daypart, duration_minutes FROM slot ORDER BY slot_key")
    slots = [{"slot_key": r[0], "slot_name": r[1], "daypart": r[2], "duration": r[3]} for r in cur.fetchall()]

    cur.execute("SELECT program_key, title, program_type, genre FROM program")
    programs = [{"program_key": r[0], "title": r[1], "program_type": r[2], "genre": r[3]} for r in cur.fetchall()]

    cur.execute("SELECT commercial_key, brand_name, target_demographic FROM commercial")
    commercials = [{"commercial_key": r[0], "brand_name": r[1], "target_demographic": r[2]} for r in cur.fetchall()]

    return slots, programs, commercials

# ==========================
# Prompt Construction
# ==========================

def build_slot_prompt(slot, current_date, programs, commercials, previous_slot=None, error=None):
    daypart = slot["daypart"].lower()
    is_weekend = current_date.weekday() in (5, 6)
    day_type = "Weekend" if is_weekend else "Weekday"

    # Guide viewership scale based on standard operational parameters
    if "overnight" in daypart:
        viewers = "100,000 to 500,000"
    elif "morning" in daypart:
        viewers = "300,000 to 1,000,000"
    elif "afternoon" in daypart:
        viewers = "500,000 to 1,500,000"
    elif "prime time" in daypart:
        viewers = "2,000,000 to 4,500,000" if is_weekend else "1,500,000 to 4,000,000"
    else:
        viewers = "300,000 to 1,200,000"

    context_str = "This is the first slot of the day."
    if previous_slot:
        context_str = f"The previous slot was running program ID {previous_slot['program_key']} with {previous_slot['viewer_count']} viewers."

    prompt = f"""You are the Programming Director of a television network.
Generate highly realistic scheduling and viewership metrics for ONE SPECIFIC TIME SLOT.

Current Target:
- Date: {current_date.strftime('%Y-%m-%d')} ({day_type})
- Slot: {slot['slot_name']} ({slot['daypart']})
- Duration: {slot['duration']} minutes

Context:
{context_str}

Available Programs (Pick EXACTLY ONE that matches the vibe/daypart):
{json.dumps(programs, indent=2)}

Available Commercials (Pick EXACTLY 2 or 3 that target a similar demographic as the program):
{json.dumps(commercials, indent=2)}

Requirements for this Daypart:
- Expected Viewer Count: {viewers}
- Retention Rate: 0.50 to 0.95
- Dropoff Rate: 1.0 - Retention Rate
- Ad revenue should scale logically based on the viewer count ($15 to $35 CPM per commercial).

Return JSON ONLY using exactly this format:
{{
    "program_key": 1,
    "commercial_keys": [1, 2],
    "viewer_count": 100000,
    "avg_watch_minutes": 30,
    "retention_rate": 0.70,
    "dropoff_rate": 0.30,
    "ad_revenue": 50000
}}"""

    if error:
        prompt += f"\n\nCRITICAL: Your previous generation failed validation due to: {error}. Fix this error immediately."

    return prompt

# ==========================
# Parsers & Database Savers
# ==========================

def extract_json(raw):
    try:
        return json.loads(raw)
    except Exception:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError("No JSON block found")
        return json.loads(match.group())

def validate_slot_response(parsed, valid_programs, valid_commercials):
    required = ["program_key", "commercial_keys", "viewer_count", "avg_watch_minutes", "retention_rate", "dropoff_rate", "ad_revenue"]
    if not all(field in parsed for field in required):
        return False, "Missing required key metrics."
    if parsed["program_key"] not in valid_programs:
        return False, f"Invalid program_key: {parsed['program_key']}"
    if not (2 <= len(parsed["commercial_keys"]) <= 3):
        return False, "Must contain exactly 2 or 3 commercial keys."
    if any(ck not in valid_commercials for ck in parsed["commercial_keys"]):
        return False, "Contains invalid commercial identifiers."
    return True, None

def save_slot_to_db(cur, slot_key, target_date, data):
    cur.execute("""
        INSERT INTO slot_program (slot_key, broadcast_date, program_key, slot_order)
        VALUES (%s, %s, %s, 1);
    """, (slot_key, target_date, data["program_key"]))

    for idx, comm_key in enumerate(data["commercial_keys"], start=1):
        cur.execute("""
            INSERT INTO slot_commercial (slot_key, broadcast_date, commercial_key, sequence_order)
            VALUES (%s, %s, %s, %s);
        """, (slot_key, target_date, comm_key, idx))

    cur.execute("""
        INSERT INTO slot_viewership (slot_key, broadcast_date, viewer_count, avg_watch_minutes, retention_rate, dropoff_rate, ad_revenue)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (slot_key, target_date, data["viewer_count"], data["avg_watch_minutes"], data["retention_rate"], data["dropoff_rate"], data["ad_revenue"]))

# ==========================
# Main Orchestrator Loop
# ==========================

def main():
    conn = connect_db()
    cur = conn.cursor()

    try:
        slots, programs, commercials = load_inventory(cur)
        valid_programs = {p["program_key"] for p in programs}
        valid_commercials = {c["commercial_key"] for c in commercials}

        current_date = START_DATE
        previous_slot_data = None
        
        print(f"🎬 Starting processing engine... Generating from {START_DATE} to {END_DATE}.")

        while current_date < END_DATE:
            print(f"\n📅 Processing Date: {current_date.strftime('%Y-%m-%d')}")
            
            for slot in slots:
                # Sub-sample random items per slot to prevent exploding context windows on your GPU
                sampled_programs = random.sample(programs, min(12, len(programs)))
                sampled_commercials = random.sample(commercials, min(8, len(commercials)))
                
                slot_data = None
                error_msg = None

                for attempt in range(1, MAX_RETRIES + 1):
                    prompt = build_slot_prompt(slot, current_date, sampled_programs, sampled_commercials, previous_slot_data, error_msg)
                    
                    try:
                        raw_response = ollama.chat(
                            model=MODEL_NAME,
                            format="json",
                            messages=[{"role": "user", "content": prompt}]
                        )["message"]["content"]
                        
                        parsed = extract_json(raw_response)
                        is_valid, error_msg = validate_slot_response(parsed, valid_programs, valid_commercials)
                        
                        if is_valid:
                            slot_data = parsed
                            break
                    except Exception as e:
                        error_msg = str(e)

                if not slot_data:
                    raise RuntimeError(f"Failed generation chain on date {current_date} for slot {slot['slot_key']}")

                save_slot_to_db(cur, slot["slot_key"], current_date, slot_data)
                previous_slot_data = slot_data

            # Batch commit to DB at the end of every month so you don't lose progress if you pause it
            if current_date.day == 28: # Broad checkpoint check
                conn.commit()
                print("💾 Progress safely synchronized and committed to database.")

            current_date += datetime.timedelta(days=1)

        conn.commit()
        print("\n🎉 Generation complete! 5 years of rich AI mock metrics successfully stored.")

    except Exception as err:
        conn.rollback()
        print(f"\n💥 Script halted. Structural changes rolled back safely. Error:\n{err}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()