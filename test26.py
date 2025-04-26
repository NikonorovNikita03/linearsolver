import sys
import csv
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QGroupBox, QPushButton,
    QLabel, QSpinBox, QMessageBox, QTextEdit, QFileDialog,
    QStackedWidget, QHeaderView
)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QIcon, QColor, QBrush
from solver import Solver
from TransportProblemParser import TransportProblemParser
import constants


class TransportationSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение транспортной задачи")
        self.setGeometry(100, 100, 1366, 768)

        self.costs = [
            [4, 8, 8],
            [16, 24, 16],
            [8, 16, 24]
        ]
        self.supply = [76, 82, 77]
        self.demand = [72, 102, 41]
        self.total_cost = 0
        self.is_multi_product = False  # Флаг для определения типа задачи
        self.multi_product_data = {}   # Хранение данных для многопродуктной задачи

        self.central_widget = QWidget() 
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("padding: 3px; background: #f0f0f0; border-top: 1px solid #ccc;")

        self.icon = QIcon()
        self.icon.addFile('images/calculator.svg')
        self.setWindowIcon(self.icon)
        
        self.control_group = QGroupBox("Настройка задачи")
        self.create_controls()
        
        self.stacked_widget = QStackedWidget()
        
        self.input_page = QWidget()
        self.create_combined_input_table()
        
        self.solution_page = QWidget()
        self.create_solution_page()
        
        self.text_input_page = QWidget()
        self.create_text_input_page()
        
        self.stacked_widget.addWidget(self.input_page)
        self.stacked_widget.addWidget(self.solution_page)
        self.stacked_widget.addWidget(self.text_input_page)
        
        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.addWidget(self.status_label)

        self.update_table_size()
        self.write_data_into_input_table()
    
    def q_push_button(self, name, style, function, cursor=True):
        btn = QPushButton(name)
        btn.setStyleSheet(style)
        btn.clicked.connect(function)
        if cursor:
            btn.setCursor(Qt.PointingHandCursor)
        return btn

    def create_text_input_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel("Текстовый ввод данных")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(constants.title_label)
        layout.addWidget(title_label)
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(constants.text_edit_placeholder)
        layout.addWidget(self.text_edit)
        
        button_layout = QHBoxLayout()
        
        back_btn = self.q_push_button("Назад", "background-color: #607D8B; color: white;", self.show_input_page)
        enter_btn = self.q_push_button("Ввести", "background-color: #4CAF50; color: white;", self.process_text_input)

        button_layout.addWidget(back_btn)
        button_layout.addStretch()
        button_layout.addWidget(enter_btn)
        
        layout.addLayout(button_layout)
        self.text_input_page.setLayout(layout)
    
    def create_controls(self):
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(5, 5, 5, 5)
        control_layout.setSpacing(10)
        
        source_layout = QVBoxLayout()
        source_layout.setSpacing(0)
        source_layout.addWidget(QLabel("Поставщики:"))
        self.source_spin = QSpinBox()
        self.source_spin.setRange(1, 10)
        self.source_spin.setValue(3)
        self.source_spin.valueChanged.connect(self.update_input_table)
        source_layout.addWidget(self.source_spin)
        
        dest_layout = QVBoxLayout()
        dest_layout.setSpacing(0)
        dest_layout.addWidget(QLabel("Потребители:"))
        self.dest_spin = QSpinBox()
        self.dest_spin.setRange(1, 10)
        self.dest_spin.setValue(3)
        self.dest_spin.valueChanged.connect(self.update_input_table)
        dest_layout.addWidget(self.dest_spin)
        
        self.toggle_mode_btn = self.q_push_button(
            "Переключить на многопродуктную", 
            "background-color: #9C27B0; color: white;", 
            self.toggle_problem_mode
        )
        
        self.solve_btn = self.q_push_button("Решить", constants.solve_btn, self.solve_problem)
        
        self.back_btn = QPushButton("Назад")
        self.back_btn.setFixedHeight(60)
        self.back_btn.setStyleSheet("background-color: #607D8B; color: white;")
        self.back_btn.clicked.connect(self.show_input_page)
        self.back_btn.setVisible(False)
        
        control_layout.addLayout(source_layout)
        control_layout.addLayout(dest_layout)
        control_layout.addStretch()
        control_layout.addWidget(self.toggle_mode_btn)
        control_layout.addWidget(self.back_btn)
        control_layout.addWidget(self.solve_btn)
        
        self.control_group.setLayout(control_layout)
        self.main_layout.addWidget(self.control_group)

    def toggle_problem_mode(self):
        """Переключает между обычной и многопродуктной задачей"""
        if self.is_multi_product:
            # Сохраняем данные многопродуктной задачи перед переключением
            self.save_multi_product_data()
            self.is_multi_product = False
            self.toggle_mode_btn.setText("Переключить на многопродуктную")
            self.toggle_mode_btn.setStyleSheet("background-color: #9C27B0; color: white;")
        else:
            # Сохраняем данные обычной задачи перед переключением
            self.save_single_product_data()
            self.is_multi_product = True
            self.toggle_mode_btn.setText("Переключить на обычную")
            self.toggle_mode_btn.setStyleSheet("background-color: #673AB7; color: white;")
        
        # Обновляем таблицу ввода
        self.update_table_size()
        self.write_data_into_input_table()
        self.show_status_message("Режим изменен на " + ("многопродуктную" if self.is_multi_product else "обычную") + " задачу")

    def save_single_product_data(self):
        """Сохраняет данные обычной задачи перед переключением на многопродуктную"""
        try:
            self.get_data_from_input_table()
            self.multi_product_data = {
                'type': 'single',
                'costs': self.costs,
                'supply': self.supply,
                'demand': self.demand
            }
        except Exception as e:
            print(f"Ошибка при сохранении данных обычной задачи: {e}")

    def save_multi_product_data(self):
        """Сохраняет данные многопродуктной задачи перед переключением на обычную"""
        try:
            # Здесь можно добавить логику сохранения данных многопродуктной задачи
            # Пока просто сохраняем те же данные
            self.multi_product_data = {
                'type': 'multi',
                'costs': self.costs,
                'supply': self.supply,
                'demand': self.demand
            }
        except Exception as e:
            print(f"Ошибка при сохранении данных многопродуктной задачи: {e}")

    def create_combined_input_table(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        group = QGroupBox("Ввод данных транспортной задачи")
        group_layout = QVBoxLayout()
        
        self.combined_table = QTableWidget()
        self.combined_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        
        btn_layout = QHBoxLayout()
        copy_btn = self.q_push_button("Копировать", "background-color: #2196F3; color: white;", 
                                    lambda: self.copy_table_data(self.combined_table))
        paste_btn = self.q_push_button("Вставить", "background-color: #FF9800; color: white;", 
                                    lambda: self.paste_data_to_table(self.combined_table))
        
        btn_layout.addStretch()
        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(paste_btn)
        
        group_layout.addWidget(self.combined_table)
        group_layout.addLayout(btn_layout)
        group.setLayout(group_layout)
        
        layout.addWidget(group)
        self.input_page.setLayout(layout)

    def highlight_table_regions(self):
        """Выделяет цветом разные области таблицы"""
        # Очищаем предыдущее выделение
        for row in range(self.combined_table.rowCount()):
            for col in range(self.combined_table.columnCount()):
                item = self.combined_table.item(row, col)
                if item:
                    item.setBackground(QBrush(QColor(255, 255, 255)))
        
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        
        if self.is_multi_product:
            # Выделение для многопродуктной задачи
            products = 3  # Примерное количество продуктов
            
            # Выделяем область поставщиков (последняя колонка)
            for row in range(1, sources + 1):
                item = self.combined_table.item(row, destinations * products + 1)
                if item:
                    item.setBackground(QBrush(QColor(230, 240, 255)))  # Голубой
            
            # Выделяем область потребителей (последняя строка)
            for col in range(1, destinations * products + 1):
                item = self.combined_table.item(sources + 1, col)
                if item:
                    item.setBackground(QBrush(QColor(255, 230, 230)))  # Розовый
            
            # Выделяем область стоимости (основная таблица)
            for row in range(1, sources + 1):
                for col in range(1, destinations * products + 1):
                    item = self.combined_table.item(row, col)
                    if item:
                        item.setBackground(QBrush(QColor(230, 255, 230)))  # Зеленый
        else:
            # Выделение для обычной задачи
            # Выделяем область поставщиков (последняя колонка)
            for row in range(1, sources + 1):
                item = self.combined_table.item(row, destinations + 1)
                if item:
                    item.setBackground(QBrush(QColor(230, 240, 255)))  # Голубой
            
            # Выделяем область потребителей (последняя строка)
            for col in range(1, destinations + 1):
                item = self.combined_table.item(sources + 1, col)
                if item:
                    item.setBackground(QBrush(QColor(255, 230, 230)))  # Розовый
            
            # Выделяем область стоимости (основная таблица)
            for row in range(1, sources + 1):
                for col in range(1, destinations + 1):
                    item = self.combined_table.item(row, col)
                    if item:
                        item.setBackground(QBrush(QColor(230, 255, 230)))  # Зеленый
        
        # Выделяем угловую ячейку (баланс)
        corner_item = self.combined_table.item(sources + 1, destinations + 1)
        if corner_item:
            total_supply = sum(int(self.combined_table.item(i, destinations + 1).text()) 
                            for i in range(1, sources + 1) 
                            if self.combined_table.item(i, destinations + 1))
            total_demand = sum(int(self.combined_table.item(sources + 1, j).text()) 
                        for j in range(1, destinations + 1) 
                        if self.combined_table.item(sources + 1, j))
            
            if total_supply == total_demand:
                corner_item.setBackground(QBrush(QColor(200, 255, 200)))  # Зеленый если сбалансировано
            else:
                corner_item.setBackground(QBrush(QColor(255, 200, 200)))  # Красный если дисбаланс

    def process_text_input(self):
        tpp = TransportProblemParser(self.text_edit.toPlainText())
        print(tpp.parse_transport_problem())
        self.show_input_page()
    
    def show_text_input_page(self):        
        self.control_group.setVisible(False)
        self.stacked_widget.setCurrentIndex(2)
        self.solve_btn.setVisible(False)
        self.back_btn.setVisible(False)
    
    def show_input_page(self):        
        self.control_group.setVisible(True)
        self.stacked_widget.setCurrentIndex(0)
        self.solve_btn.setVisible(True)
        self.back_btn.setVisible(False)
    
    def show_solution_page(self):
        self.control_group.setVisible(True)
        self.stacked_widget.setCurrentIndex(1)
        self.solve_btn.setVisible(False)
        self.back_btn.setVisible(True)
    
    def create_solution_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        solution_group = QGroupBox("Оптимальное распределение")
        solution_layout = QVBoxLayout()
        solution_layout.setContentsMargins(5, 5, 5, 5)
        
        self.solution_table = QTableWidget()
        self.solution_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.solution_table.setStyleSheet("""
            QTableWidget {
                font-size: 12px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        
        s_header = self.solution_table.horizontalHeader()
        s_header.setSectionResizeMode(QHeaderView.Stretch)
        s_header.setDefaultAlignment(Qt.AlignCenter)
        s_header.setStyleSheet("""
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        s_v_header = self.solution_table.verticalHeader()
        s_v_header.setSectionResizeMode(QHeaderView.Stretch)
        s_v_header.setDefaultAlignment(Qt.AlignCenter)
        s_v_header.setStyleSheet("""
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #e0e0e0;
            }
        """)

        self.total_cost_label = QLabel("Общая стоимость: -")
        self.total_cost_label.setAlignment(Qt.AlignCenter)
        self.total_cost_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                background-color: #e8f5e9;
                border: 1px solid #c8e6c9;
                border-radius: 4px;
            }
        """)
        
        btn_layout = QHBoxLayout()
        
        solution_copy_btn = self.q_push_button(
            "Копировать решение", 
            """
            QPushButton {
                background-color: #2196F3; 
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            """, 
            lambda: self.copy_table_data(self.solution_table)
        )
        
        self.export_csv_btn = self.q_push_button(
            "Выгрузить CSV", 
            """
            QPushButton {
                background-color: #4CAF50; 
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
            """, 
            self.export_solution_to_csv
        )
        
        btn_layout.addStretch()
        btn_layout.addWidget(solution_copy_btn)
        btn_layout.addWidget(self.export_csv_btn)
        
        solution_layout.addWidget(self.solution_table)
        solution_layout.addWidget(self.total_cost_label)
        solution_layout.addLayout(btn_layout)
        solution_group.setLayout(solution_layout)
        
        layout.addWidget(solution_group)
        self.solution_page.setLayout(layout)

    def highlight_solution_table(self):
        """Выделяет цветом разные области таблицы решения"""
        if not self.solution_table.rowCount() or not self.solution_table.columnCount():
            return
        
        CORNER_COLOR = QColor(255, 255, 255)
        SUPPLIER_HEADER_COLOR = QColor(230, 240, 255)
        CONSUMER_HEADER_COLOR = QColor(255, 230, 230)
        VALUE_COLOR = QColor(220, 255, 220)
        NON_ZERO_COLOR = QColor(200, 255, 200)
        
        for row in range(self.solution_table.rowCount()):
            for col in range(self.solution_table.columnCount()):
                item = self.solution_table.item(row, col)
                if item:
                    item.setBackground(QBrush(QColor(255, 255, 255)))
        
        corner_row = self.solution_table.rowCount() - 1
        corner_col = self.solution_table.columnCount() - 1
        corner_item = self.solution_table.item(corner_row, corner_col)
        if corner_item:
            corner_item.setBackground(QBrush(CORNER_COLOR))
        
        for row in range(1, corner_row):
            item = self.solution_table.item(row, corner_col)
            if item:
                item.setBackground(QBrush(SUPPLIER_HEADER_COLOR))
        
        for col in range(1, corner_col):
            item = self.solution_table.item(corner_row, col)
            if item:
                item.setBackground(QBrush(CONSUMER_HEADER_COLOR))
        
        for row in range(1, corner_row):
            for col in range(1, corner_col):
                item = self.solution_table.item(row, col)
                if item:
                    item.setBackground(QBrush(VALUE_COLOR))
                    if item.text() != "0" and item.text() != "":
                        item.setBackground(QBrush(NON_ZERO_COLOR))
    
    def copy_table_data(self, table):
        if not table:
            return
            
        data = []
        for row in range(table.rowCount()):
            row_data = []
            for col in range(table.columnCount()):
                item = table.item(row, col)
                row_data.append(item.text() if item else "")
            data.append("\t".join(row_data))
        
        clipboard = QApplication.clipboard()
        mime_data = QMimeData()
        mime_data.setText("\n".join(data))
        clipboard.setMimeData(mime_data)
        self.show_status_message("Данные скопированы в буфер обмена!")
    
    def paste_data_to_table(self, table):
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        
        if not text:
            self.show_status_message("Буфер обмена пуст!")
            return
        
        rows = [row for row in text.split('\n') if row.strip()]
        if not rows:
            self.show_status_message("Нет данных в буфере обмена!")
            return
        
        data = [row.split('\t') for row in rows]
        
        try:
            new_rows = len(data)
            new_cols = max(len(row) for row in data) if data else 0
            
            table.setRowCount(new_rows)
            table.setColumnCount(new_cols)
            
            for row_idx in range(new_rows):
                for col_idx in range(min(len(data[row_idx]), new_cols)):
                    value = data[row_idx][col_idx]
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(Qt.AlignCenter)
                    table.setItem(row_idx, col_idx, item)
            
            if table == self.combined_table:
                if new_rows > 1 and new_cols > 1:
                    self.source_spin.setValue(new_rows - 1)
                    self.dest_spin.setValue(new_cols - 1)
            
            self.show_status_message("Данные вставлены успешно!")
            self.highlight_table_regions()
        except Exception as e:
            self.show_status_message(f"Ошибка при вставке данных: {str(e)}")
    
    def export_solution_to_csv(self):
        if self.solution_table.rowCount() == 0 or self.solution_table.columnCount() == 0:
            QMessageBox.warning(self, "Ошибка", "Нет данных для экспорта!")
            return
        
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить решение как CSV",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_name:
            return
        
        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                
                for i in range(self.solution_table.rowCount()):
                    row_data = []
                    for j in range(self.solution_table.columnCount()):
                        item = self.solution_table.item(i, j)
                        row_data.append(item.text() if item else "0")
                    writer.writerow(row_data)
                
                writer.writerow([constants.stringify(self.total_cost)])
            
            self.show_status_message(f"Решение сохранено в {file_name}")
            QMessageBox.information(self, "Успех", "Файл успешно сохранен!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
            self.show_status_message(f"Ошибка при сохранении CSV: {str(e)}")
    
    def show_status_message(self, message):
        self.status_label.setText(message)
    
    def get_data_from_input_table(self):
        rows = self.combined_table.rowCount()
        cols = self.combined_table.columnCount()
        
        if rows < 2 or cols < 2:
            raise ValueError("Таблица должна содержать хотя бы одного поставщика и потребителя")
        
        if self.is_multi_product:
            # Логика получения данных для многопродуктной задачи
            products = 3  # Примерное количество продуктов
            
            # Получаем данные о поставщиках (последняя колонка)
            self.supply = []
            for row in range(1, rows):
                item = self.combined_table.item(row, cols - 1)
                self.supply.append(int(item.text()) if item and item.text().isdigit() else 0)
            
            # Получаем данные о потребителях (последняя строка)
            self.demand = []
            for col in range(1, cols - 1):
                item = self.combined_table.item(rows - 1, col)
                self.demand.append(int(item.text()) if item and item.text().isdigit() else 0)
            
            # Получаем матрицу стоимостей
            self.costs = []
            for row in range(1, rows):
                cost_row = []
                for col in range(1, cols - 1):
                    item = self.combined_table.item(row, col)
                    cost_row.append(int(item.text()) if item and item.text().isdigit() else 0)
                self.costs.append(cost_row)
        else:
            # Логика получения данных для обычной задачи
            # Получаем данные о поставщиках (первая колонка, начиная со второй строки)
            self.supply = []
            for row in range(1, rows):
                item = self.combined_table.item(row, 0)
                self.supply.append(int(item.text()) if item and item.text().isdigit() else 0)
            
            # Получаем данные о потребителях (первая строка, начиная со второй колонки)
            self.demand = []
            for col in range(1, cols):
                item = self.combined_table.item(0, col)
                self.demand.append(int(item.text()) if item and item.text().isdigit() else 0)
            
            # Получаем матрицу стоимостей
            self.costs = []
            for row in range(1, rows):
                cost_row = []
                for col in range(1, cols):
                    item = self.combined_table.item(row, col)
                    cost_row.append(int(item.text()) if item and item.text().isdigit() else 0)
                self.costs.append(cost_row)
    
    def write_data_into_input_table(self):
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        
        if self.is_multi_product:
            # Настройка таблицы для многопродуктной задачи
            products = 3  # Примерное количество продуктов
            self.combined_table.setRowCount(sources + 2)
            self.combined_table.setColumnCount(destinations * products + 2)
            
            # Заполняем заголовки продуктов
            for p in range(products):
                for j in range(1, destinations + 1):
                    col = (p * destinations) + j
                    item = QTableWidgetItem(f"Продукт {p+1} Потр. {j}")
                    item.setTextAlignment(Qt.AlignCenter)
                    self.combined_table.setItem(0, col, item)
            
            # Заполняем заголовки поставщиков
            for i in range(1, sources + 1):
                item = QTableWidgetItem(f"Поставщик {i}")
                item.setTextAlignment(Qt.AlignCenter)
                self.combined_table.setItem(i, 0, item)
            
            # Заполняем поставки (последняя колонка)
            for i in range(1, sources + 1):
                val = self.supply[i-1] if len(self.supply) > i-1 else 0
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.combined_table.setItem(i, destinations * products + 1, item)
            
            # Заполняем спрос (последняя строка)
            for p in range(products):
                for j in range(1, destinations + 1):
                    col = (p * destinations) + j
                    val = self.demand[j-1] if len(self.demand) > j-1 else 0
                    item = QTableWidgetItem(str(val))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.combined_table.setItem(sources + 1, col, item)
            
            # Заполняем угловую ячейку
            corner_item = QTableWidgetItem("Многопродуктная")
            corner_item.setTextAlignment(Qt.AlignCenter)
            self.combined_table.setItem(sources + 1, destinations * products + 1, corner_item)
            
            # Заполняем матрицу стоимостей
            for i in range(1, sources + 1):
                for p in range(products):
                    for j in range(1, destinations + 1):
                        col = (p * destinations) + j
                        val = 0
                        if len(self.costs) > i-1 and len(self.costs[i-1]) > j-1:
                            val = self.costs[i-1][j-1]
                        item = QTableWidgetItem(str(val))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.combined_table.setItem(i, col, item)
        else:
            # Настройка таблицы для обычной задачи
            self.combined_table.setRowCount(sources + 2)
            self.combined_table.setColumnCount(destinations + 2)
            
            # Заполняем угловую ячейку (правый нижний угол)
            corner_item = QTableWidgetItem("")
            corner_item.setTextAlignment(Qt.AlignCenter)
            self.combined_table.setItem(sources + 1, destinations + 1, corner_item)
            
            # Добавляем подпись "Поставщики"
            suppliers_label = QTableWidgetItem("Поставщики")
            suppliers_label.setTextAlignment(Qt.AlignCenter)
            self.combined_table.setItem(0, destinations + 1, suppliers_label)
            
            # Добавляем подпись "Потребители"
            consumers_label = QTableWidgetItem("Потребители")
            consumers_label.setTextAlignment(Qt.AlignCenter)
            self.combined_table.setItem(sources + 1, 0, consumers_label)

            # Заполняем угловую ячейку (левый верхний угол)
            corner_item = QTableWidgetItem("Маршруты")
            corner_item.setTextAlignment(Qt.AlignCenter)
            self.combined_table.setItem(0, 0, corner_item)
            
            # Заполняем заголовки поставщиков (первая колонка)
            for i in range(1, sources + 1):
                item = QTableWidgetItem(f"Поставщик {i}")
                item.setTextAlignment(Qt.AlignCenter)
                self.combined_table.setItem(i, 0, item)
            
            # Заполняем заголовки потребителей (первая строка)
            for j in range(1, destinations + 1):
                item = QTableWidgetItem(f"Потребитель {j}")
                item.setTextAlignment(Qt.AlignCenter)
                self.combined_table.setItem(0, j, item)
            
            # Заполняем угловую ячейку (правый нижний угол) с балансом
            total_supply = sum(self.supply[:sources]) if len(self.supply) >= sources else 0
            total_demand = sum(self.demand[:destinations]) if len(self.demand) >= destinations else 0
            balance = "Сбалансировано" if total_supply == total_demand else f"Дисбаланс: {total_supply - total_demand}"
            
            corner_item = QTableWidgetItem(f"{balance}")
            corner_item.setTextAlignment(Qt.AlignCenter)
            self.combined_table.setItem(sources + 1, destinations + 1, corner_item)
            
            # Автозаполнение названий поставщиков (последняя колонка)
            for i in range(1, sources + 1):
                name_item = QTableWidgetItem(f"Поставщик {i}")
                name_item.setTextAlignment(Qt.AlignCenter)
                self.combined_table.setItem(i, destinations + 1, name_item)
                
                val = self.supply[i-1] if len(self.supply) > i-1 else 0
                value_item = QTableWidgetItem(str(val))
                value_item.setTextAlignment(Qt.AlignCenter)
                self.combined_table.setItem(i, destinations + 1, value_item)
            
            # Автозаполнение названий потребителей (последняя строка)
            for j in range(1, destinations + 1):
                name_item = QTableWidgetItem(f"Потребитель {j}")
                name_item.setTextAlignment(Qt.AlignCenter)
                self.combined_table.setItem(sources + 1, j, name_item)
                
                val = self.demand[j-1] if len(self.demand) > j-1 else 0
                value_item = QTableWidgetItem(str(val))
                value_item.setTextAlignment(Qt.AlignCenter)
                self.combined_table.setItem(sources + 1, j, value_item)
            
            # Заполняем матрицу стоимостей
            for i in range(1, sources + 1):
                for j in range(1, destinations + 1):
                    val = 0
                    if len(self.costs) > i-1 and len(self.costs[i-1]) > j-1:
                        val = self.costs[i-1][j-1]
                    item = QTableWidgetItem(str(val))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.combined_table.setItem(i, j, item)
        
        self.highlight_table_regions()

    def update_table_size(self):
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        
        if self.is_multi_product:
            # Размер таблицы для многопродуктной задачи
            products = 3  # Примерное количество продуктов
            self.combined_table.setRowCount(sources + 2)
            self.combined_table.setColumnCount(destinations * products + 2)
        else:
            # Размер таблицы для обычной задачи
            self.combined_table.setRowCount(sources + 2)
            self.combined_table.setColumnCount(destinations + 2)
        
        # Настраиваем размеры столбцов и строк
        for i in range(self.combined_table.columnCount()):
            self.combined_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        
        for i in range(self.combined_table.rowCount()):
            self.combined_table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
    
    def update_input_table(self):
        self.get_data_from_input_table()
        self.update_table_size()
        self.write_data_into_input_table()
    
    def extract_data(self):
        self.get_data_from_input_table()
        return self.costs, self.supply, self.demand
    
    def solve_problem(self):
        try:
            costs, supply, demand = self.extract_data()
            
            if self.is_multi_product:
                # Логика решения многопродуктной задачи
                # Здесь можно добавить специальную обработку для многопродуктного случая
                pass
            
            problem = Solver(supply, demand, costs)
            result_matrix, self.total_cost = problem.solve_transportation_scipy()

            sources = len(result_matrix)
            destinations = len(result_matrix[0]) if sources > 0 else 0

            self.solution_table.setRowCount(sources)
            self.solution_table.setColumnCount(destinations)
            
            for i in range(sources):
                input_item = self.combined_table.item(i + 1, 0)
                supplier_name = input_item.text() if input_item else f"Поставщик {i + 1}"
                self.solution_table.setVerticalHeaderItem(i, QTableWidgetItem(supplier_name))
            
            for j in range(destinations):
                input_item = self.combined_table.item(0, j + 1)
                consumer_name = input_item.text() if input_item else f"Потребитель {j + 1}"
                self.solution_table.setHorizontalHeaderItem(j, QTableWidgetItem(consumer_name))
            
            for i in range(sources):
                for j in range(destinations):
                    item = QTableWidgetItem(str(result_matrix[i][j]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.solution_table.setItem(i, j, item)
            
            self.total_cost_label.setText(f"Общая стоимость: {constants.stringify(self.total_cost)}")
            self.highlight_solution_table()
            
            self.show_solution_page()
            self.show_status_message("Задача решена!")
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Ошибка", f"Не удалось решить задачу:\n{str(e)}")
            self.show_status_message("Задача решена!")
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Ошибка", f"Не удалось решить задачу:\n{str(e)}")
            self.show_status_message(f"Ошибка: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransportationSolver()
    window.show()
    sys.exit(app.exec())