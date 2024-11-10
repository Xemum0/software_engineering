import sqlite3

class Database:
    def __init__(self, db_name="expenses.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute('''CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                insert_date DATE NOT NULL
            )''')

    def add_expense(self, name, price, date):
        with self.connection:
            self.connection.execute('INSERT INTO expenses (name, price, insert_date) VALUES (?, ?, ?)', 
                                 (name, price, date))

    def get_expenses(self, page=1, items_per_page=10):
        offset = (page - 1) * items_per_page
        with self.connection:
            return self.connection.execute(
                'SELECT * FROM expenses ORDER BY insert_date DESC LIMIT ? OFFSET ?', 
                (items_per_page, offset)
            ).fetchall()
    
    def get_total_expenses_count(self):
        with self.connection:
            return self.connection.execute('SELECT COUNT(*) FROM expenses').fetchone()[0]
    
    def get_expenses_in_duration(self, start_date, end_date, page=1, items_per_page=10):
        offset = (page - 1) * items_per_page
        with self.connection:
            return self.connection.execute(
                '''SELECT * FROM expenses 
                   WHERE insert_date BETWEEN ? AND ? 
                   ORDER BY insert_date DESC 
                   LIMIT ? OFFSET ?''',
                (start_date, end_date, items_per_page, offset)
            ).fetchall()

    def delete_expense(self, expense_id):
        with self.connection:
            self.connection.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
