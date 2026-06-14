from pydantic import BaseModel


class GenerateScheduleRequest(BaseModel):
    days_ahead: int = 1


class SlotResponse(BaseModel):
    slot_key: int
    time: str
    program_key: int
    reason: str


class GenerateScheduleResponse(BaseModel):
    approved: bool

    target_date: str

    theme: str
    editorial_brief: str

    editorial_notes: list[str]

    schedule: list[SlotResponse]

    xml_filename: str