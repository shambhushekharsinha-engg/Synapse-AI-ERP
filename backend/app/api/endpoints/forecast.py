from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from app.schemas.forecast import ForecastResponse
from app.services.forecast import ForecastService
from ml.registry import ModelRegistry

router = APIRouter()

# Dependency to get the Forecast Service
def get_forecast_service():
    registry = ModelRegistry()
    return ForecastService(registry)

@router.get("/{product_id}", response_model=ForecastResponse)
def get_forecast(
    product_id: int,
    warehouse_id: Optional[int] = Query(None, description="Optional warehouse ID"),
    horizon_days: int = Query(14, ge=1, le=90, description="Forecast horizon in days (1-90)"),
    service: ForecastService = Depends(get_forecast_service)
):
    try:
        return service.get_forecast(product_id, warehouse_id, horizon_days)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred during forecasting.")
