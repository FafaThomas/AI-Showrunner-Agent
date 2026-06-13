import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

def connect_db():
    """
    Create a PostgreSQL connection.
    """

    load_dotenv()

    base_dir = Path(__file__).resolve().parents[2]

    password_path = (
        base_dir
        / "secrets"
        / "postgres_password.txt"
    )

    db_password = password_path.read_text().strip()

    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(
            os.getenv("POSTGRES_PORT", 5432)
        ),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=db_password,
    )

def load_programs(cur):
    """
    Load all available programs.
    """

    cur.execute("""
        SELECT
            program_key,
            title,
            program_type,
            genre,
            target_demographic
        FROM program
        ORDER BY title
    """)

    return [
        {
            "program_key": row[0],
            "title": row[1],
            "program_type": row[2],
            "genre": row[3],
            "target_demographic": row[4],
        }
        for row in cur.fetchall()
    ]


def load_slots(cur):
    """
    Load the 24 broadcast slots.
    """

    cur.execute("""
        SELECT
            slot_key,
            slot_name,
            daypart,
            start_time,
            end_time
        FROM slot
        ORDER BY start_time
    """)

    return [
        {
            "slot_key": row[0],
            "time": row[1],
            "daypart": row[2],
            "start_time": str(row[3]),
            "end_time": str(row[4]),
        }
        for row in cur.fetchall()
    ]

def load_historical_insights(cur):
    """
    Summarize historical performance
    for Showrunner decision-making.
    """

    cur.execute("""
        SELECT
            s.daypart,
            p.genre,

            ROUND(
                AVG(sv.viewer_count)
            ) AS avg_viewers,

            ROUND(
                AVG(sv.retention_rate)::numeric,
                2
            ) AS avg_retention

        FROM slot_program sp

        JOIN slot s
            ON sp.slot_key = s.slot_key

        JOIN program p
            ON sp.program_key = p.program_key

        JOIN slot_viewership sv
            ON sp.slot_key = sv.slot_key
           AND sp.broadcast_date =
               sv.broadcast_date

        GROUP BY
            s.daypart,
            p.genre

        ORDER BY
            avg_viewers DESC
    """)

    insights = []

    for row in cur.fetchall():

        insights.append(
            (
                f"{row[0]} | "
                f"{row[1]} | "
                f"Avg Viewers: "
                f"{int(row[2]):,} | "
                f"Retention: "
                f"{row[3]}"
            )
        )

    return insights

def load_network_identity():
    """
    Defines the personality
    of the network.
    """

    return {
        "name": "Crimson Broadcasting Network",

        "identity": (
            "Family-oriented fantasy "
            "and prestige storytelling."
        ),

        "core_values": [
            "Escapism",
            "Warmth",
            "Adventure",
        ],
    }
