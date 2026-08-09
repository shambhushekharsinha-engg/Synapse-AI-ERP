import pytest
from app.services.stockout_risk import StockoutRiskService
from app.services.dead_stock import DeadStockService
from app.services.inventory_turnover import InventoryTurnoverService
from datetime import datetime

def test_stockout_risk():
    start_date = datetime(2026, 8, 10)
    forecast = [
        {"date": "2026-08-11", "predicted_demand": 50},
        {"date": "2026-08-12", "predicted_demand": 50},
        {"date": "2026-08-13", "predicted_demand": 50},
    ] # Total 150
    
    # Scenario 1: Stockout
    res1 = StockoutRiskService.calculate_risk(
        product_id=1, current_inventory=100, forecast=forecast, planned_inbound=0, start_date=start_date
    )
    assert res1['stockout_expected'] is True
    assert res1['stockout_risk'] == "HIGH"
    
    # Scenario 2: No stockout due to inbound
    res2 = StockoutRiskService.calculate_risk(
        product_id=1, current_inventory=100, forecast=forecast, planned_inbound=100, start_date=start_date
    )
    assert res2['stockout_expected'] is False
    assert res2['stockout_risk'] == "LOW"

def test_dead_stock():
    # Scenario 1: Dead stock
    res1 = DeadStockService.evaluate(
        product_id=1, inventory_units=800, days_since_last_sale=146, forecast_demand_30d=5.0
    )
    assert res1['is_dead_stock'] is True
    
    # Scenario 2: Healthy
    res2 = DeadStockService.evaluate(
        product_id=1, inventory_units=100, days_since_last_sale=2, forecast_demand_30d=80.0
    )
    assert res2['is_dead_stock'] is False

def test_turnover():
    res1 = InventoryTurnoverService.calculate(product_id=1, cogs=1000, average_inventory=100)
    assert res1['turnover_ratio'] == 10.0
    assert res1['calculation_method'] == "cogs_based"
    
    res2 = InventoryTurnoverService.calculate(product_id=1, revenue=5000, average_inventory=100)
    assert res2['turnover_ratio'] == 50.0
    assert res2['calculation_method'] == "revenue_based_proxy"
