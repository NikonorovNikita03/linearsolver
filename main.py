import sys
from PySide6.QtWidgets import QApplication
from UserInterface import UserInterface

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserInterface()
    window.show()
    sys.exit(app.exec()) 