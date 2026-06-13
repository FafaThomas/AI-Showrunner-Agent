# app/models/showrunner.py

from pydantic import BaseModel, Field


class EditorialVision(BaseModel):
    """
    High-level editorial direction
    for the broadcast day.
    """

    theme: str = Field(
        ...,
        description="Editorial theme."
    )

    editorial_brief: str = Field(
        ...,
        description=(
            "Narrative description of "
            "how the day should feel."
        )
    )