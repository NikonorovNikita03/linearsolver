import constants
from PySide6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QSpinBox, QVBoxLayout, QLabel,
    QTableWidget, QHeaderView, QTableWidgetItem, QGroupBox
)
from PySide6.QtCore import Qt
from functions import q_push_button, combine_arrays_1d_pure, combine_arrays_pure
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
        
        #self.text_input_btn = self.q_push_button("Ввести текстом", constants.text_input_btn, self.show_text_input_page)
        self.menu_btn = q_push_button("Меню", constants.solve_btn)
        self.solve_btn = q_push_button("Решить", constants.solve_btn)
        
        #self.solve
        #self.multiproduct_btn = self.q_push_button("Мультипродуктовая задача", constants.multiproduct_btn_ss, self.show_multiproduct_table)
        #self.examples_btn = self.q_push_button("Примеры", constants.examples_btn_ss, self.show_examples_page)
        
        #self.back_btn = self.q_push_button("Назад", constants.back_btn_ss, self.show_input_page)
        #self.back_btn.setVisible(False)
        

        self.control_layout.addLayout(self.source_layout)
        self.control_layout.addLayout(self.dest_layout)
        self.control_layout.addWidget(self.menu_btn)
        self.control_layout.addStretch()
        self.control_layout.addWidget(self.solve_btn)

        self.group_top.setLayout(self.control_layout)
        #control_layout.addWidget(self.text_input_btn)
        # control_layout.addWidget(self.back_btn)
        # control_layout.addWidget(self.examples_btn)
        
        #control_layout.addWidget(self.multiproduct_btn)

    def update_table_size(self):  
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()

        self.size_x = destinations
        self.size_y = sources
        
        self.table.setRowCount(sources + 2)
        self.table.setColumnCount(destinations + 2)

        if len(self.supply_labels) <= sources:
            for i in range(len(self.supply_labels), sources + 1):
                self.supply_labels.insert(i - 1, "Поставщик " + str(i))
                self.supply.append(0)
                self.costs.append([0 for x in range(len(self.costs[0]))])

        if len(self.demand_labels) <= destinations:
            for j in range(len(self.demand_labels), destinations + 1):
                self.demand_labels.insert(j - 1, "Потребитель " + str(j))
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

        to_write = [[""] + self.demand_labels[0:destinations] + [self.demand_labels[-1]]]
        for i in range(0, sources):
            this = [self.supply_labels[i]] + self.costs[i][0:destinations] + [self.supply[i]]
            to_write.append(this)
        to_write.append([self.demand_labels[-1]] + self.demand + [""])

        for y in range(sources + 2):
            for x in range(destinations + 2):
                item = QTableWidgetItem(str(to_write[y][x]))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(y, x, item)
        
        #self.highlight_table_regions()

    def get_data_from_input_table(self):
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        
        if rows < 3 or cols < 3:  # Минимум 1 поставщик, 1 потребитель + заголовки
            raise ValueError("Таблица должна содержать хотя бы одного поставщика и потребителя")
        
        sources = rows - 2
        destinations = cols - 2

        new_demand_labels = []
        for col in range(1, destinations + 2):
            item = self.table.item(0, col)
            new_demand_labels.append(item.text())
        
        new_supply_labels = []
        for row in range(1, sources + 2):
            item = self.table.item(row, 0)
            new_supply_labels.append(item.text())
            
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
        self.supply_labels = combine_arrays_1d_pure(new_supply_labels[0:-1], self.supply_labels)
        self.demand_labels = combine_arrays_1d_pure(new_demand_labels[0:-1], self.demand_labels)

    def update_input_table(self):
        self.get_data_from_input_table()
        self.update_table_size()
        self.write_data_into_input_table()

    def solve(self):
        self.get_data_from_input_table()
        costs, supply, demand = self.costs, self.supply, self.demand
        
        problem = Solver(supply, demand, costs)
        result_matrix, self.total_cost = problem.solve_transportation_scipy()

        sources = len(result_matrix)
        destinations = len(result_matrix[0]) if sources > 0 else 0

        to_write = [[""] + self.demand_labels[0:self.size_x]]

        if destinations > self.size_x:
            to_write[0].append("Фиктивный потребитель")

        for i in range(0, self.size_y):
            this = [self.supply_labels[i]] + result_matrix[i].tolist()
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
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                self.solution_table.setItem(y, x, item)
        
        self.solution_table.setSpan(len(to_write), 0, 1, len(to_write[0]))
        item = QTableWidgetItem(f"Общая стоимость: {constants.stringify(self.total_cost)}")
        item.setTextAlignment(Qt.AlignCenter)
        self.solution_table.setItem(len(to_write), 0, QTableWidgetItem(item))
        
        #self.total_cost_label.setText(f"Общая стоимость: {constants.stringify(self.total_cost)}")
        #self.highlight_solution_table()
        
    #     self.show_solution_page()
    #     self.show_status_message("Задача решена!")