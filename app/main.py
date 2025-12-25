from fastapi import FastAPI
from app.ai.routes import router as ai_router

app = FastAPI(
    title="Little Naples AI Catering Engine (PoC)",
    description="AI backend for catering ingredient calculation",
    version="1.0.0"
)

app.include_router(ai_router, prefix="/ai", tags=["AI"])

@app.get("/health")
def health_check():
    return {"status": "OK", "service": "AI Backend Running"}
