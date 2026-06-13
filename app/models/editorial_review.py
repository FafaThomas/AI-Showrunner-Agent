from typing import List

from pydantic import BaseModel, Field


class EditorialDecision(BaseModel):

    approved: bool = Field(
        ...,
        description="Whether the schedule passes review."
    )

    notes: List[str] = Field(
        default_factory=list,
        description=(
            "Feedback from the editorial board."
        )
    )