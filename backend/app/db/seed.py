import random
from app.db.session import SessionLocal
from app.models.domain import Product, Warehouse

def seed_db():
    db = SessionLocal()
    try:
        # Seed Products
        products = [
            Product(sku="PRD-001", name="Industrial Widget A", category="Components", unit_price=25.50, lead_time_days=5),
            Product(sku="PRD-002", name="Steel Beam B", category="Raw Materials", unit_price=120.00, lead_time_days=14),
            Product(sku="PRD-003", name="Microcontroller X", category="Electronics", unit_price=15.75, lead_time_days=30),
        ]
        
        # Check if already seeded
        if not db.query(Product).first():
            db.add_all(products)
            db.commit()
            print("Seeded Products")
            
        # Seed Warehouses
        warehouses = [
            Warehouse(name="Central Hub", location="New York, NY", capacity=50000),
            Warehouse(name="West Coast Dist", location="Los Angeles, CA", capacity=35000),
        ]
        
        if not db.query(Warehouse).first():
            db.add_all(warehouses)
            db.commit()
            print("Seeded Warehouses")
            
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting database seed...")
    seed_db()
    print("Seeding complete.")
