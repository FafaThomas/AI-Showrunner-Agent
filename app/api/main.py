from fastapi import FastAPI

from app.api.routes.schedules import (
    router as schedules_router,
)


app = FastAPI(
    title="AI Showrunner API",
    version="2.0.0",
    description=(
        "Generate AI-curated television "
        "schedules using a multi-agent "
        "broadcast pipeline."
    ),
)

app.include_router(
    schedules_router,
    prefix="/api/v1/schedules",
    tags=["Schedules"],
)


@app.get("/")
def root():
    return {
        "service": "AI Showrunner API",
        "version": "2.0.0",
        "status": "online",
    }