from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    sku: str
    name: str
    category: Optional[str] = None
    unit_price: float
    ordering_cost_per_order: Optional[float] = None
    annual_holding_cost_per_unit: Optional[float] = None
    lead_time_days: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    class Config:
        orm_mode = True

class WarehouseBase(BaseModel):
    name: str
    location: str
    capacity: int

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseResponse(WarehouseBase):
    id: int
    class Config:
        orm_mode = True
