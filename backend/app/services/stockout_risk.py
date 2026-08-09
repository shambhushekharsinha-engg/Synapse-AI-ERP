from typing import List, Optional
from datetime import datetime, timedelta

class StockoutRiskService:
    @staticmethod
    def calculate_risk(
        product_id: int,
        current_inventory: float,
        forecast: List[dict], # List of {"date": "YYYY-MM-DD", "predicted_demand": float}
        planned_inbound: float,
        start_date: datetime
    ) -> dict:
        """
        Determines deterministic stockout risk by projecting inventory.
        """
        projected_inventory = current_inventory
        stockout_expected = False
        expected_stockout_date = None
        total_demand = 0.0
        
        # We assume planned_inbound arrives immediately for simplicity in MVP,
        # but in a real system we'd parse expected arrival dates.
        projected_inventory += planned_inbound
        
        for fp in forecast:
            demand = fp['predicted_demand']
            total_demand += demand
            projected_inventory -= demand
            
            if projected_inventory < 0 and not stockout_expected:
                stockout_expected = True
                expected_stockout_date = fp['date']
                
        # Risk categorization
        if stockout_expected:
            risk_level = "HIGH"
        elif projected_inventory < (total_demand * 0.2): # Less than 20% buffer remaining
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
            
        return {
            "product_id": product_id,
            "stockout_risk": risk_level,
            "stockout_expected": stockout_expected,
            "expected_stockout_date": str(expected_stockout_date) if expected_stockout_date else None,
            "forecast_horizon_days": len(forecast),
            "current_inventory": current_inventory,
            "forecasted_demand": round(total_demand, 2),
            "planned_inbound": planned_inbound
        }
