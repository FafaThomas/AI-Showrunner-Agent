import json
import ollama

from app.models.editorial_review import (
    EditorialDecision,
)

from app.services.prompt_builder import (
    build_editorial_review_prompt,
)

MODEL_NAME = "qwen2.5:14b"


def review_schedule(
    vision,
    approved_programs,
    schedule,
):

    prompt = build_editorial_review_prompt(
        theme=vision.theme,

        editorial_brief=(
            vision.editorial_brief
        ),

        approved_programs=approved_programs,

        schedule=schedule,
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
    print("EDITORIAL BOARD")
    print("=" * 80)
    print(raw_response)
    print("=" * 80)

    data = json.loads(raw_response)

    return EditorialDecision.model_validate(
        data
    )