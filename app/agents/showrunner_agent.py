# app/agents/showrunner_agent.py

import datetime

from app.models.showrunner import (
    EditorialVision,
)


def generate_editorial_vision(
    target_date: datetime.date,
    network_identity: dict,
) -> EditorialVision:
    """
    Generate the editorial direction
    for the day.
    """

    weekday = target_date.strftime("%A")

    if weekday == "Saturday":

        return EditorialVision(
            theme="Weekend Adventure",

            editorial_brief=(
                "A day of discovery, "
                "escapism, and excitement "
                "building toward an "
                "adventurous Prime Time."
            ),
        )

    if weekday == "Sunday":

        return EditorialVision(
            theme="Family Relaxation",

            editorial_brief=(
                "Comfortable, uplifting "
                "television designed for "
                "families winding down "
                "before the week ahead."
            ),
        )

    return EditorialVision(
        theme=(
            f"{network_identity['name']} "
            f"Weekday Programming"
        ),

        editorial_brief=(
            "Balanced programming that "
            "supports everyday routines "
            "while expressing the "
            "network identity."
        ),
    )