import sys
from Db import Database
from expenseMng import ExpenseManager
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QLineEdit, QLabel, QPushButton, QMenuBar, QMenu, QMessageBox
)
from PyQt5.QtCore import Qt

# Main UI class
class ExpenseUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.manager = ExpenseManager(self.db)

        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 600, 300)

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

        add_button = QPushButton("Add Expense")
        add_button.clicked.connect(self.add_expense)

        top_panel.addWidget(expense_label)
        top_panel.addWidget(self.expense_input)
        top_panel.addWidget(price_label)
        top_panel.addWidget(self.price_input)
        top_panel.addWidget(add_button)

        # Table to display expenses
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Expense", "Price", "Delete"])
        layout.addWidget(self.table)

        # Bottom panel for total
        total_label = QLabel("Total:")
        self.total_value = QLabel("0.00")
        total_layout = QHBoxLayout()
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_value)
        layout.addLayout(total_layout)

        # Load initial data from the database
        self.load_expenses()

    def load_expenses(self):
        self.table.setRowCount(0)
        expenses = self.manager.get_expenses()
        for expense_id, name, price in expenses:
            self.add_expense_row(expense_id, name, price)
        self.update_total()

    def add_expense_row(self, expense_id, name, price):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(name))
        self.table.setItem(row_position, 1, QTableWidgetItem(f"{price:.2f}"))

        # Create delete button
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_expense(expense_id, row_position))
        self.table.setCellWidget(row_position, 2, delete_button)

    def add_expense(self):
        expense_name = self.expense_input.text().strip()
        price_text = self.price_input.text().strip()

        if self.manager.add_expense(expense_name, price_text):
            self.load_expenses()
            self.expense_input.clear()
            self.price_input.clear()
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid expense name and price.")

    def delete_expense(self, expense_id, row_position):
        self.manager.delete_expense(expense_id)
        self.table.removeRow(row_position)
        self.update_total()

    def update_total(self):
        total = 0.0
        for row in range(self.table.rowCount()):
            price_item = self.table.item(row, 1)
            if price_item:
                total += float(price_item.text())
        self.total_value.setText(f"{total:.2f}")
