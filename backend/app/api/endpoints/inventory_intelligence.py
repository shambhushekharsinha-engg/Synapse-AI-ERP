from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import SessionLocal
from app.models.domain import Product, Inventory
from app.schemas.inventory_intelligence import EOQResponse, ROPResponse, ABCClassificationResponse
from app.services.inventory_math import InventoryMath
from app.services.abc_analysis import ABCAnalysisService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{product_id}/eoq", response_model=EOQResponse)
def get_eoq(product_id: int, annual_demand: float = Query(..., gt=0), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    # Cost fallback logic
    ordering_cost = product.ordering_cost_per_order
    holding_cost = product.annual_holding_cost_per_unit
    cost_source = "product"
    
    if ordering_cost is None:
        ordering_cost = 150.0 # Configurable system default
        cost_source = "default"
        
    if holding_cost is None:
        holding_cost = product.unit_price * 0.20 # Default 20% holding rate
        cost_source = "default"
        
    eoq_val = InventoryMath.calculate_eoq(annual_demand, ordering_cost, holding_cost)
    
    return EOQResponse(
        product_id=product_id,
        annual_demand=annual_demand,
        ordering_cost=ordering_cost,
        holding_cost=holding_cost,
        eoq=round(eoq_val, 2),
        cost_source=cost_source
    )

@router.get("/{product_id}/rop", response_model=ROPResponse)
def get_rop(
    product_id: int, 
    warehouse_id: int,
    average_daily_demand: float = Query(..., gt=0),
    demand_std_dev: float = Query(..., ge=0),
    service_level: float = Query(0.95, ge=0.5, le=0.999),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id, 
        Inventory.warehouse_id == warehouse_id
    ).first()
    
    current_inventory = inventory.quantity if inventory else 0.0
    
    lead_time_days = product.lead_time_days
    z_score = InventoryMath.get_z_score(service_level)
    
    safety_stock = InventoryMath.calculate_safety_stock(z_score, demand_std_dev, lead_time_days)
    rop = InventoryMath.calculate_reorder_point(average_daily_demand, lead_time_days, safety_stock)
    
    reorder_required = current_inventory < rop
    
    return ROPResponse(
        product_id=product_id,
        reorder_point=round(rop, 2),
        current_inventory=current_inventory,
        reorder_required=reorder_required,
        safety_stock=round(safety_stock, 2),
        demand_std_dev=demand_std_dev,
        lead_time_days=lead_time_days,
        service_level=service_level,
        z_score=z_score
    )

@router.post("/abc-classification", response_model=List[ABCClassificationResponse])
def run_abc_classification(data: List[dict]):
    # In a real system, this would fetch the catalog and annual demand directly from the DB.
    # For this endpoint, we accept a list of product dictionaries for flexibility.
    return ABCAnalysisService.classify_products(data)

from app.schemas.inventory_intelligence import StockoutRiskResponse, DeadStockResponse, InventoryTurnoverResponse
from app.services.stockout_risk import StockoutRiskService
from app.services.dead_stock import DeadStockService
from app.services.inventory_turnover import InventoryTurnoverService
from app.services.forecast import ForecastService
from ml.registry import ModelRegistry

def get_forecast_service():
    registry = ModelRegistry()
    return ForecastService(registry)

@router.get("/{product_id}/stockout-risk", response_model=StockoutRiskResponse)
def get_stockout_risk(
    product_id: int, 
    warehouse_id: int = Query(...),
    horizon_days: int = Query(14),
    planned_inbound: float = Query(0.0),
    db: Session = Depends(get_db),
    forecast_svc: ForecastService = Depends(get_forecast_service)
):
    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id, 
        Inventory.warehouse_id == warehouse_id
    ).first()
    
    current_inventory = inventory.quantity if inventory else 0.0
    
    # Delegate forecast entirely to Phase 2, isolating the ML model.
    try:
        forecast_response = forecast_svc.get_forecast(product_id, warehouse_id, horizon_days)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Forecast unavailable: {str(e)}")
        
    forecast_points = [{"date": fp.date.strftime("%Y-%m-%d"), "predicted_demand": fp.predicted_demand} for fp in forecast_response.forecast]
    
    import datetime
    start_date = datetime.datetime.utcnow()
    
    risk_dict = StockoutRiskService.calculate_risk(
        product_id=product_id,
        current_inventory=current_inventory,
        forecast=forecast_points,
        planned_inbound=planned_inbound,
        start_date=start_date
    )
    
    return StockoutRiskResponse(**risk_dict)

@router.get("/{product_id}/dead-stock", response_model=DeadStockResponse)
def get_dead_stock(
    product_id: int, 
    warehouse_id: int = Query(...),
    days_since_last_sale: int = Query(...),
    db: Session = Depends(get_db),
    forecast_svc: ForecastService = Depends(get_forecast_service)
):
    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id, 
        Inventory.warehouse_id == warehouse_id
    ).first()
    
    current_inventory = inventory.quantity if inventory else 0.0
    
    try:
        # Forecast for 30 days
        forecast_response = forecast_svc.get_forecast(product_id, warehouse_id, 30)
        total_forecast_30d = sum([fp.predicted_demand for fp in forecast_response.forecast])
    except Exception:
        total_forecast_30d = 0.0
        
    ds_dict = DeadStockService.evaluate(
        product_id=product_id,
        inventory_units=current_inventory,
        days_since_last_sale=days_since_last_sale,
        forecast_demand_30d=total_forecast_30d
    )
    
    return DeadStockResponse(**ds_dict)

@router.get("/{product_id}/turnover", response_model=InventoryTurnoverResponse)
def get_turnover(
    product_id: int,
    warehouse_id: int = Query(...),
    annual_revenue: float = Query(...),
    db: Session = Depends(get_db)
):
    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id, 
        Inventory.warehouse_id == warehouse_id
    ).first()
    
    # In MVP, average inventory is just current inventory
    average_inventory = inventory.quantity if inventory else 0.0
    
    turnover_dict = InventoryTurnoverService.calculate(
        product_id=product_id,
        revenue=annual_revenue,
        average_inventory=average_inventory
    )
    
    return InventoryTurnoverResponse(**turnover_dict)
