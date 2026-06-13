import os
import random
from pathlib import Path

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values
from datetime import date

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]

password_path = BASE_DIR / "secrets" / "postgres_password.txt"

db_password = password_path.read_text().strip()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=db_password,
)

cur = conn.cursor()

#slots section

slots = []

for hour in range(24):
    start = f"{hour:02d}:00:00"
    end = f"{(hour + 1) % 24:02d}:00:00"

    if 0 <= hour <= 5:
        daypart = "Overnight"
    elif 6 <= hour <= 11:
        daypart = "Morning"
    elif 12 <= hour <= 17:
        daypart = "Afternoon"
    elif 18 <= hour <= 22:
        daypart = "Prime Time"
    else:
        daypart = "Late Night"

    is_prime = 18 <= hour <= 22

    slots.append(
        (
            start,
            end,
            60,
            f"{hour:02d}:00-{(hour + 1) % 24:02d}:00",
            daypart,
            is_prime,
        )
    )

try:

    execute_values(
        cur,
        """
        INSERT INTO slot (
            start_time,
            end_time,
            duration_minutes,
            slot_name,
            daypart,
            is_prime_time
        )
        VALUES %s
        ON CONFLICT (start_time, end_time)
        DO NOTHING
        """,
        slots,
    )

    conn.commit()

    print(f"✓ Seeded {len(slots)} slots")

except Exception as e:
    conn.rollback()
    print(f"✗ Failed: {e}")
    raise

#program section

programs = []

adjectives = [
    "Crimson",
    "Silent",
    "Hidden",
    "Eternal",
    "Iron",
    "Midnight",
    "Lost",
    "Golden",
    "Fallen",
    "Shattered"
]

nouns = [
    "Legacy",
    "Empire",
    "Chronicles",
    "Protocol",
    "Frontier",
    "Kingdom",
    "Horizon",
    "Echo",
    "Alliance",
    "Destiny"
]

demographics = [
    "Teens",
    "Young Adults",
    "Adults",
    "Families"
]

series_genres = [
    "Drama",
    "Fantasy",
    "Sitcom",
    "Crime",
    "Sci-Fi",
    "Reality",
    "Romance"
]

used_titles = set()

while len([p for p in programs if p[1] == "Series"]) < 50:
    title = f"{random.choice(adjectives)} {random.choice(nouns)}"

    if title in used_titles:
        continue

    used_titles.add(title)

    programs.append(
        (
            title,
            "Series",
            random.choice(series_genres),
            random.randint(22, 60),
            random.choice(["G", "PG", "PG-13"]),
            random.choice(demographics),
        )
    )

movie_genres = [
    "Action",
    "Fantasy",
    "Comedy",
    "Thriller",
    "Drama"
]

while len([p for p in programs if p[1] == "Cinema"]) < 20:
    title = (
        f"{random.choice(adjectives)} "
        f"{random.choice(nouns)}: "
        f"{random.choice(adjectives)}"
    )

    if title in used_titles:
        continue

    used_titles.add(title)

    programs.append(
        (
            title,
            "Cinema",
            random.choice(movie_genres),
            random.randint(90, 180),
            random.choice(["PG", "PG-13", "R"]),
            random.choice(demographics),
        )
    )

specials = [
    "Morning News",
    "Evening News",
    "Basketball Finals",
    "Awards Night",
    "Election Coverage",
    "Year-End Countdown",
    "Championship Match",
    "Breaking News Special",
    "Sunday Public Affairs",
    "New Year's Eve Special",
]

for title in specials:
    programs.append(
        (
            title,
            "Special",
            random.choice(["News", "Sports", "Special"]),
            random.randint(60, 180),
            "G",
            "General Audience",
        )
    )

try:

    execute_values(
    cur,
    """
    INSERT INTO program (
        title,
        program_type,
        genre,
        duration_minutes,
        content_rating,
        target_demographic
    )
    VALUES %s
    ON CONFLICT (title)
    DO NOTHING
    """,
    programs,
    )

    conn.commit()

    print(f"✓ Seeded {len(programs)} programs")

except Exception as e:
    conn.rollback()
    print(f"✗ Failed: {e}")
    raise

brands = [
    "NovaTel",
    "FreshBite",
    "AetherBank",
    "PulseFit",
    "SkyDrive",
    "LunaMart",
    "Vertex Auto",
    "PureHome",
    "BrightWave",
    "AquaLife",
]

campaigns = [
    "Summer Blast",
    "Holiday Specials",
    "Back to School",
    "New Beginnings",
    "Family First",
    "Weekend Deals",
    "Premium Rewards",
    "Healthy Living",
    "Future Forward",
    "Dream Big",
]

commercial_demographics = [
    "Children",
    "Teens",
    "Young Adults",
    "Adults",
    "Families",
    "General Audience",
]

commercial_lengths = [15, 30, 60]

commercials = []
used_campaigns = set()

while len(commercials) < 50:
    brand = random.choice(brands)
    campaign = random.choice(campaigns)

    key = (brand, campaign)

    if key in used_campaigns:
        continue

    used_campaigns.add(key)

    commercials.append(
        (
            brand,
            campaign,
            random.choice(commercial_lengths),
            random.choice(commercial_demographics),

            date(
                random.randint(2016, 2025),
                random.randint(1, 12),
                random.randint(1, 28),
            ),

            date(
                random.randint(2026, 2027),
                random.randint(1, 12),
                random.randint(1, 28),
            ),
        )
    )

try:

    execute_values(
    cur,
    """
    INSERT INTO commercial (
        brand_name,
        campaign_name,
        duration_seconds,
        target_demographic,
        campaign_start,
        campaign_end
    )
    VALUES %s
    ON CONFLICT (brand_name, campaign_name)
    DO NOTHING
    """,
    commercials,
    )

    conn.commit()

    print(f"✓ Seeded {len(commercials)} commercials")

except Exception as e:
    conn.rollback()
    print(f"✗ Failed: {e}")
    raise

finally:
    cur.close()
    conn.close()