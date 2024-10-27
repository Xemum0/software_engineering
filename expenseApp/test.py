import sys
##########

import pandas as pd
import matplotlib.pyplot as plt


###########
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
    def init(self):
        super().init()
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
#########
        export = QPushButton("Export")
        export.clicked.connect(self.export)
        top_panel.addWidget(export)

    def export(self):
        data={
        "name":[],
        "price":[],
        "insert date":[]
        }
        expenses = self.manager.get_expenses()
        for expense_id, name, price,insert_date in expenses:
            data["name"]=name
            data["price"]=price
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
    
    
##########

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