import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QGroupBox, QPushButton,
    QLabel, QSpinBox, QComboBox, QTextEdit, QMessageBox, QTabWidget, QStatusBar,
    QHeaderView, QGridLayout, QSplitter
)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QClipboard, QIcon
from solver import Solver


class TransportationSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение транспортной задачи")
        self.setGeometry(100, 100, 1366, 768)
        
        self.central_widget = QWidget() 
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        # Создаём отдельный виджет для статуса
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("padding: 3px; background: #f0f0f0; border-top: 1px solid #ccc;")

        self.icon = QIcon()
        self.icon.addFile('images/calculator.svg')
        self.setWindowIcon(self.icon)
        
        self.create_controls()
        
        # Создаём главный табвиджет
        self.main_tabs = QTabWidget()
        self.main_tabs.setStyleSheet("""
            QTabBar::tab {
                padding: 8px 15px;
                background: #f0f0f0;
                border: 1px solid #ccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #fff;
                border-color: #aaa;
                border-bottom: 1px solid #fff;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background: #e0e0e0;
            }
            QTabWidget::pane {
                border: 1px solid #aaa;
                margin-top: -1px;
                background: #fff;
            }
        """)
        
        # Вкладка с исходными данными
        self.input_tab = QWidget()
        self.create_input_tables()
        
        # Вкладка с решением
        self.solution_tab = QWidget()
        self.create_solution_tab()
        
        # Добавляем вкладки
        self.main_tabs.addTab(self.input_tab, "Исходные данные")
        self.main_tabs.addTab(self.solution_tab, "Решение")
        
        self.main_layout.addWidget(self.main_tabs)
        
        # Добавляем виджет статуса в основной layout
        self.main_layout.addWidget(self.status_label)
        
        # Initialize with default problem size
        self.update_table_size()
    
    def create_controls(self):
        """Create control panel with problem setup options"""
        control_group = QGroupBox("Настройка задачи")
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(5, 5, 5, 5)
        control_layout.setSpacing(10)
        
        # Source controls
        source_layout = QVBoxLayout()
        source_layout.setSpacing(0)
        source_layout.addWidget(QLabel("Поставщики:"))
        self.source_spin = QSpinBox()
        self.source_spin.setRange(1, 10)
        self.source_spin.setValue(3)
        self.source_spin.valueChanged.connect(self.update_table_size)
        source_layout.addWidget(self.source_spin)
        
        # Destination controls
        dest_layout = QVBoxLayout()
        dest_layout.setSpacing(0)
        dest_layout.addWidget(QLabel("Потребители:"))
        self.dest_spin = QSpinBox()
        self.dest_spin.setRange(1, 10)
        self.dest_spin.setValue(3)
        self.dest_spin.valueChanged.connect(self.update_table_size)
        dest_layout.addWidget(self.dest_spin)
        
        # Method selection
        method_layout = QVBoxLayout()
        method_layout.setSpacing(0)
        method_layout.addWidget(QLabel("Метод:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Автоматически"
        ])
        method_layout.addWidget(self.method_combo)
        
        # Solve button
        self.solve_btn = QPushButton("Решить")
        self.solve_btn.setFixedHeight(60)
        self.solve_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                padding: 8px;
                margin-top: 18px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.solve_btn.clicked.connect(self.solve_problem)
        
        # Add all controls to layout
        control_layout.addLayout(source_layout)
        control_layout.addLayout(dest_layout)
        control_layout.addLayout(method_layout)
        control_layout.addStretch()
        control_layout.addWidget(self.solve_btn)
        
        control_group.setLayout(control_layout)
        self.main_layout.addWidget(control_group)
    
    def create_input_tables(self):
        """Create three tables for costs, supply and demand with specified layout"""
        input_layout = QVBoxLayout()
        #input_layout.setSpacing(5)
        #input_layout.setContentsMargins(5, 5, 5, 5)
        
        # Верхняя область (горизонтальная, 7/8 высоты)
        top_area = QHBoxLayout()
        #top_area.setSpacing(5)
        
        # Таблица перевозок (ширина равна таблице потребителей)
        costs_group = QGroupBox("Стоимости перевозок")
        costs_layout = QVBoxLayout()
        #costs_layout.setContentsMargins(5, 5, 5, 5)
        
        self.costs_table = QTableWidget()
        self.costs_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        
        # Настройка заголовков таблицы
        header = self.costs_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setVisible(False)
        
        v_header = self.costs_table.verticalHeader()
        v_header.setSectionResizeMode(QHeaderView.Stretch)
        v_header.setDefaultAlignment(Qt.AlignCenter)
        v_header.setVisible(False)
        
        # Кнопки копирования/вставки
        costs_btn_layout = QHBoxLayout()
        costs_copy_btn = QPushButton("Копировать")
        costs_copy_btn.setStyleSheet("background-color: #2196F3; color: white;")
        costs_copy_btn.clicked.connect(lambda: self.copy_table_data(self.costs_table))
        
        costs_paste_btn = QPushButton("Вставить")
        costs_paste_btn.setStyleSheet("background-color: #FF9800; color: white;")
        costs_paste_btn.clicked.connect(lambda: self.paste_data_to_table(self.costs_table))
        
        costs_btn_layout.addStretch()
        costs_btn_layout.addWidget(costs_copy_btn)
        costs_btn_layout.addWidget(costs_paste_btn)
        
        costs_layout.addWidget(self.costs_table)
        costs_layout.addLayout(costs_btn_layout)
        costs_group.setLayout(costs_layout)
        
        # Таблица поставщиков (фиксированная ширина)
        supply_group = QGroupBox("Запасы поставщиков")
        supply_layout = QVBoxLayout()
        #supply_layout.setContentsMargins(5, 5, 5, 5)
        
        self.supply_table = QTableWidget(1, 1)
        self.supply_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        #self.supply_table.setFixedWidth(200)  # Фиксированная ширина
        
        # Настройка заголовков таблицы
        s_header = self.supply_table.horizontalHeader()
        s_header.setSectionResizeMode(QHeaderView.Stretch)
        s_header.setDefaultAlignment(Qt.AlignCenter)
        s_header.setVisible(False)
        
        s_v_header = self.supply_table.verticalHeader()
        s_v_header.setSectionResizeMode(QHeaderView.Stretch)
        s_v_header.setDefaultAlignment(Qt.AlignCenter)
        s_v_header.setVisible(False)
        
        # Кнопки копирования/вставки
        supply_btn_layout = QHBoxLayout()
        supply_copy_btn = QPushButton("Копировать")
        supply_copy_btn.setStyleSheet("background-color: #2196F3; color: white;")
        supply_copy_btn.clicked.connect(lambda: self.copy_table_data(self.supply_table))
        
        supply_paste_btn = QPushButton("Вставить")
        supply_paste_btn.setStyleSheet("background-color: #FF9800; color: white;")
        supply_paste_btn.clicked.connect(lambda: self.paste_data_to_table(self.supply_table))
        
        supply_btn_layout.addStretch()
        supply_btn_layout.addWidget(supply_copy_btn)
        supply_btn_layout.addWidget(supply_paste_btn)
        
        supply_layout.addWidget(self.supply_table)
        supply_layout.addLayout(supply_btn_layout)
        supply_group.setLayout(supply_layout)
        
        # Добавляем таблицы в верхнюю область
        top_area.addWidget(costs_group, stretch=6)  # Основная ширина
        top_area.addWidget(supply_group, stretch=1)  # Фиксированная ширина
        
        # Нижняя область (таблица потребителей с фиксированной шириной и пустым пространством)
        demand_container = QWidget()
        demand_layout = QHBoxLayout()
        #demand_layout.setContentsMargins(0, 0, 0, 0)
        
        demand_group = QGroupBox("Потребности потребителей")
        group_layout = QVBoxLayout()
        #group_layout.setContentsMargins(5, 5, 5, 5)
        
        self.demand_table = QTableWidget(1, 1)
        self.demand_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        #self.demand_table.setFixedWidth(200)  # Такая же ширина, как у таблицы поставщиков
        
        # Настройка заголовков таблицы
        d_header = self.demand_table.horizontalHeader()
        d_header.setSectionResizeMode(QHeaderView.Stretch)
        d_header.setDefaultAlignment(Qt.AlignCenter)
        d_header.setVisible(False)
        
        d_v_header = self.demand_table.verticalHeader()
        d_v_header.setSectionResizeMode(QHeaderView.Stretch)
        d_v_header.setDefaultAlignment(Qt.AlignCenter)
        d_v_header.setVisible(False)
        
        # Кнопки копирования/вставки
        demand_btn_layout = QHBoxLayout()
        demand_copy_btn = QPushButton("Копировать")
        demand_copy_btn.setStyleSheet("background-color: #2196F3; color: white;")
        demand_copy_btn.clicked.connect(lambda: self.copy_table_data(self.demand_table))
        
        demand_paste_btn = QPushButton("Вставить")
        demand_paste_btn.setStyleSheet("background-color: #FF9800; color: white;")
        demand_paste_btn.clicked.connect(lambda: self.paste_data_to_table(self.demand_table))
        
        demand_btn_layout.addStretch()
        demand_btn_layout.addWidget(demand_copy_btn)
        demand_btn_layout.addWidget(demand_paste_btn)
        
        group_layout.addWidget(self.demand_table)
        group_layout.addLayout(demand_btn_layout)
        demand_group.setLayout(group_layout)
        
        # Добавляем таблицу потребителей и пустое пространство
        demand_layout.addWidget(demand_group, 6)
        demand_layout.addStretch(1)  # Добавляем растягивающееся пустое пространство
        
        demand_container.setLayout(demand_layout)
        
        # Устанавливаем соотношение высот верхней и нижней областей (7:1)
        input_layout.addLayout(top_area, stretch=7)
        input_layout.addWidget(demand_container, stretch=1)
        
        self.input_tab.setLayout(input_layout)
    
    def create_solution_tab(self):
        """Create combined solution tab with table and text"""
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Используем QSplitter для разделения таблицы и текста
        splitter = QSplitter(Qt.Vertical)
        
        # Таблица решения
        solution_group = QGroupBox("Оптимальное распределение")
        solution_layout = QVBoxLayout()
        solution_layout.setContentsMargins(5, 5, 5, 5)
        
        self.solution_table = QTableWidget()
        self.solution_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.solution_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        
        # Configure solution table resize behavior
        s_header = self.solution_table.horizontalHeader()
        s_header.setSectionResizeMode(QHeaderView.Stretch)
        s_header.setDefaultAlignment(Qt.AlignCenter)
        
        s_v_header = self.solution_table.verticalHeader()
        s_v_header.setSectionResizeMode(QHeaderView.Stretch)
        s_v_header.setDefaultAlignment(Qt.AlignCenter)
        
        solution_copy_btn = QPushButton("Копировать решение")
        solution_copy_btn.setStyleSheet("background-color: #2196F3; color: white;")
        solution_copy_btn.clicked.connect(lambda: self.copy_table_data(self.solution_table))
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(solution_copy_btn)
        
        solution_layout.addWidget(self.solution_table)
        solution_layout.addLayout(btn_layout)
        solution_group.setLayout(solution_layout)
        
        # Текст решения
        summary_group = QGroupBox("Результаты")
        summary_layout = QVBoxLayout()
        summary_layout.setContentsMargins(5, 5, 5, 5)
        
        self.solution_text = QTextEdit()
        self.solution_text.setReadOnly(True)
        self.solution_text.setStyleSheet("font-family: monospace;")
        
        summary_layout.addWidget(self.solution_text)
        summary_group.setLayout(summary_layout)
        
        # Добавляем виджеты в splitter
        splitter.addWidget(solution_group)
        splitter.addWidget(summary_group)
        
        # Устанавливаем начальные размеры
        splitter.setSizes([500, 200])
        
        layout.addWidget(splitter)
        self.solution_tab.setLayout(layout)
    
    def copy_table_data(self, table):
        """Copy only the cell values without headers to clipboard"""
        if not table:
            return
            
        # Get all data from the table
        data = []
        for row in range(table.rowCount()):
            row_data = []
            for col in range(table.columnCount()):
                item = table.item(row, col)
                row_data.append(item.text() if item else "")
            data.append("\t".join(row_data))
        
        # Put the data in clipboard
        clipboard = QApplication.clipboard()
        mime_data = QMimeData()
        mime_data.setText("\n".join(data))
        clipboard.setMimeData(mime_data)
        
        # Show temporary status message
        self.show_status_message("Данные скопированы в буфер обмена!")
    
    def paste_data_to_table(self, table):
        """Paste data from clipboard to specified table"""
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        
        if not text:
            self.show_status_message("Буфер обмена пуст!")
            return
        
        # Split clipboard data into rows
        rows = [row for row in text.split('\n') if row.strip()]
        if not rows:
            self.show_status_message("Нет данных в буфере обмена!")
            return
        
        # Split each row into columns
        data = [row.split('\t') for row in rows]
        
        try:
            # Insert as much data as possible without errors
            for row_idx in range(min(len(data), table.rowCount())):
                for col_idx in range(min(len(data[row_idx]), table.columnCount())):
                    value = data[row_idx][col_idx]
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(Qt.AlignCenter)
                    table.setItem(row_idx, col_idx, item)
            
            self.show_status_message("Данные вставлены успешно!")
        except Exception as e:
            self.show_status_message(f"Ошибка при вставке данных: {str(e)}")
    
    def show_status_message(self, message):
        """Display status message in the dedicated label"""
        self.status_label.setText(message)
    
    def update_table_size(self):
        """Update all tables dimensions based on sources/destinations"""
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        
        # Update costs table (sources x destinations)
        self.costs_table.setRowCount(sources)
        self.costs_table.setColumnCount(destinations)
        self.costs_table.clearContents()
        
        for i in range(sources):
            for j in range(destinations):
                item = QTableWidgetItem("10")
                item.setTextAlignment(Qt.AlignCenter)
                self.costs_table.setItem(i, j, item)
        
        # Update supply table (sources x 1)
        self.supply_table.setRowCount(sources)
        self.supply_table.setColumnCount(1)
        self.supply_table.clearContents()
        
        for i in range(sources):
            item = QTableWidgetItem("100")
            item.setTextAlignment(Qt.AlignCenter)
            self.supply_table.setItem(i, 0, item)
        
        # Update demand table (1 x destinations)
        self.demand_table.setRowCount(1)
        self.demand_table.setColumnCount(destinations)
        self.demand_table.clearContents()
        
        for j in range(destinations):
            item = QTableWidgetItem("80")
            item.setTextAlignment(Qt.AlignCenter)
            self.demand_table.setItem(0, j, item)
    
    def extract_data(self):
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        
        costs = []
        supply = []
        demand = []
        
        # Get costs data
        for i in range(sources):
            row = []
            for j in range(destinations):
                item = self.costs_table.item(i, j)
                value = int(item.text()) if item and item.text().isdigit() else 0
                row.append(value)
            costs.append(row)
        
        # Get supply data
        for i in range(sources):
            item = self.supply_table.item(i, 0)
            value = int(item.text()) if item and item.text().isdigit() else 0
            supply.append(value)
        
        # Get demand data
        for j in range(destinations):
            item = self.demand_table.item(0, j)
            value = int(item.text()) if item and item.text().isdigit() else 0
            demand.append(value)
        
        return costs, supply, demand

    def solve_problem(self):
        costs, supply, demand = self.extract_data()

        problem = Solver(supply, demand, costs)
        result_matrix, total_cost = problem.solve_transportation_scipy()

        sources, destinations = len(result_matrix), len(result_matrix[0])

        self.solution_table.setRowCount(sources)
        self.solution_table.setColumnCount(destinations)
        self.solution_table.setHorizontalHeaderLabels([f"Потребитель {j+1}" for j in range(destinations)])
        self.solution_table.setVerticalHeaderLabels([f"Поставщик {i+1}" for i in range(sources)])

        for i in range(sources):
            for j in range(destinations):
                item = QTableWidgetItem(str(result_matrix[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.solution_table.setItem(i, j, item)
        
        summary = f"""=== Решение транспортной задачи ===
Метод: {"Метод потенциалов"}

Поставщики: {sources}
Потребители: {destinations}

Общая стоимость: {total_cost}

Распределение:
"""
        for i in range(sources):
            for j in range(destinations):
                value = self.solution_table.item(i, j).text()
                summary += f"Поставщик {i+1} → Потребитель {j+1}: {value} единиц\n"
        
        self.solution_text.setPlainText(summary)
        self.main_tabs.setCurrentIndex(1)  # Switch to solution tab
        self.show_status_message("Задача решена!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransportationSolver()
    window.show()
    sys.exit(app.exec())