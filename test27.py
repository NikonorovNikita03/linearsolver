import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QTableWidget,
                               QTableWidgetItem, QVBoxLayout, QWidget,
                               QPushButton, QHBoxLayout, QLabel, QSpinBox)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Таблица с пропорциональными размерами")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Параметры таблицы
        self.rows = 5
        self.cols = 5
        self.row_percentages = [100 / self.rows] * self.rows  # Изначально равные доли
        self.col_percentages = [100 / self.cols] * self.cols  # Изначально равные доли

        # Кнопки и спинбоксы для управления размером ячеек
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        # Выбор строки
        row_label = QLabel("Строка:")
        self.row_spinbox = QSpinBox()
        self.row_spinbox.setMinimum(0)
        self.row_spinbox.setMaximum(self.rows - 1)  # Максимум - номер последней строки
        control_layout.addWidget(row_label)
        control_layout.addWidget(self.row_spinbox)

        # Процент строки
        row_percent_label = QLabel("Процент высоты строки:")
        self.row_percent_spinbox = QSpinBox()
        self.row_percent_spinbox.setMinimum(1)
        self.row_percent_spinbox.setMaximum(100)  # Максимум 100%
        self.row_percent_spinbox.setValue(int(self.row_percentages[0])) # Изначальное значение
        control_layout.addWidget(row_percent_label)
        control_layout.addWidget(self.row_percent_spinbox)

        self.row_percent_spinbox.valueChanged.connect(self.set_row_percentage)


        # Выбор столбца
        col_label = QLabel("Столбец:")
        self.col_spinbox = QSpinBox()
        self.col_spinbox.setMinimum(0)
        self.col_spinbox.setMaximum(self.cols - 1) # Максимум - номер последнего столбца
        control_layout.addWidget(col_label)
        control_layout.addWidget(self.col_spinbox)

        # Процент столбца
        col_percent_label = QLabel("Процент ширины столбца:")
        self.col_percent_spinbox = QSpinBox()
        self.col_percent_spinbox.setMinimum(1)
        self.col_percent_spinbox.setMaximum(100)  # Максимум 100%
        self.col_percent_spinbox.setValue(int(self.col_percentages[0])) # Изначальное значение
        control_layout.addWidget(col_percent_label)
        control_layout.addWidget(self.col_percent_spinbox)

        self.col_percent_spinbox.valueChanged.connect(self.set_col_percentage)


        self.table_widget = QTableWidget()
        main_layout.addWidget(self.table_widget)

        # Инициализация таблицы
        self.table_widget.setRowCount(self.rows)
        self.table_widget.setColumnCount(self.cols)

        # Заполнение таблицы данными (просто для примера)
        for row in range(self.rows):
            for col in range(self.cols):
                item = QTableWidgetItem(f"Row {row}, Col {col}")
                self.table_widget.setItem(row, col, item)

        # Устанавливаем режим растягивания
        self.table_widget.horizontalHeader().setSectionResizeMode(self.table_widget.horizontalHeader().ResizeMode.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(self.table_widget.verticalHeader().ResizeMode.Stretch)


        # Установка первоначальных размеров строк и столбцов
        self.update_row_heights()
        self.update_column_widths()


    def set_row_percentage(self, value):
        row_index = self.row_spinbox.value()
        old_percentage = self.row_percentages[row_index]
        diff = value - old_percentage
        self.row_percentages[row_index] = value

        remaining_rows = self.rows - 1
        if remaining_rows > 0:  # Чтобы не было деления на ноль при rows=1
            diff_per_row = diff / remaining_rows
            for i in range(self.rows):
                if i != row_index:
                    self.row_percentages[i] -= diff_per_row
                    self.row_percentages[i] = max(1, self.row_percentages[i]) # Гарантируем, что процент не станет меньше 1
        self.update_row_heights()

    def set_col_percentage(self, value):
        col_index = self.col_spinbox.value()
        old_percentage = self.col_percentages[col_index]
        diff = value - old_percentage
        self.col_percentages[col_index] = value


        remaining_cols = self.cols - 1
        if remaining_cols > 0:
            diff_per_col = diff / remaining_cols
            for i in range(self.cols):
                if i != col_index:
                    self.col_percentages[i] -= diff_per_col
                    self.col_percentages[i] = max(1, self.col_percentages[i]) # Гарантируем, что процент не станет меньше 1
        self.update_column_widths()

    def update_row_heights(self):
        total_height = self.table_widget.height()  # Текущая высота таблицы
        for row in range(self.rows):
            height = int(total_height * self.row_percentages[row] / 100)
            self.table_widget.setRowHeight(row, height)

    def update_column_widths(self):
        total_width = self.table_widget.width()  # Текущая ширина таблицы
        for col in range(self.cols):
            width = int(total_width * self.col_percentages[col] / 100)
            self.table_widget.setColumnWidth(col, width)

    def resizeEvent(self, event):
        # Обновляем размеры строк и столбцов при изменении размера окна
        self.update_row_heights()
        self.update_column_widths()
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())