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
