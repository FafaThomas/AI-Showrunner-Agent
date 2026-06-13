# app/agents/librarian.py

import json
import ollama

from app.models.librarian import (
    LibrarianRecommendation,
)

from app.services.prompt_builder import (
    build_librarian_prompt,
)

MODEL_NAME = "qwen2.5:14b"


def curate_programs(
    theme,
    editorial_brief,
    programs,
):
    """
    Curate a shortlist of programs
    matching the editorial vision.
    """

    prompt = build_librarian_prompt(
        theme=theme,

        editorial_brief=editorial_brief,

        programs=programs,
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
    print("LIBRARIAN RESPONSE")
    print("=" * 80)
    print(raw_response)
    print("=" * 80)

    data = json.loads(
        raw_response
    )

    recommendation = (
        LibrarianRecommendation.model_validate(
            data
        )
    )

    return recommendation

if __name__ == "__main__":

    from app.database.db import (
        connect_db,
        load_programs,
    )

    conn = connect_db()
    cur = conn.cursor()

    try:

        programs = load_programs(cur)

        result = curate_programs(
            theme="Weekend Adventure",

            editorial_brief=(
                "A day of discovery, escapism, "
                "and excitement."
            ),

            programs=programs,
        )

        print("\nCURATED PROGRAMS")

        print(
            result.model_dump_json(
                indent=4,
            )
        )

    finally:

        cur.close()
        conn.close()