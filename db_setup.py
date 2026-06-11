import sqlite3

def create_database():
    # 1. Connect to SQLite (This creates the file if it doesn't exist)
    conn = sqlite3.connect('erp_system.db')
    cursor = conn.cursor()

    print("Successfully connected to the database.")

    # 2. Create the Suppliers Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Suppliers (
        Supplier_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Contact_Email TEXT NOT NULL,
        Lead_Time_Days INTEGER
    )
    ''')

    # 3. Create the Inventory Table
    # Notice how Supplier_ID links back to the Suppliers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Inventory (
        Item_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Item_Name TEXT NOT NULL,
        Current_Stock INTEGER NOT NULL,
        Reorder_Threshold INTEGER NOT NULL,
        Supplier_ID INTEGER,
        FOREIGN KEY (Supplier_ID) REFERENCES Suppliers (Supplier_ID)
    )
    ''')

    # 4. Create the Transactions Table
    # The 'Category' column starts empty so your NLP model can fill it later
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Transactions (
        Transaction_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Transaction_Date DATE NOT NULL,
        Raw_String TEXT NOT NULL, 
        Amount REAL NOT NULL,
        NLP_Category TEXT, 
        Item_ID INTEGER,
        FOREIGN KEY (Item_ID) REFERENCES Inventory (Item_ID)
    )
    ''')

    # 5. Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    print("Database and tables successfully created! Check your folder for 'erp_system.db'.")

if __name__ == "__main__":
    create_database()