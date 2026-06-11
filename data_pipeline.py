import sqlite3
import pandas as pd

def extract_data():
    # 1. Open the connection to your database
    conn = sqlite3.connect('erp_system.db')

    # 2. Query A: Get all transactions that need NLP categorization
    # We specifically look for rows where NLP_Category is NULL
    print("--- Fetching Unprocessed Transactions ---")
    unprocessed_query = "SELECT * FROM Transactions WHERE NLP_Category IS NULL;"
    
    # The Magic Command: This runs the SQL query and dumps the result into a Pandas DataFrame
    df_transactions = pd.read_sql_query(unprocessed_query, conn)
    
    # Display the first 5 rows
    print(df_transactions.head())
    print(f"\nTotal transactions to process: {len(df_transactions)}\n")

    # 3. Query B: Get Inventory that is running dangerously low
    # We use a JOIN here to grab the Supplier's email at the same time!
    print("--- Fetching Critical Inventory ---")
    low_stock_query = """
        SELECT i.Item_Name, i.Current_Stock, i.Reorder_Threshold, s.Name as Supplier_Name, s.Contact_Email
        FROM Inventory i
        JOIN Suppliers s ON i.Supplier_ID = s.Supplier_ID
        WHERE i.Current_Stock <= i.Reorder_Threshold;
    """
    
    df_low_stock = pd.read_sql_query(low_stock_query, conn)
    print(df_low_stock)

    # 4. Always close the connection when done
    conn.close()

if __name__ == "__main__":
    extract_data()