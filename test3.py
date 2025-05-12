from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QListWidget, QVBoxLayout, QWidget

app = QApplication([])

table = QTableWidget(3, 2)  # 3 строки, 2 столбца

# Создаем виджет-контейнер для ячейки
cell_widget = QWidget()
layout = QVBoxLayout(cell_widget)

# Создаем список
list_widget = QListWidget()
list_widget.addItems(["Элемент 1", "Элемент 2", "Элемент 3"])

# Добавляем список в контейнер
layout.addWidget(list_widget)
cell_widget.setLayout(layout)

# Помещаем контейнер в ячейку таблицы
table.setCellWidget(1, 1, cell_widget)

table.show()
app.exec()