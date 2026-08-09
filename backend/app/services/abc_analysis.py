import pandas as pd
from typing import List
from app.schemas.inventory_intelligence import ABCClassificationResponse

class ABCAnalysisService:
    @staticmethod
    def classify_products(products_data: List[dict]) -> List[ABCClassificationResponse]:
        """
        Classifies products into A, B, and C categories based on annual consumption value.
        If unit cost is unavailable, sales revenue is used as a proxy.
        
        products_data should be a list of dicts with:
        - product_id
        - sku
        - annual_demand
        - unit_cost (or unit_price)
        """
        if not products_data:
            return []
            
        df = pd.DataFrame(products_data)
        
        # Calculate consumption value
        df['annual_consumption_value'] = df['annual_demand'] * df.get('unit_cost', df.get('unit_price', 0))
        
        # Sort descending by consumption value
        df = df.sort_values(by='annual_consumption_value', ascending=False).reset_index(drop=True)
        
        # Calculate cumulative percentage
        total_value = df['annual_consumption_value'].sum()
        if total_value == 0:
            df['cumulative_percentage'] = 0.0
        else:
            df['cumulative_percentage'] = (df['annual_consumption_value'].cumsum() / total_value) * 100
            
        def assign_class(cum_pct: float) -> str:
            if cum_pct <= 80.0:
                return 'A'
            elif cum_pct <= 95.0:
                return 'B'
            else:
                return 'C'
                
        df['abc_class'] = df['cumulative_percentage'].apply(assign_class)
        
        results = []
        for _, row in df.iterrows():
            results.append(ABCClassificationResponse(
                product_id=row['product_id'],
                sku=row['sku'],
                annual_consumption_value=round(row['annual_consumption_value'], 2),
                abc_class=row['abc_class'],
                cumulative_percentage=round(row['cumulative_percentage'], 2)
            ))
            
        return results
