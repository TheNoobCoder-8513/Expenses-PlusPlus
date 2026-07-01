import sqlite3
from datetime import date, time
import slint


DB_NAME = "Expenses.db"

def init_db():
    """Creates the database and tables with correct strict data types."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                target_date TEXT NOT NULL,  -- Stored as 'YYYY-MM-DD'
                target_time TEXT NOT NULL,  -- Stored as 'HH:MM:SS'
                total REAL NOT NULL,        -- Numeric currency (e.g., 1200.50)
                saved REAL NOT NULL DEFAULT 0.0
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                record_date TEXT NOT NULL,  -- Stored as 'YYYY-MM-DD'
                record_time TEXT NOT NULL,  -- Stored as 'HH:MM:SS'
                category TEXT NOT NULL,
                amount REAL NOT NULL        -- Numeric currency (e.g., 4.50)
            )
        """)
        
        conn.commit()
    print("Database safely initialized with native-mapped types.")


def seed_mock_data():
    """Seeds the database with multiple goals and various multi-category daily records."""
    print("Seeding mock data...")
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # Optional: Clear existing data so you don't keep duplicating on every run
        cursor.execute("DELETE FROM goals")
        cursor.execute("DELETE FROM records")
        
        # 1. Adding Multiple Goals
        mock_goals = [
            ("Emergency Fund", date(2026, 12, 31).isoformat(), time(23, 59, 59).isoformat(), 5000.00, 1200.00),
            ("New Laptop", date(2026, 9, 15).isoformat(), time(12, 0, 0).isoformat(), 1500.00, 450.00),
            ("Vacation Trip", date(2027, 0, 1).isoformat() if 0 else "2027-06-01", time(9, 0, 0).isoformat(), 3000.00, 0.00)
        ]
        
        cursor.executemany("""
            INSERT INTO goals (name, target_date, target_time, total, saved)
            VALUES (?, ?, ?, ?, ?)
        """, mock_goals)
        
        # 2. Adding Multiple Records (Same Month, Same Day variations)
        mock_records = [
            # --- DAY 1: June 15, 2026 (Multiple items, different times & categories) ---
            ("Morning Latte", date(2026, 6, 15).isoformat(), time(8, 30, 0).isoformat(), "Food & Drinks", 5.50),
            ("Uber to Office", date(2026, 6, 15).isoformat(), time(9, 15, 0).isoformat(), "Transportation", 18.75),
            ("Office Lunch Deal", date(2026, 6, 15).isoformat(), time(13, 0, 0).isoformat(), "Food & Drinks", 14.20),
            ("Electricity Bill", date(2026, 6, 15).isoformat(), time(16, 45, 0).isoformat(), "Utilities", 85.00),
            ("Cinema Ticket", date(2026, 6, 15).isoformat(), time(20, 15, 0).isoformat(), "Entertainment", 16.50),
            
            # --- DAY 2: June 16, 2026 (Same month, next day) ---
            ("Weekly Groceries", date(2026, 6, 16).isoformat(), time(11, 0, 0).isoformat(), "Groceries", 112.40),
            ("Gym Membership", date(2026, 6, 16).isoformat(), time(14, 30, 0).isoformat(), "Health & Fitness", 45.00),
            
            # --- DAY 3: July 01, 2026 (Different Month) ---
            ("Monthly Rent", date(2026, 7, 1).isoformat(), time(0, 5, 0).isoformat(), "Housing", 1200.00),
            ("Streaming Subscription", date(2026, 7, 1).isoformat(), time(6, 0, 0).isoformat(), "Entertainment", 14.99)
        ]
        
        cursor.executemany("""
            INSERT INTO records (name, record_date, record_time, category, amount)
            VALUES (?, ?, ?, ?, ?)
        """, mock_records)
        
        conn.commit()
    print("Mock data successfully injected!")


def get_total_balance_from_db():
    """Fetches the calculated total from your SQLite ledger."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(amount) FROM records")
            balance = cursor.fetchone()[0]
            return balance if balance else 0.0
    except Exception as e:
        print(f"Database error: {e}")
        return 0.0
    

def main():
    ui = slint.load_file("UI/UI.slint")

    class ExpenseApp(ui.UI):
        
        @slint.callback(global_name="Glue")
        def get_TotalAmount(self):
            try:
                with sqlite3.connect(DB_NAME) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT SUM(amount) FROM records")
                    balance = cursor.fetchone()[0]
                    balance = balance if balance is not None else 0.0
                return balance
            except sqlite3.Error:
                return 0.0

        @slint.callback(global_name="Glue")
        def get_FrozenAmount(self):
            try:
                with sqlite3.connect(DB_NAME) as conn:
                    cursor = conn.cursor()
                    # Sums up the 'saved' column from your goals table
                    cursor.execute("SELECT SUM(saved) FROM goals")
                    total_saved = cursor.fetchone()[0]
                    return float(total_saved) if total_saved is not None else 0.0
            except sqlite3.Error:
                return 0.0
        
        
        
        @slint.callback(global_name="Glue")
        def get_Goals(self):
            slint_goals_list = []
            try:
                with sqlite3.connect(DB_NAME) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT name, target_date, target_time, total, saved FROM goals")
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        goal_struct = {
                            "name": str(row[0]),
                            "date": str(row[1]),
                            "time": str(row[2]),
                            "total": float(row[3]),  # Passed as a raw float
                            "saved": float(row[4])   # Passed as a raw float
                        }
                        slint_goals_list.append(goal_struct)
                return slint.ListModel(slint_goals_list)
            except sqlite3.Error as e:
                print(f"Database error fetching goals: {e}")
                return slint.ListModel([])

        @slint.callback(global_name="Glue")
        def get_Records(self):
            records_list = []
            try:
                with sqlite3.connect(DB_NAME) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT name, record_date, record_time, category, amount 
                        FROM records 
                        ORDER BY record_date DESC, record_time DESC
                    """)
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        record_struct = {
                            "name": str(row[0]),
                            "date": str(row[1]),
                            "time": str(row[2]),
                            "category": str(row[3]),
                            "amount": float(row[4])  
                        }
                        records_list.append(record_struct)
                
                return slint.ListModel(records_list)
                
            except sqlite3.Error as e:
                print(f"Database error fetching records: {e}")
                return slint.ListModel([])

    app = ExpenseApp()
    print("UI is up and running connected to SQLite backend.")
    app.run()


if __name__ == "__main__":
    # init_db()
    # seed_mock_data()

    main()