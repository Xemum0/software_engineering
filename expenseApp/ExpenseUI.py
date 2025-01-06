# Db.py and ExpenseManager.py remain the same as in previous version

# ExpenseUI.py
import sys
from Db import Database
from expenseMng import ExpenseManager
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QDateEdit, QLineEdit, QLabel, QPushButton, 
    QMenuBar, QMenu, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, QDate
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class ExpenseUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.manager = ExpenseManager(self.db)

        self.items_per_page = 10
        self.current_page = 1
        self.is_filtered = False

        # Apply stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QFrame {
                background-color: #3c3f41;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton {
                background-color: #4caf50;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                border: none;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #5c6e58;
            }
            QLineEdit, QDateEdit {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #4caf50;
                padding: 6px;
                border-radius: 4px;
            }
            QLabel {
                color: #ffffff;
            }
            QTableWidget {
                background-color: #3c3f41;
                color: #ffffff;
                border: none;
                gridline-color: #555555;
                font-size: 13px;  
            }
            QTableWidget QHeaderView::section {
                background-color: #4caf50;
                color: white;
                padding: 8px;
                border: none;
            }

            QMenuBar {
                background-color: #3c3f41;
                color: white;
            }
            QMenuBar::item {
                background-color: #3c3f41;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #4caf50;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                border: none;
                background: #2b2b2b;
                width: 8px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #4caf50;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;
            }
        """)

        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 1000, 700)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        # Add expense panel
        add_panel = QFrame()
        add_panel.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        add_layout = QHBoxLayout(add_panel)
        
        # Input fields
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

        # Buttons
        add_button = QPushButton("Add Expense")
        add_button.clicked.connect(self.add_expense)
        
        export_button = QPushButton("Export PDF")
        export_button.clicked.connect(self.export_pdf)
        
        # Add widgets to add panel
        add_layout.addWidget(expense_label)
        add_layout.addWidget(self.expense_input)
        add_layout.addWidget(price_label)
        add_layout.addWidget(self.price_input)
        add_layout.addWidget(date_label)
        add_layout.addWidget(self.date_input)
        add_layout.addWidget(add_button)
        add_layout.addWidget(export_button)
        
        layout.addWidget(add_panel)

        # Filter panel
        filter_panel = QFrame()
        filter_panel.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        filter_layout = QHBoxLayout(filter_panel)
        
        # Date range filter
        filter_layout.addWidget(QLabel("Filter by date range:"))
        
        start_date_label = QLabel("Start Date:")
        self.start_date_filter = QDateEdit()
        self.start_date_filter.setCalendarPopup(True)
        self.start_date_filter.setDate(QDate.currentDate().addMonths(-1))
        
        end_date_label = QLabel("End Date:")
        self.end_date_filter = QDateEdit()
        self.end_date_filter.setCalendarPopup(True)
        self.end_date_filter.setDate(QDate.currentDate())
        
        apply_filter_button = QPushButton("Apply Filter")
        apply_filter_button.clicked.connect(self.apply_date_filter)
        
        clear_filter_button = QPushButton("Clear Filter")
        clear_filter_button.clicked.connect(self.clear_filter)
        
        filter_layout.addWidget(start_date_label)
        filter_layout.addWidget(self.start_date_filter)
        filter_layout.addWidget(end_date_label)
        filter_layout.addWidget(self.end_date_filter)
        filter_layout.addWidget(apply_filter_button)
        filter_layout.addWidget(clear_filter_button)
        filter_layout.addStretch()
        
        layout.addWidget(filter_panel)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Expense", "Price", "Date", "Action"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setCornerButtonEnabled(False)

        # Fix header height and styling
        header = self.table.horizontalHeader()
        header.setFixedHeight(60)
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # Set column widths
        self.table.setColumnWidth(0, 300)  
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150) 

        layout.addWidget(self.table)

        # Pagination controls
        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_page)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.page_label = QLabel("Page 1")
        
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_button)
        pagination_layout.addStretch()
        
        layout.addLayout(pagination_layout)

        # Total and Filtered Total
        totals_layout = QHBoxLayout()
        
        # Overall total
        total_label = QLabel("Total:")
        self.total_value = QLabel("0.00")
        totals_layout.addWidget(total_label)
        totals_layout.addWidget(self.total_value)
        
        # Filtered total
        self.filtered_total_label = QLabel("Filtered Total:")
        self.filtered_total_value = QLabel("0.00")
        self.filtered_total_label.setVisible(False)
        self.filtered_total_value.setVisible(False)
        totals_layout.addSpacing(20)
        totals_layout.addWidget(self.filtered_total_label)
        totals_layout.addWidget(self.filtered_total_value)
        
        totals_layout.addStretch()
        layout.addLayout(totals_layout)

        self.load_expenses()

    def apply_date_filter(self):
        start_date = self.start_date_filter.date().toPyDate()
        end_date = self.end_date_filter.date().toPyDate()
        
        if start_date > end_date:
            QMessageBox.warning(self, "Invalid Date Range", 
                              "Start date must be before end date.")
            return
        
        self.is_filtered = True
        self.current_page = 1
        self.load_expenses()

    def clear_filter(self):
        self.is_filtered = False
        self.current_page = 1
        self.filtered_total_label.setVisible(False)
        self.filtered_total_value.setVisible(False)
        self.load_expenses()

    def load_expenses(self):
        self.table.setRowCount(0)
        
        if self.is_filtered:
            start_date = self.start_date_filter.date().toPyDate()
            end_date = self.end_date_filter.date().toPyDate()
            expenses = self.manager.get_expenses_in_duration(
                start_date, end_date, self.current_page, self.items_per_page
            )
        else:
            expenses = self.manager.get_expenses(self.current_page, self.items_per_page)
        
        total_pages = self.manager.get_total_pages(self.items_per_page)
        
        for expense_id, name, price, date in expenses:
            self.add_expense_row(expense_id, name, price, date)
            
        self.update_pagination_controls(total_pages)
        self.update_total()
        
        if self.is_filtered:
            self.update_filtered_total()

    def update_filtered_total(self):
        start_date = self.start_date_filter.date().toPyDate()
        end_date = self.end_date_filter.date().toPyDate()
        filtered_expenses = self.manager.get_expenses_in_duration(
            start_date, end_date, page=1, items_per_page=1000
        )
        filtered_total = sum(price for _, _, price, _ in filtered_expenses)
        
        self.filtered_total_label.setVisible(True)
        self.filtered_total_value.setVisible(True)
        self.filtered_total_value.setText(f"{filtered_total:.2f}")

    def add_expense_row(self, expense_id, name, price, date):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        self.table.setItem(row_position, 0, QTableWidgetItem(name))
        self.table.setItem(row_position, 1, QTableWidgetItem(f"{price:.2f}"))
        self.table.setItem(row_position, 2, QTableWidgetItem(str(date)))
        
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_expense(expense_id))
        self.table.setCellWidget(row_position, 3, delete_button)

    def add_expense(self):
        expense_name = self.expense_input.text().strip()
        price_text = self.price_input.text().strip()
        date = self.date_input.date().toPyDate()
        
        if self.manager.add_expense(expense_name, price_text, date):
            self.load_expenses()
            self.expense_input.clear()
            self.price_input.clear()
            self.date_input.setDate(QDate.currentDate())
        else:
            QMessageBox.warning(self, "Invalid Input", 
                              "Please enter a valid expense name and price.")

    def delete_expense(self, expense_id):
        self.manager.delete_expense(expense_id)
        self.load_expenses()

    def update_pagination_controls(self, total_pages):
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < total_pages)
        self.page_label.setText(f"Page {self.current_page} of {total_pages}")

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_expenses()

    def next_page(self):
        total_pages = self.manager.get_total_pages(self.items_per_page)
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_expenses()

    def update_total(self):
        all_expenses = self.manager.get_expenses(page=1, items_per_page=1000)  # Get all expenses
        total = sum(price for _, _, price, _ in all_expenses)
        self.total_value.setText(f"{total:.2f}")

    def export_pdf(self):
        try:
            # Get expenses based on current filter
            if self.is_filtered:
                start_date = self.start_date_filter.date().toPyDate()
                end_date = self.end_date_filter.date().toPyDate()
                expenses = self.manager.get_expenses_in_duration(
                    start_date, end_date, page=1, items_per_page=1000
                )
            else:
                expenses = self.manager.get_expenses(page=1, items_per_page=1000)
            
            # Create DataFrame
            data = {
                "Name": [name for _, name, _, _ in expenses],
                "Price": [f"{price:.2f}" for _, _, price, _ in expenses],
                "Date": [date for _, _, _, date in expenses]
            }
            df = pd.DataFrame(data)

            # Create figure and axis
            plt.figure(figsize=(11, 8))
            fig, ax = plt.subplots()

            # Hide axes
            ax.axis('off')

            # Create table
            table = ax.table(
                cellText=df.values,
                colLabels=df.columns,
                cellLoc='center',
                loc='center',
                colWidths=[0.4, 0.3, 0.3]
            )

            # Style the table
            table.auto_set_font_size(False)
            table.set_fontsize(9)
            table.scale(1.2, 1.5)

            # Add title
            title = "All Expenses Report"
            if self.is_filtered:
                title = f"Expenses Report ({self.start_date_filter.date().toString('yyyy-MM-dd')} to {self.end_date_filter.date().toString('yyyy-MM-dd')})"
            plt.title(title)

            # Save to PDF
            plt.savefig('expenses_report.pdf', 
                       bbox_inches='tight',
                       dpi=300,
                       format='pdf')
            plt.close()

            QMessageBox.information(self, "Export Successful", 
                                  "Expenses have been exported to 'expenses_report.pdf'")
        except Exception as e:
            QMessageBox.warning(self, "Export Failed", 
                              f"Failed to export expenses: {str(e)}")