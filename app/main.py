from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .domain import (
    user_router,
    auth_router
)

app = FastAPI(
    title="MyTour API",
    version="1.0.0",
    root_path="/api"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(auth_router)

@app.get("/health", tags=["health"])
def check_health():
    return {"status": "Ngon chim"}
