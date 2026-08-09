from pydantic import BaseModel, Field
from typing import Optional, List, Union, Literal

class ScenarioEvent(BaseModel):
    type: str # "supplier_delay", "demand_change", "supply_reduction"
    
    # Specific fields based on type
    supplier_id: Optional[int] = None
    delay_days: Optional[int] = None
    
    demand_multiplier: Optional[float] = None
    supply_multiplier: Optional[float] = None

class SimulationRequest(BaseModel):
    product_id: int
    warehouse_id: int
    horizon_days: int = 30
    scenario: Optional[ScenarioEvent] = None
    scenarios: Optional[List[ScenarioEvent]] = None

class SimulationState(BaseModel):
    stockout: bool
    stockout_date: Optional[str] = None
    ending_inventory: float

class SimulationImpact(BaseModel):
    additional_shortage_units: float
    inventory_delta: float

class SimulationResponse(BaseModel):
    scenario_type: str
    baseline: SimulationState
    scenario: SimulationState
    impact: SimulationImpact
    recommendations: List[str]
