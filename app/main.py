from pathlib import Path

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .domain import (
    user_router,
    auth_router,
    tour_router,
    media_router,
)

app = FastAPI(
    title="MyTour API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure local media directory exists (served via GET /api/media/files/...)
Path(settings.MEDIA_ROOT).mkdir(parents=True, exist_ok=True)

api = APIRouter(prefix="/api")
api.include_router(user_router)
api.include_router(auth_router)
api.include_router(tour_router)
api.include_router(media_router)

app.include_router(api)


@app.get("/health", tags=["health"])
def check_health():
    return {"status": "Ngon chim"}
