import sys
import csv
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QGroupBox, QPushButton,
    QLabel, QSpinBox, QMessageBox,  QTextEdit, QFileDialog,
    QHeaderView, QStackedWidget
)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QIcon
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
        self.create_input_tables()
        
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
        self.write_data_into_input_tables()
    
    def q_push_button(self, name, style, function, cursor = True):
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
        self.source_spin.valueChanged.connect(self.update_input_tables)
        source_layout.addWidget(self.source_spin)
        
        dest_layout = QVBoxLayout()
        dest_layout.setSpacing(0)
        dest_layout.addWidget(QLabel("Потребители:"))
        self.dest_spin = QSpinBox()
        self.dest_spin.setRange(1, 10)
        self.dest_spin.setValue(3)
        self.dest_spin.valueChanged.connect(self.update_input_tables)
        dest_layout.addWidget(self.dest_spin)
        
        self.text_input_btn = self.q_push_button("Ввести текстом", constants.text_input_btn, self.show_text_input_page)
        self.solve_btn = self.q_push_button("Решить", constants.solve_btn, self.solve_problem)
        
        self.back_btn = QPushButton("Назад")
        self.back_btn.setFixedHeight(60)
        self.back_btn.setStyleSheet("background-color: #607D8B; color: white;")
        self.back_btn.clicked.connect(self.show_input_page)
        self.back_btn.setVisible(False)
        
        control_layout.addLayout(source_layout)
        control_layout.addLayout(dest_layout)
        control_layout.addStretch()
        control_layout.addWidget(self.text_input_btn)
        control_layout.addWidget(self.back_btn)
        control_layout.addWidget(self.solve_btn)
        
        self.control_group.setLayout(control_layout)
        self.main_layout.addWidget(self.control_group)

    def process_text_input(self):
        #self.show_status_message("Данные введены (заглушка)")
        tpp = TransportProblemParser(self.text_edit.toPlainText())
        print(tpp.parse_transport_problem())
        self.show_input_page()
    
    def show_text_input_page(self):        
        self.control_group.setVisible(False)
        self.stacked_widget.setCurrentIndex(2)
        self.solve_btn.setVisible(False)
        self.back_btn.setVisible(False)
        self.text_input_btn.setVisible(False)
    
    def show_input_page(self):        
        self.control_group.setVisible(True)
        self.stacked_widget.setCurrentIndex(0)
        self.solve_btn.setVisible(True)
        self.back_btn.setVisible(False)
        self.text_input_btn.setVisible(True)
    
    def show_solution_page(self):
        self.control_group.setVisible(True)
        self.stacked_widget.setCurrentIndex(1)
        self.solve_btn.setVisible(False)
        self.back_btn.setVisible(True)
        self.text_input_btn.setVisible(False)
    
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

        costs_copy_btn = self.q_push_button("Копировать", "background-color: #2196F3; color: white;", lambda: self.copy_table_data(self.costs_table))
        costs_paste_btn = self.q_push_button("Вставить", "background-color: #FF9800; color: white;", lambda: self.paste_data_to_table(self.costs_table))
        
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

        supply_copy_btn = self.q_push_button("Копировать", "background-color: #2196F3; color: white;", lambda: self.copy_table_data(self.supply_table))
        supply_paste_btn = self.q_push_button("Вставить", "background-color: #FF9800; color: white;", lambda: self.paste_data_to_table(self.supply_table))
        
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

        demand_copy_btn = self.q_push_button("Копировать", "background-color: #2196F3; color: white;", lambda: self.copy_table_data(self.demand_table))
        demand_paste_btn = self.q_push_button("Вставить", "background-color: #FF9800; color: white;", lambda: self.paste_data_to_table(self.demand_table))
        
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
        
        self.input_page.setLayout(input_layout)
    
    def create_solution_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
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

        self.total_cost_label = QLabel("Общая стоимость: -")
        self.total_cost_label.setAlignment(Qt.AlignCenter)
        self.total_cost_label.setStyleSheet(constants.total_cost_label)
        
        btn_layout = QHBoxLayout()
        
        solution_copy_btn = QPushButton("Копировать решение")
        solution_copy_btn.setStyleSheet("background-color: #2196F3; color: white;")
        solution_copy_btn.clicked.connect(lambda: self.copy_table_data(self.solution_table))
        
        self.export_csv_btn = QPushButton("Выгрузить CSV")
        self.export_csv_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        self.export_csv_btn.clicked.connect(self.export_solution_to_csv)
        
        btn_layout.addStretch()
        btn_layout.addWidget(solution_copy_btn)
        btn_layout.addWidget(self.export_csv_btn)
        
        solution_layout.addWidget(self.solution_table)
        solution_layout.addWidget(self.total_cost_label)
        solution_layout.addLayout(btn_layout)
        solution_group.setLayout(solution_layout)
        
        layout.addWidget(solution_group)
        self.solution_page.setLayout(layout)
    
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
    
    def get_data_from_input_tables(self):
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

    def write_data_into_input_tables(self):
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()

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
    
    def update_table_size(self):
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        
        self.costs_table.setRowCount(sources)
        self.costs_table.setColumnCount(destinations)
        
        self.supply_table.setRowCount(sources)
        self.supply_table.setColumnCount(1)
        
        self.demand_table.setRowCount(1)
        self.demand_table.setColumnCount(destinations)     

    def update_input_tables(self):
        self.get_data_from_input_tables()
        self.update_table_size()
        self.write_data_into_input_tables()  

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
        result_matrix, self.total_cost = problem.solve_transportation_scipy()

        sources, destinations = len(result_matrix), len(result_matrix[0])

        self.solution_table.setRowCount(sources)
        self.solution_table.setColumnCount(destinations)
        
        header = self.solution_table.horizontalHeader()
        header.setVisible(False)

        v_header = self.solution_table.verticalHeader()
        v_header.setVisible(False)

        for i in range(sources):
            for j in range(destinations):
                item = QTableWidgetItem(constants.stringify(result_matrix[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.solution_table.setItem(i, j, item)
        
        self.total_cost_label.setText(f"Общая стоимость: {constants.stringify(self.total_cost)}")
        
        self.show_solution_page()
        self.show_status_message("Задача решена!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransportationSolver()
    window.show()
    sys.exit(app.exec())