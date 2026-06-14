import datetime

from fastapi import APIRouter

from app.orchestrator import orchestrate

from app.api.schemas.schedule import (
    GenerateScheduleRequest,
    GenerateScheduleResponse,
)


router = APIRouter()


@router.post(
    "/generate",
    response_model=GenerateScheduleResponse,
)
def generate_schedule(
    request: GenerateScheduleRequest,
):
    target_date = (
        datetime.date.today()
        + datetime.timedelta(
            days=request.days_ahead
        )
    )

    result = orchestrate(
        target_date=target_date,
    )

    return result