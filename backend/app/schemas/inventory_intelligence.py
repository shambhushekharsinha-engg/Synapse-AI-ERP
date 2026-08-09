from pydantic import BaseModel
from typing import Optional

class EOQResponse(BaseModel):
    product_id: int
    annual_demand: float
    ordering_cost: float
    holding_cost: float
    eoq: float
    cost_source: str

class ROPResponse(BaseModel):
    product_id: int
    reorder_point: float
    current_inventory: float
    reorder_required: bool
    safety_stock: float
    demand_std_dev: float
    lead_time_days: int
    service_level: float
    z_score: float

class ABCClassificationResponse(BaseModel):
    product_id: int
    sku: str
    annual_consumption_value: float
    abc_class: str
    cumulative_percentage: float

class StockoutRiskResponse(BaseModel):
    product_id: int
    stockout_risk: str # "HIGH", "MEDIUM", "LOW"
    stockout_expected: bool
    expected_stockout_date: Optional[str] = None
    forecast_horizon_days: int
    current_inventory: float
    forecasted_demand: float
    planned_inbound: float

class DeadStockResponse(BaseModel):
    product_id: int
    is_dead_stock: bool
    inventory_units: float
    forecast_demand_30d: float
    days_since_last_sale: int
    reason: str

class InventoryTurnoverResponse(BaseModel):
    product_id: int
    turnover_ratio: float
    calculation_method: str # e.g. "revenue_based_proxy"
    average_inventory: float
    annual_cogs_or_revenue: float

