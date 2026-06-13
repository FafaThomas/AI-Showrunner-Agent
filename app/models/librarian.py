# app/models/librarian.py

from typing import List

from pydantic import BaseModel, Field


class LibrarianRecommendation(BaseModel):
    """
    Curated catalog recommendation
    for the editorial vision.
    """

    recommended_program_keys: List[int] = Field(
        ...,
        description=(
            "Program IDs that best align "
            "with the editorial vision."
        ),
    )

    reason: str = Field(
        ...,
        description=(
            "Explanation for why these "
            "programs were selected."
        ),
    )