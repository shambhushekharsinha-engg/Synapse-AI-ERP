import math

class InventoryMath:
    @staticmethod
    def calculate_safety_stock(z_score: float, demand_std_dev: float, lead_time_days: int) -> float:
        """
        Safety Stock = Z * (Demand_Std_Dev * sqrt(Lead_Time))
        Assumes demand variability is measured at the daily level and lead time is expressed in days.
        """
        if lead_time_days < 0 or demand_std_dev < 0:
            raise ValueError("Lead time and demand standard deviation must be non-negative.")
        return z_score * demand_std_dev * math.sqrt(lead_time_days)

    @staticmethod
    def calculate_reorder_point(average_daily_demand: float, lead_time_days: int, safety_stock: float) -> float:
        """
        Reorder Point = (Average Daily Demand * Lead Time) + Safety Stock
        """
        return (average_daily_demand * lead_time_days) + safety_stock

    @staticmethod
    def calculate_eoq(annual_demand: float, ordering_cost: float, holding_cost: float) -> float:
        """
        Economic Order Quantity = sqrt((2 * Annual_Demand * Ordering_Cost) / Holding_Cost)
        """
        if holding_cost <= 0:
            raise ValueError("Holding cost must be greater than zero to calculate EOQ.")
        if annual_demand < 0 or ordering_cost < 0:
            raise ValueError("Demand and Ordering cost must be non-negative.")
        
        return math.sqrt((2 * annual_demand * ordering_cost) / holding_cost)

    @staticmethod
    def get_z_score(service_level: float) -> float:
        """
        Helper to map common service levels to Z-scores.
        """
        mapping = {
            0.90: 1.28,
            0.95: 1.65,
            0.975: 1.96,
            0.99: 2.33
        }
        # Approximate matching for standard levels
        for level, z in mapping.items():
            if math.isclose(service_level, level, abs_tol=0.01):
                return z
        
        # Fallback to 95% if not standard
        return 1.65
