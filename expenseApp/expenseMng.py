# Manager class to handle the logic of managing expenses
class ExpenseManager:
    def __init__(self, db):
        self.db = db

    def add_expense(self, name, price,date):
        if name and self.is_valid_price(price):
            self.db.add_expense(name, float(price),date)
            return True
        return False

    def get_expenses(self):
        return self.db.get_expenses()

    def delete_expense(self, expense_id):
        self.db.delete_expense(expense_id)

    def get_expenses_in_duration(self,start_date,end_date):
        self.db.get_expenses_in_duration(start_date,end_date)
    def is_valid_price(self, price):
        try:
            float(price)
            return True
        except ValueError:
            return False
