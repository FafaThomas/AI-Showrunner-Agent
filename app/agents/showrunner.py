# app/agents/showrunner.py

import datetime
import json
import ollama

from app.database.db import (
    connect_db,
    load_programs,
    load_slots,
    load_historical_insights,
    load_network_identity,
)

from app.models.schedule import DailySchedule

from app.services.prompt_builder import (
    build_showrunner_prompt,
)

from app.services.validator import (
    validate_schedule,
)

from app.services.editorial_review import (
    review_schedule,
)

from app.services.xml_exporter import (
    schedule_to_xml,
    save_xml,
)

MODEL_NAME = "qwen2.5:14b"


def determine_theme(
    target_date: datetime.date,
    network_identity: dict,
) -> str:
    """
    Determine the editorial theme for the day.
    """

    weekday = target_date.strftime("%A")

    if weekday == "Saturday":
        return "Weekend Adventure"

    if weekday == "Sunday":
        return "Family Relaxation"

    return (
        f"{network_identity['name']} "
        f"Weekday Programming"
    )


def generate_schedule(
    target_date: datetime.date,
):
    conn = connect_db()
    cur = conn.cursor()

    try:
        print("Loading memory...")

        programs = load_programs(cur)

        slots = load_slots(cur)

        from app.services.retriever import (
            retrieve_programs,
        )

        historical_insights = (
            load_historical_insights(cur)
        )

        network_identity = (
            load_network_identity()
        )

        theme = determine_theme(
            target_date,
            network_identity,
        )

        print(
            f"Theme selected: {theme}"
        )

        
        candidate_programs = []

        seen = set()

        for slot in slots:

            retrieved = retrieve_programs(
                programs,
                theme,
                slot,
            )

            for program in retrieved:

                key = program["program_key"]

                if key not in seen:

                    candidate_programs.append(
                        program
                    )

                    seen.add(key)


        MAX_RETRIES = 5

        feedback = None

        for attempt in range(
            1,
            MAX_RETRIES + 1,
        ):

            print(
                f"\nConsulting the Showrunner..."
            )

            print(
                f"Attempt {attempt}/{MAX_RETRIES}"
            )

            prompt = build_showrunner_prompt(
                target_date=target_date.isoformat(),

                network_identity=(
                    network_identity["identity"]
                ),

                theme=theme,

                slots=slots,

                programs=candidate_programs,

                historical_insights=(
                    historical_insights
                ),

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
            print("RAW QWEN RESPONSE")
            print("=" * 80)
            print(raw_response)
            print("=" * 80 + "\n")
            try:
                data = json.loads(
                    raw_response
                )

                schedule = (
                    DailySchedule.model_validate(
                        data
                    )
                )

            except Exception as e:
                feedback = (
                    f"Your response could not "
                    f"be parsed.\n\n"
                    f"Error:\n{str(e)}"
                )

                print(
                    "Parsing failed:"
                )

                print(
                    feedback
                )

                continue

            is_valid, feedback = (
                validate_schedule(
                    schedule,
                    slots,
                    programs,
                )
            )

            if not is_valid:

                print(
                    "Structural validation failed."
                )

                print(feedback)

                continue

            print(
                "Structural validation passed."
            )

            editorial_ok, notes = review_schedule(
                schedule,
                programs,
                theme,
            )

            if not editorial_ok:

                feedback = (
                    "Editorial Review Failed:\n"
                    + "\n".join(notes)
                )

                print("\nEditorial Review Failed:")

                for note in notes:
                    print(f"- {note}")

                continue

            print(
                "Editorial review passed."
            )

            break

        else:

            raise RuntimeError(
                "Showrunner failed after "
                f"{MAX_RETRIES} attempts."
            )


        xml = schedule_to_xml(
            schedule,
            target_date.isoformat(),
        )

        filename = (
            f"schedule_"
            f"{target_date.isoformat()}.xml"
        )

        save_xml(
            xml,
            filename,
        )

        print(
            "\nShowrunner completed."
        )

        print(
            f"Saved to {filename}"
        )

        return schedule, programs

    finally:
        cur.close()
        conn.close()


def main():
    target_date = datetime.date.today()

    schedule, programs = generate_schedule(
        target_date
    )

    print()

    print(
        "Today's Theme:"
    )

    print(
        schedule.theme
    )

    print()

    print("\nEDITORIAL AUDIT")
    print("=" * 120)

    program_lookup = {
        p["program_key"]: p
        for p in programs
    }

    for slot in schedule.slots:

        program = program_lookup[
            slot.program_key
        ]

        print(
            f"{slot.time:<12}"
            f"{program['title']:<35}"
            f"{program['genre']:<15}"
            f"{program['program_type']:<12}"
        )

        print(
            f"Reason: {slot.reason}"
        )

        print("-" * 120)


if __name__ == "__main__":
    main()