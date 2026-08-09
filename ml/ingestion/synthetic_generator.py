import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import os

class SyntheticERPGenerator:
    def __init__(self, seed: int = 42, num_products: int = 50, num_warehouses: int = 3, days: int = 365):
        self.seed = seed
        self.num_products = num_products
        self.num_warehouses = num_warehouses
        self.days = days
        np.random.seed(self.seed)
        
    def generate_products(self):
        return pd.DataFrame({
            "product_id": range(1, self.num_products + 1),
            "sku": [f"SKU-{i:04d}" for i in range(1, self.num_products + 1)],
            "category": np.random.choice(["Electronics", "Raw Materials", "Components", "Packaging"], self.num_products),
            "base_price": np.random.uniform(10, 500, self.num_products).round(2),
            "lead_time_days": np.random.randint(2, 30, self.num_products)
        })

    def generate_warehouses(self):
        return pd.DataFrame({
            "warehouse_id": range(1, self.num_warehouses + 1),
            "name": [f"Warehouse {i}" for i in range(1, self.num_warehouses + 1)],
            "capacity": np.random.randint(10000, 100000, self.num_warehouses)
        })

    def generate_demand(self, products_df, warehouses_df):
        dates = [datetime.today().date() - timedelta(days=x) for x in range(self.days)]
        dates.reverse()
        
        records = []
        for d in dates:
            for _, p in products_df.iterrows():
                for _, w in warehouses_df.iterrows():
                    # Seasonal + trend + noise
                    day_of_year = d.timetuple().tm_yday
                    seasonality = np.sin(2 * np.pi * day_of_year / 365) * 10
                    base_demand = np.random.normal(50, 15)
                    demand = max(0, int(base_demand + seasonality))
                    
                    records.append({
                        "date": d,
                        "product_id": p["product_id"],
                        "warehouse_id": w["warehouse_id"],
                        "demand": demand,
                        "inventory_level": max(0, demand * np.random.uniform(1, 3)),
                        "stockout": 1 if demand > 0 and np.random.random() < 0.05 else 0
                    })
        return pd.DataFrame(records)

    def run(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        products = self.generate_products()
        warehouses = self.generate_warehouses()
        demand = self.generate_demand(products, warehouses)
        
        # Validation checks
        assert demand.isnull().sum().sum() == 0, "Nulls found in synthetic data"
        assert (demand['demand'] < 0).sum() == 0, "Negative demand found"
        
        # Save
        demand.to_csv(f"{output_dir}/synthetic_demand.csv", index=False)
        
        # Manifest
        manifest = {
            "dataset_version": "v1.0.0",
            "source": "synthetic",
            "random_seed": self.seed,
            "generated_at": datetime.utcnow().isoformat(),
            "rows": len(demand),
            "features": len(demand.columns),
            "date_start": str(demand['date'].min()),
            "date_end": str(demand['date'].max())
        }
        with open(f"{output_dir}/manifest.json", "w") as f:
            json.dump(manifest, f, indent=4)
            
        print(f"Generated synthetic data: {len(demand)} rows.")

if __name__ == "__main__":
    generator = SyntheticERPGenerator(days=100) # Shorter for quick test
    generator.run("ml/data/synthetic")
