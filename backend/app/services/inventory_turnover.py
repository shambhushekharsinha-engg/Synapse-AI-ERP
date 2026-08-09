class InventoryTurnoverService:
    @staticmethod
    def calculate(
        product_id: int,
        cogs: float = None,
        revenue: float = None,
        average_inventory: float = 0.0
    ) -> dict:
        """
        Inventory Turnover = COGS / Average Inventory.
        If COGS is missing, Revenue is used as a proxy.
        """
        if average_inventory <= 0:
            return {
                "product_id": product_id,
                "turnover_ratio": 0.0,
                "calculation_method": "zero_inventory",
                "average_inventory": 0.0,
                "annual_cogs_or_revenue": 0.0
            }
            
        if cogs is not None and cogs > 0:
            ratio = cogs / average_inventory
            method = "cogs_based"
            val = cogs
        elif revenue is not None and revenue > 0:
            ratio = revenue / average_inventory
            method = "revenue_based_proxy"
            val = revenue
        else:
            ratio = 0.0
            method = "no_sales_data"
            val = 0.0
            
        return {
            "product_id": product_id,
            "turnover_ratio": round(ratio, 2),
            "calculation_method": method,
            "average_inventory": round(average_inventory, 2),
            "annual_cogs_or_revenue": round(val, 2)
        }
