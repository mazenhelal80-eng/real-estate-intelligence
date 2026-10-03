from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas.ml import HealthResponse
from backend.api.routes.ml import router as ml_router

app = FastAPI(
    title="Real Estate Intelligence & AI Decision Engine API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    return HealthResponse(status="ok", version="1.0.0")

app.include_router(ml_router)
