from PySide6 import QtWidgets
from PySide6 import QtGui
from solver import Solver
import sys
import numpy as np

#lbltext = np.array2string(matrix)

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("PySide6 Application")
window.resize(600, 400)

table = QtWidgets.QTableWidget()
row_count = len(data) - 2
column_count = len(data[0])
table.setRowCount(row_count)
table.setColumnCount(column_count)
table.setHorizontalHeaderLabels([str(i) for i in range(1, len(data[0]) + 1)])
table.setFixedSize(column_count * 100 + 18, 20 + 35 * row_count)

for i in range(row_count):
    for k in range(len(data[0])):
        table.setItem(i, k, QtWidgets.QTableWidgetItem(str(data[i][k])))

btn = QtWidgets.QPushButton("Close")
box = QtWidgets.QVBoxLayout()

box.addWidget(table)
box.addWidget(btn)
window.setLayout(box)

btn.clicked.connect(app.quit)
window.show()

sys.exit(app.exec())