import sqlite3
import random
from datetime import datetime, timedelta

def seed_database():
    conn = sqlite3.connect('erp_system.db')
    cursor = conn.cursor()

    # Clear existing data to avoid duplicates when re-running.
    cursor.execute("DELETE FROM Transactions;")
    cursor.execute("DELETE FROM Inventory;")
    cursor.execute("DELETE FROM Suppliers;")

    # 1. Insert Dummy Suppliers
    suppliers = [
        ('TechSource Electronics', 'orders@techsource.com', 5),
        ('Global Parts Inc.', 'restock@globalparts.com', 10),
        ('FastShip Logistics', 'supply@fastship.com', 3)
    ]
    cursor.executemany('''
        INSERT INTO Suppliers (Name, Contact_Email, Lead_Time_Days) 
        VALUES (?, ?, ?)
    ''', suppliers)

    # 2. Insert Dummy Inventory
    inventory = [
        ('ThinkPad Laptops', 45, 20, 1),
        ('Dell Monitors 24inch', 12, 15, 2),
        ('Mechanical Keyboards', 110, 30, 1),
        ('Server Racks', 4, 5, 3),
        ('Ergonomic Chairs', 8, 10, 2)
    ]
    cursor.executemany('''
        INSERT INTO Inventory (Item_Name, Current_Stock, Reorder_Threshold, Supplier_ID) 
        VALUES (?, ?, ?, ?)
    ''', inventory)

    # 3. Generate Messy Transactions for NLP and ML
    messy_strings = [
        "AMZN* RESTOCK #99283", 
        "UBER EATS 05/24 MEAL", 
        "STRIPE PAYOUT // TXN-992", 
        "OFFICE DEPOT * MISC CHARGE",
        "SALES REV - INVOICE 001",
        "SYSCO CORP CATERING"
    ]

    transactions = []
    base_date = datetime.now()

    # Generate 50 random transactions over the last 90 days
    for _ in range(50):
        random_days_ago = random.randint(1, 90)
        txn_date = (base_date - timedelta(days=random_days_ago)).strftime('%Y-%m-%d')
        raw_string = random.choice(messy_strings) + f" id:{random.randint(1000, 9999)}"
        amount = round(random.uniform(-500.0, 1500.0), 2) # Mix of expenses and revenue
        item_id = random.randint(1, 5) # Randomly link to one of our 5 items
        
        # NLP_Category is left as None (NULL) so your AI can fill it in Week 2!
        transactions.append((txn_date, raw_string, amount, None, item_id))

    cursor.executemany('''
        INSERT INTO Transactions (Transaction_Date, Raw_String, Amount, NLP_Category, Item_ID) 
        VALUES (?, ?, ?, ?, ?)
    ''', transactions)

    conn.commit()
    conn.close()
    
    print("Success! Database has been populated with dummy suppliers, inventory, and 50 messy transactions.")

if __name__ == "__main__":
    seed_database()