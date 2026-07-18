from fastapi import FastAPI
from .domain import user_router
app = FastAPI (
    title="MyTour API",
    version="1.0.0",
    root_path="/api"
)

app.include_router(user_router)

@app.get("/health", tags=["health"])
def check_health():
    return {"status": "Ngon chim"}
