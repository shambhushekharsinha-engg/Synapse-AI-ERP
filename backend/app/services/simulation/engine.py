from typing import List, Dict, Tuple
import datetime
from app.schemas.simulation import ScenarioEvent, SimulationState, SimulationImpact, SimulationResponse

class SimulationEngine:
    @staticmethod
    def project_inventory(
        initial_inventory: float,
        daily_demands: List[float],
        daily_inbounds: List[float],
        start_date: datetime.date
    ) -> SimulationState:
        """
        Projects inventory day-by-day and returns the state (stockout info and ending inventory).
        """
        inv = initial_inventory
        stockout = False
        stockout_date = None
        
        for i, (demand, inbound) in enumerate(zip(daily_demands, daily_inbounds)):
            inv += inbound
            inv -= demand
            if inv < 0 and not stockout:
                stockout = True
                stockout_date = start_date + datetime.timedelta(days=i)
                
        return SimulationState(
            stockout=stockout,
            stockout_date=str(stockout_date) if stockout_date else None,
            ending_inventory=inv
        )

    @staticmethod
    def apply_scenarios(
        scenarios: List[ScenarioEvent],
        daily_demands: List[float],
        daily_inbounds: List[float]
    ) -> Tuple[List[float], List[float], str]:
        """
        Applies non-destructive transformations to the demand and inbound arrays based on scenarios.
        Returns the modified arrays and a string identifying the scenario type(s).
        """
        mod_demands = list(daily_demands)
        mod_inbounds = list(daily_inbounds)
        types = []
        
        for sc in scenarios:
            types.append(sc.type)
            if sc.type == "demand_change":
                multiplier = sc.demand_multiplier or 1.0
                mod_demands = [d * multiplier for d in mod_demands]
                
            elif sc.type == "supply_reduction":
                multiplier = sc.supply_multiplier or 1.0
                mod_inbounds = [ib * multiplier for ib in mod_inbounds]
                
            elif sc.type == "supplier_delay":
                delay = sc.delay_days or 0
                # Shift inbounds to the right by `delay` days
                if delay > 0:
                    mod_inbounds = [0.0] * delay + mod_inbounds[:-delay] if len(mod_inbounds) > delay else [0.0] * len(mod_inbounds)
                    
        type_str = "combined" if len(scenarios) > 1 else (types[0] if types else "baseline")
        return mod_demands, mod_inbounds, type_str

    @staticmethod
    def generate_recommendations(baseline: SimulationState, scenario: SimulationState, scenario_types: List[str]) -> List[str]:
        recs = []
        if scenario.stockout and not baseline.stockout:
            if "supplier_delay" in scenario_types:
                recs.append("Expedite inbound shipment")
                recs.append("Evaluate alternate supplier")
            if "demand_change" in scenario_types:
                recs.append("Increase replenishment quantity")
        elif scenario.stockout and baseline.stockout:
            if scenario.ending_inventory < baseline.ending_inventory:
                recs.append("Situation worsens: Immediate emergency replenishment required.")
        return recs or ["No immediate action required"]

    @staticmethod
    def run_simulation(
        initial_inventory: float,
        daily_demands: List[float],
        daily_inbounds: List[float],
        start_date: datetime.date,
        scenarios: List[ScenarioEvent]
    ) -> SimulationResponse:
        
        # 1. Baseline
        baseline_state = SimulationEngine.project_inventory(
            initial_inventory, daily_demands, daily_inbounds, start_date
        )
        
        # 2. Modify arrays
        mod_demands, mod_inbounds, type_str = SimulationEngine.apply_scenarios(
            scenarios, daily_demands, daily_inbounds
        )
        
        # 3. Scenario state
        scenario_state = SimulationEngine.project_inventory(
            initial_inventory, mod_demands, mod_inbounds, start_date
        )
        
        # 4. Impact calculation
        # If ending inventory is less than 0, the magnitude is the shortage
        baseline_shortage = max(0, -baseline_state.ending_inventory)
        scenario_shortage = max(0, -scenario_state.ending_inventory)
        
        additional_shortage = scenario_shortage - baseline_shortage
        inventory_delta = scenario_state.ending_inventory - baseline_state.ending_inventory
        
        impact = SimulationImpact(
            additional_shortage_units=round(additional_shortage, 2),
            inventory_delta=round(inventory_delta, 2)
        )
        
        # 5. Recommendations
        recs = SimulationEngine.generate_recommendations(baseline_state, scenario_state, [s.type for s in scenarios])
        
        return SimulationResponse(
            scenario_type=type_str,
            baseline=baseline_state,
            scenario=scenario_state,
            impact=impact,
            recommendations=recs
        )
