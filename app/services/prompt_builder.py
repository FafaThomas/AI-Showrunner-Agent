import json
from pathlib import Path


def build_showrunner_prompt(
    target_date,
    network_identity,
    historical_insights,
):
    """
    Construct the Showrunner prompt.
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

        historical_insights="\n".join(
            historical_insights
        ),
    )

def build_librarian_prompt(
    theme,
    editorial_brief,
    programs,
    feedback=None,
):
    """
    Construct the Librarian prompt.
    """

    valid_program_keys = [
        p["program_key"]
        for p in programs
    ]

    feedback_text = ""

    if feedback:

        feedback_text = f"""

==================================================
PREVIOUS EDITORIAL FEEDBACK
==================================================

The Editorial Board rejected the previous catalog.

Address the following concerns:

{feedback}
"""

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

        feedback=feedback_text,
    )

def build_scheduler_prompt(
    theme,
    editorial_brief,
    slots,
    programs,
    feedback=None,
):
    """
    Construct the Scheduler prompt.
    """

    from pathlib import Path
    import json

    valid_program_keys = [
        p["program_key"]
        for p in programs
    ]

    revision_notes = ""

    if feedback:

        revision_notes = f"""
The previous schedule proposal was rejected.

Reason:

{feedback}

Revise the schedule while preserving the editorial vision.
"""

    prompt_path = (
        Path(__file__).parent.parent
        / "prompts"
        / "scheduler_prompt.txt"
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

        slots=json.dumps(
            slots,
            indent=2,
        ),

        slot_count=len(slots),

        revision_notes=revision_notes,
    )

def build_editorial_review_prompt(
    theme,
    editorial_brief,
    approved_programs,
    schedule,
):
    from pathlib import Path
    import json

    prompt_path = (
        Path(__file__).parent.parent
        / "prompts"
        / "editorial_review_prompt.txt"
    )

    template = prompt_path.read_text(
        encoding="utf-8"
    )

    return template.format(
        theme=theme,

        editorial_brief=editorial_brief,

        approved_programs=json.dumps(
            approved_programs,
            indent=2,
        ),

        schedule=json.dumps(
            schedule.model_dump(),
            indent=2,
        ),
    )