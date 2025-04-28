import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QHeaderView
)


class TableApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таблица с объединенными ячейками")
        self.setGeometry(100, 100, 600, 400)
        
        # Создаем центральный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Создаем таблицу 5x5
        self.table = QTableWidget(5, 5)
        layout.addWidget(self.table)
        
        # Настраиваем таблицу
        self.setup_table()
        
        # Заполняем таблицу данными
        self.populate_table()
    
    def setup_table(self):
        # Настраиваем заголовки
        self.table.setHorizontalHeaderLabels(["Колонка 1", "Колонка 2", "Колонка 3", "Колонка 4", "Колонка 5"])
        self.table.setVerticalHeaderLabels(["Строка 1", "Строка 2", "Строка 3", "Строка 4", "Строка 5"])
        
        # Растягиваем ячейки на всю доступную область
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Объединяем некоторые ячейки
        self.table.setSpan(0, 0, 1, 2)  # Первая ячейка занимает 1 строку и 2 колонки
        self.table.setSpan(1, 1, 2, 1)  # Ячейка занимает 2 строки и 1 колонку
        self.table.setSpan(3, 3, 2, 2)  # Ячейка занимает 2 строки и 2 колонки
    
    def populate_table(self):
        # Заполняем таблицу данными
        data = [
            ["Объединенная ячейка (1x2)", "", "Обычная", "Обычная", "Обычная"],
            ["Обычная", "Объединенная (2x1)", "Обычная", "Обычная", "Обычная"],
            ["Обычная", "", "Обычная", "Обычная", "Обычная"],
            ["Обычная", "Обычная", "Обычная", "Объединенная (2x2)", ""],
            ["Обычная", "Обычная", "Обычная", "", ""]
        ]
        
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                if data[row][col]:  # Если есть текст для этой ячейки
                    item = QTableWidgetItem(data[row][col])
                    self.table.setItem(row, col, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableApp()
    window.show()
    sys.exit(app.exec())