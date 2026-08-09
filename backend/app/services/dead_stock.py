class DeadStockService:
    @staticmethod
    def evaluate(
        product_id: int,
        inventory_units: float,
        days_since_last_sale: int,
        forecast_demand_30d: float,
        # Configurable thresholds
        stale_days_threshold: int = 90,
        low_forecast_threshold: float = 10.0,
        min_inventory_threshold: float = 1.0
    ) -> dict:
        """
        Determines dead stock based on configurable business rules rather than strict zero.
        """
        is_dead = False
        reason = "Healthy inventory."
        
        if inventory_units >= min_inventory_threshold:
            if days_since_last_sale >= stale_days_threshold:
                if forecast_demand_30d <= low_forecast_threshold:
                    is_dead = True
                    reason = "High inventory with persistently low demand and no recent sales."
                else:
                    reason = "Stale inventory, but upcoming forecast shows recovery."
            else:
                if forecast_demand_30d <= low_forecast_threshold:
                    reason = "Recent sales exist, but upcoming forecast is very weak."
        else:
            reason = "Zero or negligible inventory, cannot be dead stock."
            
        return {
            "product_id": product_id,
            "is_dead_stock": is_dead,
            "inventory_units": inventory_units,
            "forecast_demand_30d": round(forecast_demand_30d, 2),
            "days_since_last_sale": days_since_last_sale,
            "reason": reason
        }
