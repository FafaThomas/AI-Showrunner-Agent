import json
from pathlib import Path


def build_showrunner_prompt(
    target_date,
    network_identity,
    theme,
    editorial_brief,
    slots,
    programs,
    historical_insights,
    feedback=None,
):
    """
    Construct the Showrunner prompt.
    """

    valid_program_keys = [
        p["program_key"]
        for p in programs
    ]

    revision_notes = ""

    if feedback:
        revision_notes = f"""
==================================================
REVISION NOTES
==================================================

Your previous schedule proposal was rejected.

Reason:

{feedback}

Revise the schedule.

Preserve the original editorial intent.

Correct the mistakes without introducing new ones.
"""

    prompt_path = (
        Path(__file__).parent.parent
        / "prompts"
        / "showrunner_prompt.txt"
    )

    template = prompt_path.read_text(
        encoding="utf-8"
    )

    return template.format(
        target_date=target_date,

        network_identity=network_identity,

        theme=theme,

        editorial_brief=editorial_brief,

        historical_insights="\n".join(
            historical_insights
        ),

        programs=json.dumps(
            programs,
            indent=2,
        ),

        valid_program_keys=valid_program_keys,

        slots=json.dumps(
            slots,
            indent=2,
        ),

        slot_count=len(slots),

        revision_notes=revision_notes,
    )

def build_librarian_prompt(
    theme,
    editorial_brief,
    programs,
):
    """
    Construct the Librarian prompt.
    """

    valid_program_keys = [
        p["program_key"]
        for p in programs
    ]

    prompt_path = (
        Path(__file__).parent.parent
        / "prompts"
        / "librarian_prompt.txt"
    )

    template = prompt_path.read_text(
        encoding="utf-8"
    )

    return template.format(
        theme=theme,

        editorial_brief=editorial_brief,

        programs=json.dumps(
            programs,
            indent=2,
        ),

        valid_program_keys=valid_program_keys,
    )