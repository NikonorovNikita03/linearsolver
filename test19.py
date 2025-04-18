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
import styles


class TransportationSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение транспортной задачи")
        self.setGeometry(100, 100, 1366, 768)

        self.costs = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.supply = [0, 0, 0]
        self.demand = [0, 0, 0]
        
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
        
        self.main_tabs = QTabWidget()
        self.main_tabs.setStyleSheet(styles.mainTab)
        
        self.input_tab = QWidget()
        self.create_input_tables()
        
        self.solution_tab = QWidget()
        self.create_solution_tab()
        
        self.main_tabs.addTab(self.input_tab, "Исходные данные")
        self.main_tabs.addTab(self.solution_tab, "Решение")
        
        self.main_layout.addWidget(self.main_tabs)
        self.main_layout.addWidget(self.status_label)
        self.update_table_size()
    
    def create_controls(self):
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
        self.solve_btn.setStyleSheet(styles.solve_btn)
        self.solve_btn.clicked.connect(self.solve_problem)
        
        control_layout.addLayout(source_layout)
        control_layout.addLayout(dest_layout)
        control_layout.addLayout(method_layout)
        control_layout.addStretch()
        control_layout.addWidget(self.solve_btn)
        
        control_group.setLayout(control_layout)
        self.main_layout.addWidget(control_group)
    
    def create_input_tables(self):
        input_layout = QVBoxLayout()
        
        top_area = QHBoxLayout()
        
        costs_group = QGroupBox("Стоимости перевозок")
        costs_layout = QVBoxLayout()
        
        self.costs_table = QTableWidget()
        self.costs_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        
        header = self.costs_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setVisible(False)
        
        v_header = self.costs_table.verticalHeader()
        v_header.setSectionResizeMode(QHeaderView.Stretch)
        v_header.setDefaultAlignment(Qt.AlignCenter)
        v_header.setVisible(False)
        
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
        
        supply_group = QGroupBox("Запасы поставщиков")
        supply_layout = QVBoxLayout()
        
        self.supply_table = QTableWidget(1, 1)
        self.supply_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        
        s_header = self.supply_table.horizontalHeader()
        s_header.setSectionResizeMode(QHeaderView.Stretch)
        s_header.setDefaultAlignment(Qt.AlignCenter)
        s_header.setVisible(False)
        
        s_v_header = self.supply_table.verticalHeader()
        s_v_header.setSectionResizeMode(QHeaderView.Stretch)
        s_v_header.setDefaultAlignment(Qt.AlignCenter)
        s_v_header.setVisible(False)
        
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
        
        top_area.addWidget(costs_group, stretch=6)
        top_area.addWidget(supply_group, stretch=1)
        
        demand_container = QWidget()
        demand_layout = QHBoxLayout()
        
        demand_group = QGroupBox("Потребности потребителей")
        group_layout = QVBoxLayout()
        
        self.demand_table = QTableWidget(1, 1)
        self.demand_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        
        d_header = self.demand_table.horizontalHeader()
        d_header.setSectionResizeMode(QHeaderView.Stretch)
        d_header.setDefaultAlignment(Qt.AlignCenter)
        d_header.setVisible(False)
        
        d_v_header = self.demand_table.verticalHeader()
        d_v_header.setSectionResizeMode(QHeaderView.Stretch)
        d_v_header.setDefaultAlignment(Qt.AlignCenter)
        d_v_header.setVisible(False)
        
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
        
        demand_layout.addWidget(demand_group, 6)
        demand_layout.addStretch(1)
        
        demand_container.setLayout(demand_layout)
        
        input_layout.addLayout(top_area, stretch=7)
        input_layout.addWidget(demand_container, stretch=1)
        
        self.input_tab.setLayout(input_layout)
    
    def create_solution_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        splitter = QSplitter(Qt.Vertical)
        
        solution_group = QGroupBox("Оптимальное распределение")
        solution_layout = QVBoxLayout()
        solution_layout.setContentsMargins(5, 5, 5, 5)
        
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
        
        solution_layout.addWidget(self.solution_table)
        solution_layout.addLayout(btn_layout)
        solution_group.setLayout(solution_layout)
        
        summary_group = QGroupBox("Результаты")
        summary_layout = QVBoxLayout()
        summary_layout.setContentsMargins(5, 5, 5, 5)
        
        self.solution_text = QTextEdit()
        self.solution_text.setReadOnly(True)
        self.solution_text.setStyleSheet("font-family: monospace;")
        
        summary_layout.addWidget(self.solution_text)
        summary_group.setLayout(summary_layout)
        
        splitter.addWidget(solution_group)
        splitter.addWidget(summary_group)
        splitter.setSizes([500, 200])
        
        layout.addWidget(splitter)
        self.solution_tab.setLayout(layout)
    
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
                        
            if table == self.costs_table:
                self.source_spin.setValue(new_rows)
                self.dest_spin.setValue(new_cols)
            elif table == self.supply_table:
                self.source_spin.setValue(new_rows)
            elif table == self.demand_table:
                self.dest_spin.setValue(new_cols)
            
            self.show_status_message("Данные вставлены успешно!")
        except Exception as e:
            self.show_status_message(f"Ошибка при вставке данных: {str(e)}")
    
    def show_status_message(self, message):
        self.status_label.setText(message)
    
    def update_table_size(self):
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        
        for i in range(self.costs_table.rowCount()):
            for j in range(self.costs_table.columnCount()):
                if len(self.costs) <= i:
                    self.costs.append([0 for x in range(len(self.costs[0]))])
                if len(self.costs[0]) <= j:
                    for k in range(len(self.costs)):
                        self.costs[k].append(0)
                self.costs[i][j] = int(self.costs_table.item(i, j).text())
        
        for i in range(self.supply_table.rowCount()):
            if len(self.supply) <= i:
                self.supply.append(0)
            item = self.supply_table.item(i, 0)
            self.supply[i] = int(item.text()) if item else 0
        
        for j in range(self.demand_table.columnCount()):
            if len(self.demand) <= j:
                self.demand.append(0)
            item = self.demand_table.item(0, j)
            self.demand[j] = int(item.text()) if item else 0
        
        self.costs_table.setRowCount(sources)
        self.costs_table.setColumnCount(destinations)
        
        self.supply_table.setRowCount(sources)
        self.supply_table.setColumnCount(1)
        
        self.demand_table.setRowCount(1)
        self.demand_table.setColumnCount(destinations)
        
        for i in range(sources):
            for j in range(destinations):
                val = 0
                if len(self.costs) > i and len(self.costs[i]) > j:
                    val = self.costs[i][j]
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.costs_table.setItem(i, j, item)
        
        for i in range(sources):
            val = self.supply[i] if len(self.supply) > i else 0
            item = QTableWidgetItem(str(val))
            item.setTextAlignment(Qt.AlignCenter)
            self.supply_table.setItem(i, 0, item)
        
        for j in range(destinations):
            val = self.demand[j] if len(self.demand) > j else 0
            item = QTableWidgetItem(str(val))
            item.setTextAlignment(Qt.AlignCenter)
            self.demand_table.setItem(0, j, item)
    
    def extract_data(self):
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        
        costs = []
        supply = []
        demand = []
        
        for i in range(sources):
            row = []
            for j in range(destinations):
                item = self.costs_table.item(i, j)
                value = int(item.text()) if item and item.text().isdigit() else 0
                row.append(value)
            costs.append(row)
        
        for i in range(sources):
            item = self.supply_table.item(i, 0)
            value = int(item.text()) if item and item.text().isdigit() else 0
            supply.append(value)
        
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
        self.main_tabs.setCurrentIndex(1)
        self.show_status_message("Задача решена!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransportationSolver()
    window.show()
    sys.exit(app.exec())