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

    def add_expense(self, name, price,date):
        with self.connection:
            self.connection.execute('INSERT INTO expenses (name, price,insert_date) VALUES (?, ?,?)', (name, price,date))

    def get_expenses(self):
        with self.connection:
            return self.connection.execute('SELECT * FROM expenses').fetchall()
    
    def get_expenses_in_duration(self,start_date,end_date):
        with self.connection:
            return self.connection.execute('SELECT * FROM expenses WHERE insert_date BETWEEN ? AND ?',(start_date,end_date)).fetchall()

    def delete_expense(self, expense_id):
        with self.connection:
            self.connection.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))