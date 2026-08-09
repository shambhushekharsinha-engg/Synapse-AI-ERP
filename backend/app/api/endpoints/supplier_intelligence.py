from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.supplier_intelligence import (
    SupplierScoreResponse, SupplierLeadTimeAnalytics, 
    SupplierDelayRiskResponse, SupplierComparisonProduct, SupplierComparisonResponse
)
from app.services.supplier_intelligence import SupplierIntelligenceService

router = APIRouter()

@router.get("/{supplier_id}/score", response_model=SupplierScoreResponse)
def get_supplier_score(
    supplier_id: int,
    on_time_rate: float = Query(...),
    avg_lead_time_days: float = Query(...),
    delay_rate: float = Query(...)
):
    # In reality, these metrics would be queried from the DB (Purchase Orders). 
    # For MVP, we pass them as queries to demonstrate the calculation.
    return SupplierIntelligenceService.calculate_supplier_score(
        supplier_id, on_time_rate, avg_lead_time_days, delay_rate
    )

@router.post("/{supplier_id}/lead-time-analytics", response_model=SupplierLeadTimeAnalytics)
def get_lead_time_analytics(
    supplier_id: int,
    historical_lead_times: List[float],
    delay_frequency: float = Query(...)
):
    return SupplierIntelligenceService.calculate_lead_time_analytics(
        supplier_id, historical_lead_times, delay_frequency
    )

@router.get("/{supplier_id}/delay-risk", response_model=SupplierDelayRiskResponse)
def get_delay_risk(
    supplier_id: int,
    delay_frequency: float = Query(...),
    lead_time_variance: float = Query(...),
    lead_time_trend: str = Query("STABLE")
):
    return SupplierIntelligenceService.evaluate_delay_risk(
        supplier_id, delay_frequency, lead_time_variance, lead_time_trend
    )

@router.post("/compare/{product_id}", response_model=SupplierComparisonResponse)
def compare_suppliers(
    product_id: int,
    suppliers_data: List[dict] # Expected: supplier_id, supplier_name, avg_lead_time, on_time_rate, delay_rate, avg_order_qty
):
    comparison_list = []
    for s in suppliers_data:
        # Get score
        score_res = SupplierIntelligenceService.calculate_supplier_score(
            s['supplier_id'], s['on_time_rate'], s['avg_lead_time'], s['delay_rate']
        )
        
        comparison_list.append(
            SupplierComparisonProduct(
                supplier_id=s['supplier_id'],
                supplier_name=s['supplier_name'],
                avg_lead_time=s['avg_lead_time'],
                on_time_rate=s['on_time_rate'],
                delay_rate=s['delay_rate'],
                avg_order_qty=s['avg_order_qty'],
                score=score_res.score
            )
        )
        
    return SupplierComparisonResponse(
        product_id=product_id,
        suppliers=comparison_list
    )
