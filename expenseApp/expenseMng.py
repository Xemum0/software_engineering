class ExpenseManager:
    def __init__(self, db):
        self.db = db

    def add_expense(self, name, price, date):
        if name and self.is_valid_price(price):
            self.db.add_expense(name, float(price), date)
            return True
        return False

    def get_expenses(self, page=1, items_per_page=10):
        return self.db.get_expenses(page, items_per_page)

    def get_total_pages(self, items_per_page=10):
        total_items = self.db.get_total_expenses_count()
        return max(1, (total_items + items_per_page - 1) // items_per_page)

    def delete_expense(self, expense_id):
        self.db.delete_expense(expense_id)
    
    def get_expenses_in_duration(self, start_date, end_date, page=1, items_per_page=10):
        return self.db.get_expenses_in_duration(start_date, end_date, page, items_per_page)

    def is_valid_price(self, price):
        try:
            float(price)
            return True
        except ValueError:
            return False