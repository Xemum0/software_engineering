import sqlite3

# Database class to handle SQLite interactions
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
                insert_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')

    def add_expense(self, name, price):
        with self.connection:
            self.connection.execute('INSERT INTO expenses (name, price) VALUES (?, ?)', (name, price))

    def get_expenses(self):
        with self.connection:
            return self.connection.execute('SELECT * FROM expenses').fetchall()

    def delete_expense(self, expense_id):
        with self.connection:
            self.connection.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
