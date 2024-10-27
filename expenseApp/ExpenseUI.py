import sys
from Db import Database
from expenseMng import ExpenseManager
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QDateEdit,
    QLineEdit, QLabel, QPushButton, QMenuBar, QMenu, QMessageBox
)
from PyQt5.QtCore import Qt,QDate
import pandas as pd 
import matplotlib.pyplot as plt

# Main UI class
class ExpenseUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.manager = ExpenseManager(self.db)
        
        # Pagination settings
        self.items_per_page = 10
        self.current_page = 1
        self.total_pages = 1

        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 600, 400)  

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        # Top panel for adding expenses
        top_panel = QHBoxLayout()
        layout.addLayout(top_panel)

        expense_label = QLabel("Expense:")
        self.expense_input = QLineEdit()
        self.expense_input.setFixedWidth(150)

        price_label = QLabel("Price:")
        self.price_input = QLineEdit()
        self.price_input.setFixedWidth(100)
        date_label = QLabel("Date:")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())

        add_button = QPushButton("Add Expense")
        add_button.clicked.connect(self.add_expense)
        
        
        export = QPushButton("Export")
        export.clicked.connect(self.export)
        top_panel.addWidget(export)
        
        
        top_panel.addWidget(expense_label)
        top_panel.addWidget(self.expense_input)
        top_panel.addWidget(price_label)
        top_panel.addWidget(self.price_input)
        top_panel.addWidget(date_label)
        top_panel.addWidget(self.date_input)
        top_panel.addWidget(add_button)

        # Table to display expenses
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Expense", "Price", "Delete"])
        layout.addWidget(self.table)

        # Pagination controls
        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_page)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.page_label = QLabel("Page 1 of 1")
        
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_button)
        pagination_layout.addStretch()
        
        layout.addLayout(pagination_layout)

        # Bottom panel for total
        total_label = QLabel("Total:")
        self.total_value = QLabel("0.00")
        total_layout = QHBoxLayout()
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_value)
        layout.addLayout(total_layout)

        # Load initial data from the database
        self.load_expenses()
    def export(self):
        data={
        "name":[],
        "price":[],
        "insert date":[]
        }
        expenses = self.manager.get_expenses()
        for expense_id, name, price,insert_date in expenses:
            data["name"].append(name)
            data["price"].append(price)
            data['insert date']=insert_date
        df = pd.DataFrame(data)

# Create a figure and axis
        fig, ax = plt.subplots(figsize=(8, 4))  # Set the size of the PDF

# Hide axes
        ax.axis('tight')
        ax.axis('off')

# Create a table from the DataFrame
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

# Save the table as a PDF
        plt.savefig('output_table.pdf', bbox_inches='tight')
        plt.close()
    
    def load_expenses(self):
        """
        Load expenses with pagination:
        1. Calculate total pages based on total items and items per page
        2. Get subset of expenses for current page
        3. Update pagination controls
        4. Display current page's expenses in table
        """
        self.table.setRowCount(0)
        
        # Get total count of expenses and calculate total pages
        all_expenses = self.manager.get_expenses()
        total_items = len(all_expenses)
        self.total_pages = max(1, (total_items + self.items_per_page - 1) // self.items_per_page)
        
        # Adjust current page if it's out of bounds
        self.current_page = min(max(1, self.current_page), self.total_pages)
        
        # Calculate start and end indices for current page
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        
        # Get expenses for current page
        current_page_expenses = all_expenses[start_idx:end_idx]
        
        # Update table with current page's expenses
        for expense_id, name, price,date in current_page_expenses:
            self.add_expense_row(expense_id, name, price,date)
            
        # Update pagination controls
        self.update_pagination_controls()
        self.update_total()

    def update_pagination_controls(self):
        """
        Update pagination controls state:
        1. Enable/disable Previous/Next buttons based on current page
        2. Update page label
        """
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < self.total_pages)
        self.page_label.setText(f"Page {self.current_page} of {self.total_pages}")

    def previous_page(self):
        """Handle previous page button click"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_expenses()

    def next_page(self):
        """Handle next page button click"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_expenses()

    def add_expense_row(self, expense_id, name, price,date):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(name))
        self.table.setItem(row_position, 1, QTableWidgetItem(f"{price:.2f}"))
        self.table.setItem(row_position, 2, QTableWidgetItem(date))
        # Create delete button
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_expense(expense_id, row_position))
        self.table.setCellWidget(row_position, 2, delete_button)

    def add_expense(self):
        expense_name = self.expense_input.text().strip()
        price_text = self.price_input.text().strip()
        date = self.date_label.text().strip()
        if self.manager.add_expense(expense_name, price_text,date):
            self.load_expenses()  # Will refresh with pagination
            self.expense_input.clear()
            self.price_input.clear()
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid expense name and price.")

    def delete_expense(self, expense_id, row_position):
        self.manager.delete_expense(expense_id)
        self.load_expenses()  # Reload all expenses with pagination instead of just removing the row

    def update_total(self):
        # Calculate total for all expenses, not just current page
        all_expenses = self.manager.get_expenses()
        total = sum(price for _, _, price in all_expenses)
        self.total_value.setText(f"{total:.2f}")