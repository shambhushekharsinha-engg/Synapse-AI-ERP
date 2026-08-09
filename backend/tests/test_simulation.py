import pytest
import datetime
from app.schemas.simulation import ScenarioEvent
from app.services.simulation.engine import SimulationEngine

def test_no_change_scenario():
    initial_inv = 100
    demands = [10] * 5
    inbounds = [0] * 5
    start_date = datetime.date(2026, 8, 10)
    
    res = SimulationEngine.run_simulation(
        initial_inv, demands, inbounds, start_date, []
    )
    
    assert res.baseline.ending_inventory == 50
    assert res.scenario.ending_inventory == 50
    assert res.impact.inventory_delta == 0

def test_supplier_delay_scenario():
    initial_inv = 90
    demands = [10] * 10  # Needs 100 total
    inbounds = [0, 0, 0, 0, 100, 0, 0, 0, 0, 0] # Arrives day 5
    start_date = datetime.date(2026, 8, 10)
    
    sc = ScenarioEvent(type="supplier_delay", delay_days=6)
    
    res = SimulationEngine.run_simulation(
        initial_inv, demands, inbounds, start_date, [sc]
    )
    
    assert res.baseline.stockout is False
    assert res.scenario.stockout is True # Arrives on day 11, runs out on day 10
    assert res.impact.inventory_delta == -100 # At end of 10 days, inbound didn't arrive

def test_demand_spike_scenario():
    initial_inv = 100
    demands = [10] * 10
    inbounds = [0] * 10
    start_date = datetime.date(2026, 8, 10)
    
    sc = ScenarioEvent(type="demand_change", demand_multiplier=2.0)
    
    res = SimulationEngine.run_simulation(
        initial_inv, demands, inbounds, start_date, [sc]
    )
    
    assert res.baseline.stockout is False
    assert res.baseline.ending_inventory == 0
    assert res.scenario.stockout is True
    assert res.scenario.ending_inventory == -100

def test_combined_scenario():
    initial_inv = 100
    demands = [10] * 10
    inbounds = [0, 0, 0, 0, 100, 0, 0, 0, 0, 0]
    start_date = datetime.date(2026, 8, 10)
    
    sc1 = ScenarioEvent(type="supplier_delay", delay_days=5)
    sc2 = ScenarioEvent(type="demand_change", demand_multiplier=2.0)
    
    res = SimulationEngine.run_simulation(
        initial_inv, demands, inbounds, start_date, [sc1, sc2]
    )
    
    # Baseline: demand=100, inbound=100, inv=100 -> no stockout
    assert res.baseline.stockout is False
    
    # Scenario: demand=200, inbound arrives day 10. Runs out on day 5.
    assert res.scenario.stockout is True
    assert "Expedite inbound shipment" in res.recommendations
