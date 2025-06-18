import constants
from PySide6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QSpinBox, QVBoxLayout, QLabel,
    QTableWidget, QHeaderView, QTableWidgetItem, QGroupBox
)
from PySide6.QtCore import Qt
from functions import q_push_button, combine_arrays_1d_pure, combine_arrays_pure, input_field
from functions import brushes
from solver import Solver
class MultiobjectiveTransportationProblem():
    def __init__(self, size_x, size_y):
        self.table = QTableWidget()
        self.solution_table = QTableWidget()
        self.table.setStyleSheet("QTableWidget { font-size: 12px; }")
        self.group_top = QGroupBox()
        self.control_layout = QHBoxLayout()
        self.size_x = size_x
        self.size_y = size_y
        self.costs = []
        for y in range(self.size_y):
            self.costs.append([])
            for x in range(self.size_x):
                self.costs[y].append([0, 0])

        self.supply = [[0, 0] for x in range(self.size_y)]
        self.demand = [[0, 0] for x in range(self.size_x)]
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
        #self.solution_table.setStyleSheet(constants.solution_table_ss)
        
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
        self.source_spin.setRange(1, 10)
        self.source_spin.setValue(self.size_y)
        self.source_spin.valueChanged.connect(self.update_input_table)
        self.source_layout.addWidget(self.source_spin)
        
        self.dest_layout = QVBoxLayout()
        self.dest_layout.setSpacing(0)
        self.dest_layout.addWidget(QLabel("Потребители:"))
        self.dest_spin = QSpinBox()
        self.dest_spin.setRange(1, 10)
        self.dest_spin.setValue(self.size_x)
        self.dest_spin.valueChanged.connect(self.update_input_table)
        self.dest_layout.addWidget(self.dest_spin)
        
        self.menu_btn = q_push_button("Меню", constants.solve_btn)
        self.solve_btn = q_push_button("Решить", constants.solve_btn)

        self.variable_field_x = input_field("Название столбцов", text = self.variable_name_x, max_length = 20)
        self.variable_field_x.setFixedWidth(132)
        self.variable_field_y = input_field("Название строк", text = self.variable_name_y, max_length = 20)
        self.variable_field_y.setFixedWidth(132)
        self.variable_field_z = input_field("Название продуктов", text = "Продукт", max_length = 20)
        self.variable_field_z.setFixedWidth(132)

        self.variable_btn_x = q_push_button("Применить", constants.variant_btn)
        # self.variable_btn_x.clicked.connect(self.variable_name_changed_x)
        self.variable_btn_y = q_push_button("Применить", constants.variant_btn)
        # self.variable_btn_y.clicked.connect(self.variable_name_changed_y)
        self.variable_btn_z = q_push_button("Применить", constants.variant_btn)

        self.control_layout.addWidget(self.menu_btn)
        self.control_layout.addSpacing(10)
        self.control_layout.addLayout(self.source_layout)
        self.control_layout.addLayout(self.dest_layout)
        self.control_layout.addSpacing(10)
        self.control_layout.addWidget(self.variable_field_x)
        self.control_layout.addWidget(self.variable_btn_x)
        self.control_layout.addWidget(self.variable_field_y)
        self.control_layout.addWidget(self.variable_btn_y)
        self.control_layout.addWidget(self.variable_field_z)
        self.control_layout.addWidget(self.variable_btn_z)
        self.control_layout.addStretch()
        self.control_layout.addWidget(self.solve_btn)

        # self.control_layout.addLayout(self.source_layout)
        # self.control_layout.addLayout(self.dest_layout)
        # self.control_layout.addWidget(self.menu_btn)
        # self.control_layout.addStretch()
        # self.control_layout.addWidget(self.solve_btn)

        self.group_top.setLayout(self.control_layout)

    def update_table_size(self):  
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()

        self.size_x = destinations
        self.size_y = sources
        
        size_y = 3 + 2 * self.size_y
        size_x = 3 + 2 * self.size_x

        self.table.setRowCount(size_y)
        self.table.setColumnCount(size_x)

        if len(self.supply_labels) <= sources:
            for i in range(len(self.supply_labels), sources + 1):
                self.supply_labels.insert(i - 1, "Поставщик " + str(i))
                self.supply.append([0, 0])
                self.costs.append([[0, 0] for x in range(len(self.costs[0]))])

        if len(self.demand_labels) <= destinations:
            for j in range(len(self.demand_labels), destinations + 1):
                self.demand_labels.insert(j - 1, "Потребитель " + str(j))
                self.demand.append([0, 0])    
                for k in range(len(self.costs)):
                    self.costs[k].append([0, 0])
        
        for i in range(size_x):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        
        for i in range(size_y):
            self.table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
    
    def write_data_into_input_table(self):
        size_y = 3 + 2 * self.size_y
        size_x = 3 + 2 * self.size_x
        product_number = 2

        self.product_names = ["Продукт 1", "Продукт 2"]

        for i in range(product_number, size_x - 1, product_number):
            self.table.setSpan(0, i, 1, product_number)

        for i in range(product_number, size_y - 1, product_number):
            self.table.setSpan(i, 0, product_number, 1)
        
        to_write = [["" for i in range(size_x)]]

        to_write.append(["", ""])
        for i in range(self.size_x):
            to_write[1] += self.product_names
        to_write[1] += [""]

        for i in range(self.size_y):
            to_write.append(["" for x in range(size_x)])
            to_write.append(["" for x in range(size_x)])
            for j in range(len(self.costs[0])):
                to_write[2 * i + 2][2 + 2 * j] = self.costs[i][j][0]
                to_write[2 * i + 3][3 + 2 * j] = self.costs[i][j][1]

            to_write[2 * i + 2][1] = self.product_names[0]
            to_write[2 * i + 3][1] = self.product_names[1]

            to_write[2 * i + 2][-1] = self.supply[i][0]
            to_write[2 * i + 3][-1] = self.supply[i][1]

        to_write.append(["0" for x in range(size_x)])
        
        for i in range(self.size_x):
            to_write[-1][2 * i + 2] = self.demand[i][0]
            to_write[-1][2 * i + 3] = self.demand[i][1]
        
        to_write[-1][1] = ""
        to_write[-1][-1] = ""

        supply_counter = 0
        demand_counter = 0
        for y in range(size_y):
            for x in range(size_x):
                item = QTableWidgetItem(str(to_write[y][x]))
                if x == 0:
                    if y < 2 or y % product_number != 0:
                        continue
                    else:
                        item = QTableWidgetItem(self.supply_labels[supply_counter])
                        supply_counter += 1
                if y == 0:
                    if x < 2 or x % product_number != 0:
                        continue
                    else:
                        item = QTableWidgetItem(self.demand_labels[demand_counter])
                        demand_counter += 1
                if size_x - 1 > x > 1 and size_y - 1 > y > 1 and ((x % 2 == 0 and y % 2 == 1) or (x % 2 == 1 and y % 2 == 0)):
                    item.setBackground(brushes["black"])
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)

                font = item.font()
                font.setPointSize(17)
                item.setFont(font)

                self.table.setItem(y, x, item)

    def get_data_from_input_table(self):
        rows = self.table.rowCount()
        cols = self.table.columnCount()
            
        new_supply = []
        for row in range(self.size_y):
            item = [
                self.table.item(2 + row * 2, cols - 1),
                self.table.item(3 + row * 2, cols - 1)
            ]
            new_supply.append([
                int(item[0].text()) if item[0].text().isdigit() else 0,
                int(item[1].text()) if item[1].text().isdigit() else 0,
            ])

        
        new_demand = []
        for col in range(self.size_x):
            item = [
                self.table.item(rows - 1, 2 + col * 2),
                self.table.item(rows - 1, 3 + col * 2),
            ]
            new_demand.append([
                int(item[0].text()) if item[0].text().isdigit() else 0,
                int(item[1].text()) if item[1].text().isdigit() else 0,
            ])
        
        new_costs = []
        for row in range(self.size_y):
            cost_row = []
            for col in range(self.size_x):
                item = [
                    self.table.item(2 + row * 2, 2 + col * 2),
                    self.table.item(3 + row * 2, 3 + col * 2),
                ]
                cost_row.append([
                    int(item[0].text()) if item[0].text().isdigit() else 0,
                    int(item[1].text()) if item[1].text().isdigit() else 0,
                ])
            new_costs.append(cost_row)

        self.supply = combine_arrays_1d_pure(new_supply, self.supply)
        self.demand = combine_arrays_1d_pure(new_demand, self.demand)
        self.costs = combine_arrays_pure(new_costs, self.costs)

    def update_input_table(self):
        self.get_data_from_input_table()
        self.update_table_size()
        self.write_data_into_input_table()

    def solve(self):
        self.get_data_from_input_table()
        
        problem = Solver(self.supply, self.demand, self.costs)
        result_matrix, self.total_cost, info = problem.solve_transportation_scipy_double()

        size_y = 2 + 2 * len(result_matrix)
        size_x = 2 + 2 * len(result_matrix[0])

        self.solution_table.setRowCount(size_y)
        self.solution_table.setColumnCount(size_x - 1)

        for i in range(2, size_x - 2, 2):
            self.solution_table.setSpan(0, i, 1, 2)

        for i in range(2, size_y - 2, 2):
            self.solution_table.setSpan(i, 0, 2, 1)
        
        to_write = [["" for i in range(size_x)]]

        to_write.append(["", "'"])
        for i in range(self.size_x):
            to_write[1] += self.product_names
        to_write[1] += [""]

        for i in range(self.size_y):
            to_write.append(["0" for x in range(size_x)])
            to_write.append(["0" for x in range(size_x)])
            for j in range(len(result_matrix[0])):
                to_write[2 * i + 2][2 + 2 * j] = result_matrix[i][j][0]
                to_write[2 * i + 3][3 + 2 * j] = result_matrix[i][j][1]

            to_write[2 * i + 2][1] = self.product_names[0]
            to_write[2 * i + 3][1] = self.product_names[1]

        to_write.append(["0" for x in range(size_x)])

        multi_demand = self.demand_labels[:-1]
        if len(to_write[1]) < size_x:
            multi_demand.append('Фиктивный потребитель')

        multi_supply = self.supply_labels[:-1]
        if len(to_write) < size_y:
            multi_supply.append('Фиктивный поставщик')

        supply_counter = 0
        demand_counter = 0

        to_write[-1][1] = ""
        for y in range(size_y - 1):
            for x in range(size_x - 1):
                val = to_write[y][x]
                if isinstance(val, float):
                    val = "{0:g}".format(val)

                if y == 0 and x > 1 and x % 2 == 0:
                    val = multi_demand[demand_counter]
                    demand_counter += 1
                
                if x == 0 and y > 1 and y % 2 == 0:
                    val = multi_supply[supply_counter]
                    supply_counter += 1

                item = QTableWidgetItem(val)
                if size_x - 2 > x > 1 and size_y - 2 > y > 1 and ((x % 2 == 0 and y % 2 == 1) or (x % 2 == 1 and y % 2 == 0)):
                    item.setBackground(brushes["black"])
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    
                font = item.font()
                font.setPointSize(16)
                item.setFont(font)

                item.setTextAlignment(Qt.AlignCenter)
                self.solution_table.setItem(y, x, item)

        self.solution_table.setSpan(len(to_write), 0, 1, len(to_write[0]))
        item = QTableWidgetItem(f"Общая стоимость: {constants.stringify(self.total_cost)}")
        item.setTextAlignment(Qt.AlignCenter)
        font = item.font()
        font.setPointSize(16)
        item.setFont(font)
        self.solution_table.setItem(len(to_write), 0, QTableWidgetItem(item))
        