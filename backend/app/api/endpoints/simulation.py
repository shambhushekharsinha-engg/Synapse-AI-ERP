from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.domain import Inventory
from app.schemas.simulation import SimulationRequest, SimulationResponse, ScenarioEvent
from app.services.simulation.engine import SimulationEngine
from app.services.forecast import ForecastService
from ml.registry import ModelRegistry
import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_forecast_service():
    registry = ModelRegistry()
    return ForecastService(registry)

@router.post("/scenarios", response_model=SimulationResponse)
def run_simulation(
    request: SimulationRequest,
    db: Session = Depends(get_db),
    forecast_svc: ForecastService = Depends(get_forecast_service)
):
    inventory = db.query(Inventory).filter(
        Inventory.product_id == request.product_id, 
        Inventory.warehouse_id == request.warehouse_id
    ).first()
    
    current_inventory = inventory.quantity if inventory else 0.0
    
    try:
        forecast_response = forecast_svc.get_forecast(request.product_id, request.warehouse_id, request.horizon_days)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Forecast unavailable: {str(e)}")
        
    daily_demands = [fp.predicted_demand for fp in forecast_response.forecast]
    # For MVP, assume 0 planned inbounds unless modeled specifically
    daily_inbounds = [0.0] * request.horizon_days
    
    start_date = datetime.date.today()
    
    scenarios = []
    if request.scenario:
        scenarios.append(request.scenario)
    if request.scenarios:
        scenarios.extend(request.scenarios)
        
    return SimulationEngine.run_simulation(
        initial_inventory=current_inventory,
        daily_demands=daily_demands,
        daily_inbounds=daily_inbounds,
        start_date=start_date,
        scenarios=scenarios
    )
