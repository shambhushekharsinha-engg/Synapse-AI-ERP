from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import products, forecast
from app.core.config import settings
from ml.registry import ModelRegistry
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Preload the ML model into memory
    registry = ModelRegistry()
    # Path is relative to where uvicorn is run (typically inside backend/)
    artifact_path = os.path.join(os.path.dirname(__file__), "../../ml/artifacts/xgboost_forecaster.json")
    try:
        registry.load_model("xgboost", artifact_path)
    except FileNotFoundError:
        print(f"Warning: Model artifact not found at {artifact_path}. Forecast API will return 503.")

from app.api.endpoints import products, forecast, inventory_intelligence

app.include_router(products.router, prefix=f"{settings.API_V1_STR}/products", tags=["products"])
app.include_router(forecast.router, prefix=f"{settings.API_V1_STR}/forecast", tags=["forecast"])
app.include_router(inventory_intelligence.router, prefix=f"{settings.API_V1_STR}/intelligence/inventory", tags=["inventory_intelligence"])

@app.get("/")
def root():
    return {"message": "Welcome to Synapse AI ERP API"}

@app.get("/health")
def health_check():
app.include_router(api_router, prefix="/api/v1")
