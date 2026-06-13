# app/agents/scheduler.py

import json
import ollama

from app.models.schedule import (
    DailySchedule,
)

from app.services.prompt_builder import (
    build_scheduler_prompt,
)

MODEL_NAME = "qwen2.5:14b"


def generate_schedule(
    theme,
    editorial_brief,
    slots,
    programs,
    feedback=None,
):
    """
    Generate a full broadcast schedule.
    """

    prompt = build_scheduler_prompt(
        theme=theme,
        editorial_brief=editorial_brief,
        slots=slots,
        programs=programs,
        feedback=feedback,
    )

    raw_response = ollama.chat(
        model=MODEL_NAME,
        format="json",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )["message"]["content"]

    print("\n" + "=" * 80)
    print("SCHEDULER RESPONSE")
    print("=" * 80)
    print(raw_response)
    print("=" * 80)

    data = json.loads(
        raw_response
    )

    return DailySchedule.model_validate(
        data
    )

if __name__ == "__main__":

    from app.database.db import (
        connect_db,
        load_slots,
        load_programs,
    )

    conn = connect_db()
    cur = conn.cursor()

    try:

        slots = load_slots(cur)

        programs = load_programs(cur)

        # Librarian-approved IDs
        curated_keys = [
            78,
            93,
            135,
            146,
            26,
            49,
            100,
            40,
            16,
            28,
            58,
            124,
            17,
            139,
            95,
            105,
        ]

        curated_programs = [
            p
            for p in programs
            if p["program_key"] in curated_keys
        ]

        print("\nCURATED PROGRAMS")

        for p in curated_programs:

            print(
                f"{p['program_key']:>3} | "
                f"{p['title']:<30} | "
                f"{p['genre']}"
            )

        schedule = generate_schedule(
            theme=(
                "Sunday Serenity: "
                "A Day of Uplifting Stories "
                "and Family Bonding"
            ),

            editorial_brief=(
                "Today our network aims to "
                "inspire optimism and strengthen "
                "family connections through "
                "heartwarming narratives."
            ),

            slots=slots,

            programs=curated_programs,
        )

        print("\nSCHEDULE SUMMARY")

        for slot in schedule.slots:

            print(
                f"{slot.time:<12}"
                f"→ Program "
                f"{slot.program_key}"
            )

    finally:

        cur.close()
        conn.close()