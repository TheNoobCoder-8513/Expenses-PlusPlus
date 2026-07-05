import sqlite3
from datetime import date, time, datetime
import slint
import random
from datetime import timedelta


DB_NAME = "Data/Expenses.db"

INCOME_SOURCES = [
    ("Freelance Gig", "Side Hustle"),
    ("Salary Payout", "Salary"),
    ("Sold Old Items", "Misc"),
    ("Dividend Payout", "Investments")
]

EXPENSES = [
    ("Morning Latte", "Food & Drinks"),
    ("Uber to Office", "Transportation"),
    ("Electricity Bill", "Utilities"),
    ("Weekly Groceries", "Groceries"),
    ("Baabu bhai ke chhole", "Food & Drinks"),
    ("Netflix Subscription", "Entertainment"),
    ("Amazon Order", "Shopping"),
    ("Gym Membership", "Health"),
    ("Dinner with Friends", "Dining"),
    ("Gas Station", "Transportation"),
    ("Evening Snacks", "Snacks"),
    ("Medicine", "Health")
]

def generate_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Clear existing data to avoid cluttering your tests
    print("Clearing old records...")
    cursor.execute("DROP TABLE IF EXISTS records")
    
    cursor.execute("""
        CREATE TABLE records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            record_date TEXT NOT NULL,
            record_time TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)

    # 2. Add an initial opening balance on Day 1
    cursor.execute("""
        INSERT INTO records (name, record_date, record_time, category, amount)
        VALUES (?, ?, ?, ?, ?)
    """, ("Initial Balance", "2026-06-01", "00:00:01", "Opening Balance", 100000.0))

    # 3. Generate data for every day of June 2026
    start_date = datetime(2026, 6, 1)
    
    print("Generating 4-7 purchases per day for June 2026...")
    for day_offset in range(30):
        current_date = start_date + timedelta(days=day_offset)
        date_str = current_date.strftime("%Y-%m-%d")
        
        # Determine a random number of transactions (4 to 7) for this specific day
        num_transactions = random.randint(4, 7)
        
        for _ in range(num_transactions):
            # Generate a random timestamp throughout the day
            hour = random.randint(7, 22)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
            
            # Most daily events are expenses, occasionally an income stream drops in
            if random.random() < 0.12:  # 12% chance of an income entry
                name, category = random.choice(INCOME_SOURCES)
                # Keep amounts clean like 150.0 or 2450.50
                amount = round(random.uniform(50.0, 5000.0), 2)
            else:
                name, category = random.choice(EXPENSES)
                # Keep expenses negative based on your database design rules
                amount = -round(random.uniform(5.0, 150.0), 2)
                
            cursor.execute("""
                INSERT INTO records (name, record_date, record_time, category, amount)
                VALUES (?, ?, ?, ?, ?)
            """, (name, date_str, time_str, category, amount))

    conn.commit()
    
    # Verify the count
    cursor.execute("SELECT COUNT(*) FROM records")
    total_rows = cursor.fetchone()[0]
    conn.close()
    
    print(f"Success! Inserted {total_rows} total rows into the database.")

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

        @slint.callback(global_name="Glue")
        def add_Goals(self, name: str, total: str, saved: str) -> bool:
            try:
                # Generate current date (YYYY-MM-DD) and time (HH:MM:SS) dynamically
                now = datetime.now()
                current_date = now.strftime("%Y-%m-%d")
                current_time = now.strftime("%H:%M:%S")

                with sqlite3.connect(DB_NAME) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO goals (name, target_date, target_time, total, saved)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        str(name),
                        current_date,
                        current_time,
                        float(total),
                        float(saved)
                    ))
                    conn.commit()
                return True
            except (sqlite3.Error, ValueError) as e:
                print(f"Failed to add goal: {e}")
                return False
            
        @slint.callback(global_name="Glue")
        def update_Goals(self, name: str, total: str, saved: str) -> bool:
            try:
                now = datetime.now()
                current_date = now.strftime("%Y-%m-%d")
                current_time = now.strftime("%H:%M:%S")

                with sqlite3.connect(DB_NAME) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE goals 
                        SET target_date = ?, 
                            target_time = ?, 
                            total = ?, 
                            saved = ?
                        WHERE name = ?
                    """, (
                        current_date,
                        current_time,
                        float(total),
                        float(saved),
                        str(name)
                    ))
                    conn.commit()
                    
                    return cursor.rowcount > 0
            except (sqlite3.Error, ValueError) as e:
                print(f"Failed to update goal: {e}")
                return False
            
        @slint.callback(global_name="Glue")
        def add_Records(self, name: str, category: str, record_type: str, amount: str) -> bool:
            try:
                now = datetime.now()
                current_date = now.strftime("%Y-%m-%d")
                current_time = now.strftime("%H:%M:%S")

                try:
                    parsed_amount = float(amount) if amount.strip() else 0.0
                except ValueError:
                    print("Invalid numeric text provided to add_Records.")
                    return False

                if record_type.lower() == "expense" and parsed_amount > 0:
                    parsed_amount = -parsed_amount

                with sqlite3.connect(DB_NAME) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO records (name, record_date, record_time, category, amount)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        str(name),
                        current_date,
                        current_time,
                        str(category),
                        parsed_amount
                    ))
                    conn.commit()
                return True

            except sqlite3.Error as e:
                print(f"Failed to add transaction record: {e}")
                return False



        @slint.callback(global_name="Glue")
        def get_RecordsForDate(self, year: int, month: int, day: int):
            records_list = []

            target_date_str = f"{year:04d}-{month:02d}-{day:02d}"
            
            try:
                with sqlite3.connect(DB_NAME) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT name, amount 
                        FROM records 
                        WHERE record_date = ?
                        ORDER BY record_time ASC
                    """, (target_date_str,))
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        name = str(row[0])
                        amount = float(row[1])
                        
                        # Apply your currency formatting rule directly before sending it over
                        formatted_amount = f"{amount:.2f}" if amount >= 0 else f"-{abs(amount):.2f}"
                        
                        # Structure matching Slint's expected { lval: string, rval: string }
                        records_list.append({
                            "lval": name,
                            "rval": formatted_amount
                        })
                        
                # Wrap into a dynamic ListModel so Slint triggers an instant visual re-render
                return slint.ListModel(records_list)
                
            except sqlite3.Error as e:
                print(f"Database error during calendar query: {e}")
                return slint.ListModel([])


        @slint.callback(global_name="Glue")
        def get_TodaysRecords(self):
            records_list = []
            
            # Automatically get today's date formatted as YYYY-MM-DD
            today_str = datetime.now().strftime("%Y-%m-%d")
            
            try:
                with sqlite3.connect(DB_NAME) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT name, amount 
                        FROM records 
                        WHERE record_date = ?
                        ORDER BY record_time DESC
                    """, (today_str,))
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        name = str(row[0])
                        amount = float(row[1])
                        
                        # Formatting currency for your UI text layout
                        formatted_amount = f"{amount:.2f}" if amount >= 0 else f"-{abs(amount):.2f}"
                        
                        records_list.append({
                            "lval": name,
                            "rval": formatted_amount
                        })
                        
                return slint.ListModel(records_list)
                
            except sqlite3.Error as e:
                print(f"Database error fetching today's records: {e}")
                return slint.ListModel([])

        @slint.callback(global_name="Glue")
        def get_MonthlyCategoryTotals(self, year: int, month: int):
            category_totals = []
            
            # Format the match pattern to target all dates in that specific month (e.g., "2026-06-%")
            month_pattern = f"{year:04d}-{month:02d}-%"
            
            try:
                with sqlite3.connect(DB_NAME) as conn:
                    cursor = conn.cursor()
                    # Sums the amount grouped by category, ordering by highest total expense/income first
                    cursor.execute("""
                        SELECT category, SUM(amount) as total
                        FROM records 
                        WHERE record_date LIKE ?
                        GROUP BY category
                        ORDER BY total ASC
                    """, (month_pattern,))
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        category = str(row[0])
                        total_amount = float(row[1])
                        
                        # Convert to string format for the UI table
                        formatted_total = f"{total_amount:.2f}" if total_amount >= 0 else f"-{abs(total_amount):.2f}"
                        
                        category_totals.append({
                            "lval": category,       # The Category Name
                            "rval": formatted_total # The Aggregated Total
                        })
                        
                return slint.ListModel(category_totals)
                
            except sqlite3.Error as e:
                print(f"Database error fetching monthly categories: {e}")
                return slint.ListModel([])

        @slint.callback(global_name="Glue")
        def get_CurrentDateBreakdown(self):
            # Automatically extracts the active system date components
            now = datetime.now()
            
            return {
                "year": int(now.year),
                "month": int(now.month),
                "date": int(now.day)
            }

    app = ExpenseApp()
    print("UI is up and running connected to SQLite backend.")
    app.run()


if __name__ == "__main__":
    # init_db()
    # seed_mock_data()
    # generate_data()
    main()