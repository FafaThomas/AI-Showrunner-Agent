from typing import List

from pydantic import BaseModel, Field, model_validator


class ScheduleSlot(BaseModel):
    """
    Represents a single broadcast slot.
    """

    slot_key: int = Field(
        ...,
        description="Database slot identifier."
    )

    time: str = Field(
        ...,
        description="Human-readable slot time."
    )

    program_key: int = Field(
        ...,
        description="Selected program identifier."
    )

    reason: str = Field(
        ...,
        description=(
            "Editorial explanation for why "
            "this program was chosen."
        )
    )


class DailySchedule(BaseModel):
    """
    Represents the full schedule for one day.
    """

    theme: str = Field(
        ...,
        description="Overall editorial theme."
    )

    slots: List[ScheduleSlot] = Field(
        ...,
        description="The complete day's schedule."
    )

    @property
    def slot_count(self) -> int:
        return len(self.slots)

    @model_validator(mode="after")
    def validate_slot_uniqueness(self):
        """
        Prevent duplicate slot assignments.
        """

        slot_keys = [
            slot.slot_key
            for slot in self.slots
        ]

        if len(slot_keys) != len(set(slot_keys)):
            raise ValueError(
                "Duplicate slot_key detected."
            )

        return self