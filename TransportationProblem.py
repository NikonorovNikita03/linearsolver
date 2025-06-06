import constants
from PySide6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QSpinBox, QVBoxLayout, QLabel,
    QTableWidget, QHeaderView, QTableWidgetItem, QGroupBox
)
from PySide6.QtCore import Qt
from functions import q_push_button, combine_arrays_1d_pure, combine_arrays_pure, input_field, int_to_subscript
from solver import Solver

class TransportationProblem():
    def __init__(self, size_x, size_y):
        self.table = QTableWidget()
        self.solution_table = QTableWidget()
        self.table.setStyleSheet("QTableWidget { font-size: 12px; }")
        self.group_top = QGroupBox()
        self.control_layout = QHBoxLayout()
        self.size_x = size_x
        self.size_y = size_y
        self.costs = [[0 for x in range(self.size_x)] for y in range(self.size_y)]
        self.supply = [0 for y in range(self.size_y)]
        self.demand = [0 for x in range(self.size_x)]
        self.total_cost = 0
        self.supply_labels =  [f"Поставщик {x}" for x in range(1, self.size_y + 1)] + ["Потребители"]
        self.demand_labels = [f"Потребитель {x}" for x in range(1, self.size_x + 1)] + ["Поставщики"]

        self.variable_name_x = "x"
        self.variable_names_x = ["x₁", "x₂", "x₃"]
        self.variable_name_y = "y"
        self.variable_names_y = ["y₁", "y₂", "y₃"]
        self.variable_names_end_x = "Поставщики"
        self.variable_names_end_y = "Потребители"

        self.solution_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.solution_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        
        s_header = self.solution_table.horizontalHeader()
        s_header.setSectionResizeMode(QHeaderView.Stretch)
        s_header.setDefaultAlignment(Qt.AlignCenter)
        s_header.setStyleSheet(constants.solution_page_h_header_ss)
        
        s_v_header = self.solution_table.verticalHeader()
        s_v_header.setSectionResizeMode(QHeaderView.Stretch)
        s_v_header.setDefaultAlignment(Qt.AlignCenter)
        s_v_header.setStyleSheet(constants.solution_page_v_header_ss)

        self.set_top_layout()
        self.update_table_size()
        self.write_data_into_input_table()

    def set_top_layout(self):
        self.control_layout.setContentsMargins(5, 5, 5, 5)
        self.control_layout.setSpacing(10)
        
        self.source_layout = QVBoxLayout()
        self.source_layout.setSpacing(0)
        self.source_layout.addWidget(QLabel("Поставщики:"))
        self.source_spin = QSpinBox()
        self.source_spin.setRange(1, 50)
        self.source_spin.setValue(self.size_y)
        self.source_spin.valueChanged.connect(self.update_input_table)
        self.source_layout.addWidget(self.source_spin)
        
        self.dest_layout = QVBoxLayout()
        self.dest_layout.setSpacing(0)
        self.dest_layout.addWidget(QLabel("Потребители:"))
        self.dest_spin = QSpinBox()
        self.dest_spin.setRange(1, 50)
        self.dest_spin.setValue(self.size_x)
        self.dest_spin.valueChanged.connect(self.update_input_table)
        self.dest_layout.addWidget(self.dest_spin)
        
        self.menu_btn = q_push_button("Меню", constants.solve_btn)
        self.solve_btn = q_push_button("Решить", constants.solve_btn)

        self.variable_field_x = input_field("Название столбцов", text = self.variable_name_x, max_length = 20)
        self.variable_field_x.setFixedWidth(132)
        self.variable_field_y = input_field("Название строк", text = self.variable_name_y, max_length = 20)
        self.variable_field_y.setFixedWidth(132)

        self.variable_btn_x = q_push_button("Применить", constants.variant_btn)
        self.variable_btn_x.clicked.connect(self.variable_name_changed_x)
        self.variable_btn_y = q_push_button("Применить", constants.variant_btn)
        self.variable_btn_y.clicked.connect(self.variable_name_changed_y)

        self.control_layout.addWidget(self.menu_btn)
        self.control_layout.addSpacing(10)
        self.control_layout.addLayout(self.source_layout)
        self.control_layout.addLayout(self.dest_layout)
        self.control_layout.addSpacing(10)
        self.control_layout.addWidget(self.variable_field_x)
        self.control_layout.addWidget(self.variable_btn_x)
        self.control_layout.addWidget(self.variable_field_y)
        self.control_layout.addWidget(self.variable_btn_y)
        self.control_layout.addStretch()
        self.control_layout.addWidget(self.solve_btn)

        self.group_top.setLayout(self.control_layout)

    def variable_name_changed_x(self):
        self.update_input_table(refresh_names_x = True)
    
    def variable_name_changed_y(self):
        self.update_input_table(refresh_names_y = True)

    def update_table_size(self):  
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()

        self.size_x = destinations
        self.size_y = sources
        
        self.table.setRowCount(sources + 2)
        self.table.setColumnCount(destinations + 2)

        if len(self.supply_labels) <= sources:
            for i in range(len(self.supply_labels), sources + 1):
                self.variable_names_x.append(f"{self.variable_name_x}{int_to_subscript(i + 1)}")
                self.supply.append(0)
                self.costs.append([0 for x in range(len(self.costs[0]))])

        if len(self.demand_labels) <= destinations:
            for j in range(len(self.demand_labels), destinations + 1):
                self.variable_names_y.append(f"{self.variable_name_y}{int_to_subscript(j + 1)}")
                self.demand.append(0)    
                for k in range(len(self.costs)):
                    self.costs[k].append(0)
        
        for i in range(destinations + 2):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        
        for i in range(sources + 2):
            self.table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
    
    def write_data_into_input_table(self):
        sources = self.size_y
        destinations = self.size_x
        self.table.setRowCount(sources + 2)
        self.table.setColumnCount(destinations + 2)

        to_write = [[""] + self.variable_names_x[0:self.size_x] + [self.variable_names_end_y]]
        for i in range(0, sources):
            this = [self.variable_names_y[i]] + self.costs[i][0:destinations] + [self.supply[i]]
            to_write.append(this)
        to_write.append([self.variable_names_end_x] + self.demand + [""])

        for y in range(sources + 2):
            for x in range(destinations + 2):
                item = QTableWidgetItem(str(to_write[y][x]))
                item.setTextAlignment(Qt.AlignCenter)

                font = item.font()
                font.setPointSize(20)
                item.setFont(font)

                self.table.setItem(y, x, item)

    def get_data_from_input_table(self, refresh_names_x = False, refresh_names_y = False):
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        
        if rows < 3 or cols < 3: 
            raise ValueError("Таблица должна содержать хотя бы одного поставщика и потребителя")
        
        sources = rows - 2
        destinations = cols - 2

        if refresh_names_x:
            x = self.dest_spin.value()
            self.variable_name = self.variable_field_x.line.text()
            self.variable_names = [f"{self.variable_name}{int_to_subscript(i)}" for i in range(1, x + 1)]
        else:
            new_variable_names = []
            for col in range(1, self.table.columnCount()):
                item = self.table.item(0, col)
                if item:
                    new_variable_names.append(item.text())
                else:
                    new_variable_names.append("")
            self.variable_names_x = combine_arrays_1d_pure(new_variable_names, self.variable_names_x)

        if refresh_names_y:
            y = self.source_spin.value()
            self.variable_name_y = self.variable_field_y.line.text()
            self.variable_names_y = [f"{self.variable_name_y}{int_to_subscript(i)}" for i in range(1, y + 1)]
        else:
            new_variable_names_y = []
            for row in range(1, self.table.rowCount()):
                item = self.table.item(row, 0)
                if item:
                    new_variable_names_y.append(item.text())
            self.variable_names_y = combine_arrays_1d_pure(new_variable_names_y, self.variable_names_y)
            
        new_supply = []
        for row in range(1, sources + 1):
            item = self.table.item(row, destinations + 1)
            new_supply.append(int(item.text()) if item and item.text().isdigit() else 0)
        
        new_demand = []
        for col in range(1, destinations + 1):
            item = self.table.item(sources + 1, col)
            new_demand.append(int(item.text()) if item and item.text().isdigit() else 0)
        
        new_costs = []
        for row in range(1, sources + 1):
            cost_row = []
            for col in range(1, destinations + 1):
                item = self.table.item(row, col)
                cost_row.append(int(item.text()) if item and item.text().isdigit() else 0)
            new_costs.append(cost_row)

        self.supply = combine_arrays_1d_pure(new_supply, self.supply)
        self.demand = combine_arrays_1d_pure(new_demand, self.demand)
        self.costs = combine_arrays_pure(new_costs, self.costs)

    def update_input_table(self, number = 0, refresh_names_x = False, refresh_names_y = False):
        self.get_data_from_input_table(refresh_names_x, refresh_names_y)
        self.update_table_size()
        self.write_data_into_input_table()

    def solve(self):
        self.get_data_from_input_table()
        costs, supply, demand = self.costs, self.supply, self.demand

        supply = supply[0:self.size_y]
        demand = demand[0:self.size_x]
        costs = [row[0:self.size_x] for row in costs[0:self.size_y]]

        problem = Solver(supply, demand, costs)
        result_matrix, self.total_cost = problem.solve_transportation_scipy()

        sources = len(result_matrix)
        destinations = len(result_matrix[0]) if sources > 0 else 0

        to_write = [[""] + self.variable_names_x[0:self.size_x]]

        if destinations > self.size_x:
            to_write[0].append("Фиктивный потребитель")

        for i in range(0, self.size_y):
            this = [self.variable_names_y[i]] + result_matrix[i].tolist()
            to_write.append(this)
    
        if sources > self.size_y:
            to_write.append(["Фиктивный поставщик"] + result_matrix[-1].tolist())
        
        self.solution_table.setRowCount(len(to_write) + 1)
        self.solution_table.setColumnCount(len(to_write[0]))

        for i in range(len(to_write[0])):
            self.solution_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        
        for i in range(len(to_write)):
            self.solution_table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        for y in range(len(to_write)):
            for x in range(len(to_write[0])):
                val = to_write[y][x]
                if isinstance(val, float):
                    val = "{0:g}".format(val)
                val = val.replace('-', '')
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)

                font = item.font()
                font.setPointSize(20)
                item.setFont(font)

                self.solution_table.setItem(y, x, item)
        
        self.solution_table.setSpan(len(to_write), 0, 1, len(to_write[0]))
        item = QTableWidgetItem(f"Общая стоимость: {constants.stringify(self.total_cost)}")
        item.setTextAlignment(Qt.AlignCenter)
        font = item.font()
        font.setPointSize(20)
        item.setFont(font)
        self.solution_table.setItem(len(to_write), 0, QTableWidgetItem(item))
