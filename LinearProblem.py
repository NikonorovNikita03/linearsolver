import constants
from PySide6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QSpinBox, QVBoxLayout, QLabel, QWidget,
    QTableWidget, QHeaderView, QTableWidgetItem, QGroupBox, QComboBox,
)
from PySide6.QtGui import QTextDocument, QTextCursor
from PySide6.QtCore import Qt
from functions import q_push_button, combine_arrays_1d_pure, combine_arrays_pure, input_field, int_to_subscript, print_table
from scipy.optimize import linprog

class LinearProblem():
    def __init__(self, size_x = 3, size_y = 3):
        self.table = QTableWidget()
        self.solution_table = QTableWidget()
        self.table.setStyleSheet("QTableWidget { font-size: 12px; }")
        self.group_top = QGroupBox()
        self.control_layout = QHBoxLayout()
        self.variable_name = "x"
        self.problem_type = "min"
        self.size_x = size_x
        self.size_y = size_y
        self.costs = [[0.02 for x in range(self.size_x)] for y in range(self.size_y)]
        self.function = [0 for y in range(self.size_y)]
        self.constraints = [0 for x in range(self.size_x)]
        self.signs = [">=" for x in range(self.size_x)]
        self.total_cost = 0
        # self.supply_labels =  [f"Поставщик {x}" for x in range(1, self.size_y + 1)] + ["Потребители"]
        # self.demand_labels = [f"Потребитель {x}" for x in range(1, self.size_x + 1)] + ["Поставщики"]

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
        self.source_layout.addWidget(QLabel("Количество<br>ограничений:"))
        self.source_spin = QSpinBox()
        self.source_spin.setRange(1, 50)
        self.source_spin.setValue(self.size_y)
        self.source_spin.valueChanged.connect(self.update_input_table)
        self.source_layout.addWidget(self.source_spin)
        
        self.dest_layout = QVBoxLayout()
        self.dest_layout.setSpacing(0)
        self.dest_layout.addWidget(QLabel("Количество<br>переменных:"))
        self.dest_spin = QSpinBox()
        self.dest_spin.setRange(1, 50)
        self.dest_spin.setValue(self.size_x)
        self.dest_spin.valueChanged.connect(self.update_input_table)
        self.dest_layout.addWidget(self.dest_spin)

        self.variable_field = input_field("Название переменной", text = self.variable_name, max_length = 5)
        self.variable_field.setFixedWidth(132)
        
        self.menu_btn = q_push_button("Меню", constants.solve_btn)
        self.solve_btn = q_push_button("Решить", constants.solve_btn)

        self.control_layout.addLayout(self.source_layout)
        self.control_layout.addLayout(self.dest_layout)
        self.control_layout.addWidget(self.menu_btn)
        self.control_layout.addWidget(self.variable_field)
        self.control_layout.addStretch()
        self.control_layout.addWidget(self.solve_btn)

        self.group_top.setLayout(self.control_layout)

    def update_table_size(self):  
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()

        self.size_x = destinations
        self.size_y = sources

        if len(self.function) < self.size_x:
            for i in range(self.size_x - len(self.function)):
                self.function.append(0)
        
        if len(self.costs) < self.size_y:
            for i in range(self.size_y - len(self.costs)):
                self.signs.append(">=")
                self.costs.append([0 for x in range(self.size_x)])

        if len(self.constraints) < len(self.costs):
            for i in range(len(self.costs) - len(self.constraints)):
                self.constraints.append(0)
        
        while len(self.costs[0]) < self.size_x:
            for i in range(self.size_y):
                self.costs[i].append(0)

        column_count = self.table.columnCount()
        for i in range(2, self.table.rowCount()):
            self.table.removeCellWidget(i, column_count - 2)
        
        self.table.setRowCount(sources + 2)
        self.table.setColumnCount(destinations + 2)

        # if len(self.supply_labels) <= sources:
        #     for i in range(len(self.supply_labels), sources + 1):
        #         self.supply_labels.insert(i - 1, "Поставщик " + str(i))
        #         self.supply.append(0)
        #         self.costs.append([0 for x in range(len(self.costs[0]))])

        # if len(self.demand_labels) <= destinations:
        #     for j in range(len(self.demand_labels), destinations + 1):
        #         self.demand_labels.insert(j - 1, "Потребитель " + str(j))
        #         self.demand.append(0)    
        #         for k in range(len(self.costs)):
        #             self.costs[k].append(0)
        
        for i in range(destinations + 2):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        
        for i in range(sources + 2):
            self.table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
    
    def write_data_into_input_table(self):
        self.table.setRowCount(self.size_y + 2)
        self.table.setColumnCount(self.size_x + 2)

        self.variable_field.line.setText(self.variable_name)

        to_write = [[""] + [f"{self.variable_name}{int_to_subscript(i)}" for i in range(1, self.size_x+1)] + [""]]
        to_write.append([f"F ({self.variable_name}) = "] + [f"{x:g}" for x in self.function[0:self.size_x]] + [""])

        for i in range(0, self.size_y):
            this = [f"{x:g}" for x in self.costs[i][0:self.size_x]] + [self.signs[i]] + [f"{self.constraints[i]:g}"]
            to_write.append(this)
        
        for y in range(self.size_y + 2):
            for x in range(self.size_x + 2):
                if x == 0 and y == 0:
                    problem_widget = QComboBox()
                    problem_widget.addItems(["Минимизация", "Максимизация"])
                    problem_widget.setStyleSheet("QComboBox {font-size: 20px;}")

                    if self.problem_type != "min":
                        problem_widget.setCurrentText("Максимизация")
                    else:
                        problem_widget.setCurrentText("Минимизация")
                    
                    self.table.setCellWidget(0, 0, problem_widget)
                    continue
                if to_write[y][x] in [">=", "=", "<="]:
                    list_widget = QComboBox()
                    list_widget.setStyleSheet("QComboBox {font-size: 25px;}")
                    list_widget.addItems([">=", "=", "<="])
                    list_widget.setCurrentText(to_write[y][x])
                    self.table.setCellWidget(y, x, list_widget)
                else:
                    item = QTableWidgetItem(str(to_write[y][x]))
                    if y == 0 or (y == 1 and x == 0): 
                        font = item.font()
                        font.setPointSize(20)
                        item.setFont(font)

                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(y, x, item)

    def get_data_from_input_table(self):
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        
        if rows < 3 or cols < 3: 
            raise ValueError("Таблица должна содержать хотя бы одного поставщика и потребителя")
        
        sources = rows - 2
        destinations = cols - 2

        # new_demand_labels = []
        # for col in range(1, destinations + 2):
        #     item = self.table.item(0, col)
        #     new_demand_labels.append(item.text())
        
        # new_supply_labels = []
        # for row in range(1, sources + 2):
        #     item = self.table.item(row, 0)
        #     new_supply_labels.append(item.text())
            
        # new_supply = []
        # for row in range(1, sources + 1):
        #     item = self.table.item(row, destinations + 1)
        #     new_supply.append(int(item.text()) if item and item.text().isdigit() else 0)
        
        # new_demand = []
        # for col in range(1, destinations + 1):
        #     item = self.table.item(sources + 1, col)
        #     new_demand.append(int(item.text()) if item and item.text().isdigit() else 0)

        if self.table.cellWidget(0, 0).currentText() != "Минимизация":
            self.problem_type = "max"
        else:
            self.problem_type = "min"

        new_constraints = []
        new_signs = []
        for row in range(2, rows):
            item = self.table.item(row, cols - 1)
            try:
                val = float(item.text())
                new_constraints.append(val)
            except:
                self.error = "Введённое значение не является числом"
            list_widget = self.table.cellWidget(row, cols - 2)
            new_signs.append(list_widget.currentText() if list_widget else ">=")

        new_function = []
        for col in range(1, cols):
            item = self.table.item(1, col)
            try:
                val = float(item.text())
                new_function.append(val)
            except:
                self.error = "Введённое значение не является числом"
        
        new_costs = []
        for row in range(2, sources + 2):
            cost_row = []
            for col in range(destinations):
                item = self.table.item(row, col)
                try:
                    val = float(item.text())
                    cost_row.append(val)
                except:
                    self.error = "Введённое значение не является числом"
            new_costs.append(cost_row)

        # self.supply = combine_arrays_1d_pure(new_supply, self.supply)
        # self.demand = combine_arrays_1d_pure(new_demand, self.demand)
        self.function = combine_arrays_1d_pure(new_function, self.function)
        self.constraints = combine_arrays_1d_pure(new_constraints, self.constraints)
        self.signs = combine_arrays_1d_pure(new_signs, self.signs)
        self.costs = combine_arrays_pure(new_costs, self.costs)
        # self.supply_labels = combine_arrays_1d_pure(new_supply_labels[0:-1], self.supply_labels)
        # self.demand_labels = combine_arrays_1d_pure(new_demand_labels[0:-1], self.demand_labels)

    def update_input_table(self):
        self.get_data_from_input_table()
        self.update_table_size()
        self.write_data_into_input_table()

    def solve(self):
        self.get_data_from_input_table()
        # costs, supply, demand = self.costs, self.supply, self.demand
        
        # problem = Solver(supply, demand, costs)
        # result_matrix, self.total_cost = problem.solve_transportation_scipy()


        # sources = len(result_matrix)
        # destinations = len(result_matrix[0]) if sources > 0 else 0

        print(self.function)
        print(self.costs)
        print(self.signs)
        print(self.constraints)

        max = self.table.cellWidget(0, 0).currentText() != "Минимизация"

        if max:
            for i in range(len(self.function)):
                self.function[i] = -self.function[i]
        
        A_ub = []
        b_ub = []
        A_eq = []
        b_eq = []
        for i in range(self.size_y):
            match self.signs[i]:
                case "<=":
                    A_ub.append(self.costs[i])
                    b_ub.append(self.constraints[i])
                case ">=":
                    A_ub.append([-x for x in self.costs[i]])
                    b_ub.append(-self.constraints[i])
                case "=":
                    A_eq.append(self.costs[i])
                    b_eq.append(self.constraints[i])
                case _:
                    continue

        result = linprog(
            c=self.function,
            A_ub=A_ub,
            b_ub=b_ub,
            A_eq=A_eq,
            b_eq=b_eq,
            bounds=[(0, None) for x in range(self.size_x)],
            method='highs'
        )
        
        answer = [-result.fun if max else result.fun, result.x]

        #to_write = [[""] + self.demand_labels[0:self.size_x]]
        to_write = [[f"{self.variable_name}{int_to_subscript(i)}" for i in range(1, self.size_x+1)]]
        to_write.append([])
        for i in range(self.size_x):
            to_write[1] = answer[1]

        # if destinations > self.size_x:
        #     to_write[0].append("Фиктивный потребитель")

        # for i in range(0, self.size_y):
        #     this = [self.supply_labels[i]] + result_matrix[i].tolist()
        #     to_write.append(this)
    
        # if sources > self.size_y:
        #     to_write.append(["Фиктивный поставщик"] + result_matrix[-1].tolist())
        
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
                item = QTableWidgetItem(val)
                if y == 0: 
                    font = item.font()
                    font.setPointSize(20)
                    item.setFont(font)
                item.setTextAlignment(Qt.AlignCenter)
                self.solution_table.setItem(y, x, item)
        
        self.solution_table.setSpan(len(to_write), 0, 1, len(to_write[0]))
        item = QTableWidgetItem(f"Экстремум функции: {constants.stringify(answer[0])}")
        item.setTextAlignment(Qt.AlignCenter)
        self.solution_table.setItem(len(to_write), 0, QTableWidgetItem(item))
