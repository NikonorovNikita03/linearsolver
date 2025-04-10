import sys
from solver import Solver
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QWidget
from PySide6.QtGui import QColor


colors = [
    ["Red", "#FF0000"],
    ["Red", "#FF0000"],
    ["Red", "#FF0000"]
]

def get_rgb_from_hex(code):
    code_hex = code.replace("#", "")
    rgb = tuple(int(code_hex[i:i+2], 16) for i in (0, 2, 4))
    return QColor.fromRgb(rgb[0], rgb[1], rgb[2])

app = QApplication()
window = QWidget()
window.setWindowTitle("Диплом")
window.resize(800, 600)

table = QTableWidget()
table.setRowCount(len(colors))
table.setColumnCount(len(colors[0]) + 1)
table.setHorizontalHeaderLabels(["Name", "Hex", "Color"])

for i, (name, code) in enumerate(colors):
    name = QTableWidgetItem(name)
    color = QTableWidgetItem()
    color.setBackground(get_rgb_from_hex(code))
    code = QTableWidgetItem(code)
    table.setItem(i, 0, name)
    table.setItem(i, 1, code)
    table.setItem(i, 2, color)

table.show()
sys.exit(app.exec())

# data = [
#     [7, 8, 1, 2],
#     [4, 5, 9, 8],
#     [9, 2, 3, 6],
#     [160, 140, 170],
#     [120, 50, 190, 110]   
# ]

# problem = Solver(data[-2], data[-1], data[:-2])
# matrix, costs, surplus = problem.double_preference()

# data3 = [
#     [11, 13, 17, 14],
#     [16, 18, 14, 10],
#     [21, 24, 13, 10],
#     [250, 300, 400],
#     [200, 225, 275, 250]
# ]
# data2 = [
#     [4, 8, 8],
#     [16, 24, 16],
#     [8, 16, 24],
#     [76, 82, 77],
#     [72, 102, 41]
# ]
# data = [
#     [19, 30, 50, 10],
#     [70, 30, 40, 60],
#     [40, 8, 70, 20],
#     [7, 9, 18],
#     [5, 8, 7, 14]
# ]
# problem = Solver(data[-2], data[-1], data[:-2])
# matrix, costs, surplus = problem.modi_method()
# print(matrix)
# print(costs)
# print(surplus)