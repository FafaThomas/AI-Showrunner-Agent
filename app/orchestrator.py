# app/orchestrator.py

import datetime

from app.database.db import (
    connect_db,
    load_programs,
    load_slots,
    load_historical_insights,
    load_network_identity,
)

from app.agents.showrunner import (
    generate_editorial_vision,
)

from app.agents.librarian import (
    curate_programs,
)

from app.agents.scheduler import (
    generate_schedule,
)

from app.services.validator import (
    validate_schedule,
)

from app.agents.editorial_board import (
    review_schedule,
)

from app.services.xml_exporter import (
    schedule_to_xml,
    save_xml,
)

def orchestrate(
    target_date: datetime.date,
):
    conn = connect_db()
    cur = conn.cursor()

    try:

        print("Loading memory...")

        programs = load_programs(cur)

        slots = load_slots(cur)

        historical_insights = (
            load_historical_insights(cur)
        )

        network_identity = (
            load_network_identity()
        )

        print("\nSHOWRUNNER")

        vision = generate_editorial_vision(
            target_date=target_date,

            network_identity=(
                network_identity["identity"]
            ),

            historical_insights=(
                historical_insights
            ),
        )

        print(
            f"Theme: {vision.theme}"
        )

        print(
            f"Brief: "
            f"{vision.editorial_brief}"
        )

        MAX_RETRIES = 3

        librarian_feedback = None
        scheduler_feedback = None

        for attempt in range(
            1,
            MAX_RETRIES + 1,
        ):
            
            print(f"\nLIBRARIAN"
                 f"ATTEMPT {attempt}/{MAX_RETRIES}" 
                  )

            recommendation = (
                curate_programs(
                    theme=vision.theme,

                    editorial_brief=(
                        vision.editorial_brief
                    ),

                    programs=programs,

                    feedback=librarian_feedback,
                )
            )

            approved_keys = (
                recommendation
                .recommended_program_keys
            )

            curated_programs = [
                p
                for p in programs
                if p["program_key"]
                in approved_keys
            ]

            print(
                f"Approved: "
                f"{approved_keys}"
            )

            print("\nSCHEDULER")

            print(
                f"\nScheduling Attempt "
                f"{attempt}/{MAX_RETRIES}"
            )

            schedule = generate_schedule(
                theme=vision.theme,

                editorial_brief=(
                    vision.editorial_brief
                ),

                slots=slots,

                programs=curated_programs,
            )

            print("\nVALIDATOR")

            is_valid, feedback = (
                validate_schedule(
                    schedule,
                    slots,
                    curated_programs,
                )
            )

            if not is_valid:

                print(
                    "\nVALIDATOR REJECTED:"
                )

                print(feedback)

                scheduler_feedback = (
                    f"Validator Rejection:\n"
                    f"{feedback}"
                )

                continue

            print(
                "\nEDITORIAL REVIEW"
            )

            decision = review_schedule(
                vision=vision,

                approved_programs=(
                    curated_programs
                ),

                schedule=schedule,
            )

            if not decision.approved:

                print(
                    "\nEDITORIAL BOARD "
                    "REJECTED:"
                )

                for note in decision.notes:

                    print(
                        f"- {note}"
                    )

                librarian_feedback = (
                    "Editorial Board "
                    "Rejection:\n"
                    + "\n".join(
                        decision.notes
                    )
                )

                continue


            print(
                    "\nEDITORIAL BOARD "
                    "APPROVED."
                )

            break

        else:

            raise RuntimeError(
                "Failed to produce "
                "an approved schedule "
                f"after {MAX_RETRIES} "
                "attempts."
            )
           

        print("\nEXPORT")

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
            f"Saved to "
            f"{filename}"
        )

        return schedule

    finally:

        cur.close()

        conn.close()

def main():

    schedule = orchestrate(
        datetime.date.today()
    )

    print(
        "\nFINAL SCHEDULE"
    )

    print(
        schedule.theme
    )


if __name__ == "__main__":
    main()