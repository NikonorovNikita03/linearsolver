from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QGroupBox, QPushButton,
    QLabel, QSpinBox, QComboBox, QTextEdit, QMessageBox, QTabWidget, QStatusBar,
    QHeaderView
)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QClipboard, QIcon
from solver import Solver


class TransportationSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение транспортной задачи")
        self.setGeometry(100, 100, 800, 600)
        
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
        
        self.create_controls()
        self.create_input_table()
        self.create_solution_tabs()
        
        self.main_layout.addWidget(self.status_label)
        
        self.update_table_size()
    
    def create_controls(self):
        """Create control panel with problem setup options"""
        control_group = QGroupBox("Настройка задачи")
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(5, 5, 5, 5)
        control_layout.setSpacing(10)
        
        source_layout = QVBoxLayout()
        source_layout.setSpacing(0)
        source_layout.addWidget(QLabel("Поставщики:"))
        self.source_spin = QSpinBox()
        self.source_spin.setRange(1, 10)
        self.source_spin.setValue(3)
        self.source_spin.valueChanged.connect(self.update_table_size)
        source_layout.addWidget(self.source_spin)
        
        dest_layout = QVBoxLayout()
        dest_layout.setSpacing(0)
        dest_layout.addWidget(QLabel("Потребители:"))
        self.dest_spin = QSpinBox()
        self.dest_spin.setRange(1, 10)
        self.dest_spin.setValue(3)
        self.dest_spin.valueChanged.connect(self.update_table_size)
        dest_layout.addWidget(self.dest_spin)
        
        method_layout = QVBoxLayout()
        method_layout.setSpacing(0)
        method_layout.addWidget(QLabel("Метод:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Автоматически"
        ])
        method_layout.addWidget(self.method_combo)
        
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
        
        control_layout.addLayout(source_layout)
        control_layout.addLayout(dest_layout)
        control_layout.addLayout(method_layout)
        control_layout.addStretch()
        control_layout.addWidget(self.solve_btn)
        
        control_group.setLayout(control_layout)
        self.main_layout.addWidget(control_group)
    
    def create_input_table(self):
        """Create the main input table for all problem data"""
        input_group = QGroupBox("Исходные данные")
        layout = QVBoxLayout()
        
        self.input_table = QTableWidget()
        self.input_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        self.input_table.itemChanged.connect(self.update_balance_cell)
        
        header = self.input_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignCenter)
        
        v_header = self.input_table.verticalHeader()
        v_header.setSectionResizeMode(QHeaderView.Stretch)
        v_header.setDefaultAlignment(Qt.AlignCenter)
        
        btn_layout = QHBoxLayout()
        
        copy_btn = QPushButton("Копировать данные")
        copy_btn.setStyleSheet("background-color: #2196F3; color: white;")
        copy_btn.clicked.connect(lambda: self.copy_table_data(self.input_table))
        
        paste_btn = QPushButton("Вставить данные")
        paste_btn.setStyleSheet("background-color: #FF9800; color: white;")
        paste_btn.clicked.connect(self.paste_data_to_table)
        
        btn_layout.addStretch()
        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(paste_btn)
        
        layout.addWidget(self.input_table)
        layout.addLayout(btn_layout)
        input_group.setLayout(layout)
        self.main_layout.addWidget(input_group)
    
    def create_solution_tabs(self):
        self.tabs = QTabWidget()
        
        self.tabs.setStyleSheet("""
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
        
        self.solution_tab = QWidget()
        solution_layout = QVBoxLayout()
        
        self.solution_table = QTableWidget()
        self.solution_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.solution_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        
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
        
        solution_layout.addWidget(QLabel("Оптимальное распределение:"))
        solution_layout.addWidget(self.solution_table)
        solution_layout.addLayout(btn_layout)
        self.solution_tab.setLayout(solution_layout)
        
        self.summary_tab = QWidget()
        summary_layout = QVBoxLayout()
        
        self.solution_text = QTextEdit()
        self.solution_text.setReadOnly(True)
        self.solution_text.setStyleSheet("font-family: monospace;")
        
        summary_layout.addWidget(QLabel("Результаты:"))
        summary_layout.addWidget(self.solution_text)
        self.summary_tab.setLayout(summary_layout)
        
        self.tabs.addTab(self.solution_tab, "Распределение")
        self.tabs.addTab(self.summary_tab, "Результаты")
        
        self.main_layout.addWidget(self.tabs)
    
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
    
    def paste_data_to_table(self):
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
        
        self.input_table.itemChanged.disconnect(self.update_balance_cell)
        
        try:
            num_rows = len(data)
            num_cols = len(data[0]) if num_rows > 0 else 0
            
            self.source_spin.setValue(num_rows - 1)
            self.dest_spin.setValue(num_cols - 1)
            
            for row_idx in range(min(len(data), self.input_table.rowCount())):
                for col_idx in range(min(len(data[row_idx]), self.input_table.columnCount())):
                    if row_idx == self.input_table.rowCount()-1 and col_idx == self.input_table.columnCount()-1:
                        continue
                        
                    value = data[row_idx][col_idx]
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.input_table.setItem(row_idx, col_idx, item)
            
            self.show_status_message("Данные вставлены успешно!")
        except Exception as e:
            self.show_status_message(f"Ошибка при вставке данных: {str(e)}")
        finally:
            self.input_table.itemChanged.connect(self.update_balance_cell)
            self.update_balance_cell()
    
    def update_balance_cell(self):
        self.input_table.itemChanged.disconnect(self.update_balance_cell)
        
        try:
            sources = self.source_spin.value()
            destinations = self.dest_spin.value()
            
            total_supply = 0
            for i in range(sources):
                item = self.input_table.item(i, destinations)
                if item and item.text().isdigit():
                    total_supply += int(item.text())
            
            total_demand = 0
            for j in range(destinations):
                item = self.input_table.item(sources, j)
                if item and item.text().isdigit():
                    total_demand += int(item.text())
            
            balance = total_supply - total_demand
            balance_item = self.input_table.item(sources, destinations)
            if not balance_item:
                balance_item = QTableWidgetItem()
                balance_item.setFlags(balance_item.flags() & ~Qt.ItemIsEditable)
                balance_item.setTextAlignment(Qt.AlignCenter)
                self.input_table.setItem(sources, destinations, balance_item)
            
            balance_item.setText(str(balance))
            
            if balance > 0:
                balance_item.setBackground(Qt.green)
            elif balance < 0:
                balance_item.setBackground(Qt.red)
            else:
                balance_item.setBackground(Qt.white)
                
        except Exception as e:
            print(f"Error updating balance: {e}")
        finally:
            self.input_table.itemChanged.connect(self.update_balance_cell)
    
    def show_status_message(self, message):
        self.status_label.setText(message)
    
    def update_table_size(self):
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        
        self.input_table.itemChanged.disconnect(self.update_balance_cell)
        
        self.input_table.setRowCount(sources + 1)
        self.input_table.setColumnCount(destinations + 1)
        
        headers = [f"Потр. {j+1}" for j in range(destinations)] + ["Запасы"]
        self.input_table.setHorizontalHeaderLabels(headers)
        
        row_headers = [f"Пост. {i+1}" for i in range(sources)] + ["Потребности"]
        self.input_table.setVerticalHeaderLabels(row_headers)
        
        self.input_table.clearContents()
        
        for i in range(sources):
            for j in range(destinations):
                item = QTableWidgetItem("10")
                item.setTextAlignment(Qt.AlignCenter)
                self.input_table.setItem(i, j, item)
            
            item = QTableWidgetItem("100")
            item.setTextAlignment(Qt.AlignCenter)
            self.input_table.setItem(i, destinations, item)
        
        for j in range(destinations):
            item = QTableWidgetItem("80")
            item.setTextAlignment(Qt.AlignCenter)
            self.input_table.setItem(sources, j, item)
        
        balance_item = QTableWidgetItem()
        balance_item.setFlags(balance_item.flags() & ~Qt.ItemIsEditable)
        balance_item.setTextAlignment(Qt.AlignCenter)
        self.input_table.setItem(sources, destinations, balance_item)
        
        self.update_balance_cell()
        self.input_table.itemChanged.connect(self.update_balance_cell)
    
    def extract_data(self):
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        
        costs = []
        supply = []
        demand = []
        
        for i in range(sources):
            row = []
            for j in range(destinations):
                item = self.input_table.item(i, j)
                value = int(item.text()) if item and item.text().isdigit() else 0
                row.append(value)
            costs.append(row)
        
        for i in range(sources):
            item = self.input_table.item(i, destinations)
            value = int(item.text()) if item and item.text().isdigit() else 0
            supply.append(value)
        
        for j in range(destinations):
            item = self.input_table.item(sources, j)
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
        self.tabs.setCurrentIndex(0)
        self.show_status_message("Задача решена!")