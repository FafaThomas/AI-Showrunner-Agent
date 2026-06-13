# app/agents/showrunner.py

import json
import ollama

from app.models.showrunner import (
    EditorialVision,
)

from app.services.prompt_builder import (
    build_showrunner_prompt,
)

MODEL_NAME = "qwen2.5:14b"


def generate_editorial_vision(
    target_date,
    network_identity,
    historical_insights,
):
    """
    Generate the editorial vision
    for the broadcast day.
    """

    prompt = build_showrunner_prompt(
        target_date=target_date,

        network_identity=network_identity,

        historical_insights=historical_insights,
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
    print("SHOWRUNNER RESPONSE")
    print("=" * 80)
    print(raw_response)
    print("=" * 80)

    data = json.loads(
        raw_response
    )

    return EditorialVision.model_validate(
        data
    )

if __name__ == "__main__":

    import datetime

    vision = generate_editorial_vision(
        target_date=datetime.date.today(),

        network_identity="""
Family-focused entertainment network
that values optimism, discovery,
and emotional storytelling.
""",

        historical_insights=[
            "Adventure programs perform well on weekends.",
            "Families prefer uplifting content on Sundays.",
            "Prime Time viewers engage strongly with emotional narratives.",
        ],
    )

    print("\nEDITORIAL VISION")

    print(
        vision.model_dump_json(
            indent=4,
        )
    )