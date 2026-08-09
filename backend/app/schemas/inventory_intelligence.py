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
