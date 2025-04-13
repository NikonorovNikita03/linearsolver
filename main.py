import sys
from PySide6.QtWidgets import QApplication
from TransportationSolver import TransportationSolver

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransportationSolver()
    window.show()
    sys.exit(app.exec())