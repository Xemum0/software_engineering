from PyQt5.QtWidgets import QApplication
from ExpenseUI import ExpenseUI
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseUI()
    window.show()
    sys.exit(app.exec_())
