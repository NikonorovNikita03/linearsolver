import constants
from PySide6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QSpinBox, QVBoxLayout, QLabel
)

class TransportationProblem():
    def __init__(self, size_x, size_y, q_push_button):
        self.size_x = size_x
        self.size_y = size_y
        self.q_push_button = q_push_button
        self.costs = [[0 for x in range(self.size_x)] for y in range(self.size_y)]
        self.supply = [0 for y in range(self.size_y)]
        self.demand = [0 for x in range(self.size_x)]
        self.total_cost = 0

    def get_top_layout(self):
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(5, 5, 5, 5)
        control_layout.setSpacing(10)
        
        self.source_layout = QVBoxLayout()
        self.source_layout.setSpacing(0)
        self.source_layout.addWidget(QLabel("Поставщики:"))
        self.source_spin = QSpinBox()
        self.source_spin.setRange(1, 10)
        self.source_spin.setValue(self.size_y)
        #self.source_spin.valueChanged.connect(self.update_input_table)
        self.source_layout.addWidget(self.source_spin)
        
        self.dest_layout = QVBoxLayout()
        self.dest_layout.setSpacing(0)
        self.dest_layout.addWidget(QLabel("Потребители:"))
        self.dest_spin = QSpinBox()
        self.dest_spin.setRange(1, 10)
        self.dest_spin.setValue(self.size_x)
        #self.dest_spin.valueChanged.connect(self.update_input_table)
        self.dest_layout.addWidget(self.dest_spin)
        
        #self.text_input_btn = self.q_push_button("Ввести текстом", constants.text_input_btn, self.show_text_input_page)
        self.solve_btn = self.q_push_button("Решить", constants.solve_btn)
        
        #self.solve
        #self.multiproduct_btn = self.q_push_button("Мультипродуктовая задача", constants.multiproduct_btn_ss, self.show_multiproduct_table)
        #self.examples_btn = self.q_push_button("Примеры", constants.examples_btn_ss, self.show_examples_page)
        
        #self.back_btn = self.q_push_button("Назад", constants.back_btn_ss, self.show_input_page)
        #self.back_btn.setVisible(False)
        

        control_layout.addLayout(self.source_layout)
        control_layout.addLayout(self.dest_layout)
        control_layout.addStretch()
        control_layout.addWidget(self.solve_btn)
        

        return control_layout
        #control_layout.addWidget(self.text_input_btn)
        # control_layout.addWidget(self.back_btn)
        # control_layout.addWidget(self.examples_btn)
        
        #control_layout.addWidget(self.multiproduct_btn)

    def update_table_size(self, table):
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()

        self.size_x = destinations
        self.size_y = sources
        
        self.combined_table.setRowCount(sources + 2)
        self.combined_table.setColumnCount(destinations + 2)

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
            self.combined_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        
        for i in range(sources + 2):
            self.combined_table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)