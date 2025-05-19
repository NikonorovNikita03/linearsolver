import sys
from PySide6.QtWidgets import QApplication
from UserInterface import UserInterface
from ProblemDatabase import ProblemDatabase

if __name__ == "__main__":
    db = ProblemDatabase()
    app = QApplication(sys.argv)
    window = UserInterface()
    window.show()
    sys.exit(app.exec()) 