import sys
import csv
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QGroupBox, QPushButton, QSizePolicy,
    QLabel, QSpinBox, QMessageBox, QFileDialog, QStackedWidget, QHeaderView
)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QIcon, QColor, QBrush
from solver import Solver
from TransportationProblem import TransportationProblem
import constants
import functions


class TransportationSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение транспортных задач линейного программирования")
        self.settings = functions.get_settings()
        self.page = "main"
        self.problem_type = ""
        self.setGeometry(100, 100, self.settings["width"], self.settings["height"])

        self.transportation_problem = TransportationProblem(3, 3, self.q_push_button)

        self.product_names = ["Продукт 1", "Продукт 2"]

        self.multi_costs = []
        for y in range(self.settings["size_y"]):
            self.multi_costs.append([])
            for x in range(self.settings['size_x']):
                self.multi_costs[y].append([0, 0])

        self.multi_supply = [[0, 0] for x in range(self.settings["size_y"])]
        self.multi_demand = [[0, 0] for x in range(self.settings["size_x"])]

        self.supply_labels =  [f"Поставщик {x}" for x in range(1, self.settings["size_y"] + 1)] + ["Потребители"]
        self.demand_labels = [f"Потребитель {x}" for x in range(1, self.settings["size_x"] + 1)] + ["Поставщики"]

        self.brushes = {}
        for color in constants.colors.items():
            self.brushes[color[0]] = QBrush(QColor(*color[1]))
        
        # self.main_layout = QVBoxLayout()
        # self.central_widget.setLayout(self.main_layout)
        
        self.icon = QIcon()
        self.icon.addFile('images/calculator.svg')
        self.setWindowIcon(self.icon)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.stacked_widget = QStackedWidget()

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.main_page = QWidget()
        self.create_main_page()

        self.input_page = QWidget()
        self.create_input_page()

        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.input_page)

        self.main_layout.addWidget(self.stacked_widget)

        # self.central_widget = QWidget() 
        # self.setCentralWidget(self.central_widget)

        # self.status_label = QLabel()
        # self.status_label.setAlignment(Qt.AlignCenter)
        # self.status_label.setStyleSheet("padding: 3px; background: #f0f0f0; border-top: 1px solid #ccc;")
        
        # self.control_group = QGroupBox("Настройка задачи")
        # self.create_controls()
        
        # self.stacked_widget = QStackedWidget()
        
        # self.input_page = QWidget()
        # self.create_combined_input_table()
        
        # self.solution_page = QWidget()
        # self.create_solution_page()

        # self.multiproduct_page = QWidget()
        # self.create_multiproduct_page()

        # self.examples_page = QWidget()
        # self.create_examples_page() 
        
        # self.stacked_widget.addWidget(self.input_page)
        # self.stacked_widget.addWidget(self.solution_page)
        # self.stacked_widget.addWidget(self.multiproduct_page)
        # self.stacked_widget.addWidget(self.examples_page)
        
        # self.main_layout.addWidget(self.stacked_widget)
        # self.main_layout.addWidget(self.status_label)

        # self.update_table_size()
        # self.write_data_into_input_table()
    
    def create_multiproduct_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        group = QGroupBox("Мультипродуктовая задача")
        group_layout = QVBoxLayout()
        
        self.multiproduct_table = QTableWidget()
        self.multiproduct_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        
        btn_layout = QHBoxLayout()
        copy_btn = self.q_push_button("Копировать", "background-color: #2196F3; color: white;", 
                                    lambda: self.copy_table_data(self.multiproduct_table))
        paste_btn = self.q_push_button("Вставить", "background-color: #FF9800; color: white;", 
                                    lambda: self.paste_data_to_table(self.multiproduct_table))
        
        btn_layout.addStretch()
        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(paste_btn)
        
        group_layout.addWidget(self.multiproduct_table)
        group_layout.addLayout(btn_layout)
        group.setLayout(group_layout)
        
        layout.addWidget(group)
        self.multiproduct_page.setLayout(layout)        
        
        # Инициализация пустой таблицы
        #self.init_empty_multiproduct_table()
        self.write_data_into_double_table()

    def get_data_from_double_table(self):
        rows = self.multiproduct_table.rowCount()
        cols = self.multiproduct_table.columnCount()
        
        # if rows < 3 or cols < 3:  # Минимум 1 поставщик, 1 потребитель + заголовки
        #     raise ValueError("Таблица должна содержать хотя бы одного поставщика и потребителя")

        # new_demand_labels = []
        # for col in range(1, destinations + 2):
        #     item = self.combined_table.item(0, col)
        #     new_demand_labels.append(item.text())
        
        # new_supply_labels = []
        # for row in range(1, sources + 2):
        #     item = self.combined_table.item(row, 0)
        #     new_supply_labels.append(item.text())
            
        new_supply = []
        for row in range(self.settings["size_y"]):
            item = [
                self.multiproduct_table.item(2 + row * 2, cols - 1),
                self.multiproduct_table.item(3 + row * 2, cols - 1)
            ]
            new_supply.append([
                int(item[0].text()) if item[0].text().isdigit() else 0,
                int(item[1].text()) if item[1].text().isdigit() else 0,
            ])

        
        new_demand = []
        for col in range(self.settings["size_x"]):
            item = [
                self.multiproduct_table.item(rows - 1, 2 + col * 2),
                self.multiproduct_table.item(rows - 1, 3 + col * 2),
            ]
            new_demand.append([
                int(item[0].text()) if item[0].text().isdigit() else 0,
                int(item[1].text()) if item[1].text().isdigit() else 0,
            ])
        
        new_costs = []
        for row in range(self.settings["size_y"]):
            cost_row = []
            for col in range(self.settings["size_x"]):
                item = [
                    self.multiproduct_table.item(2 + row * 2, 2 + col * 2),
                    self.multiproduct_table.item(3 + row * 2, 3 + col * 2),
                ]
                cost_row.append([
                    int(item[0].text()) if item[0].text().isdigit() else 0,
                    int(item[1].text()) if item[1].text().isdigit() else 0,
                ])
            new_costs.append(cost_row)


        self.multi_supply = functions.combine_arrays_1d_pure(new_supply, self.multi_supply)
        self.multi_demand = functions.combine_arrays_1d_pure(new_demand, self.multi_demand)
        self.multi_costs = functions.combine_arrays_pure(new_costs, self.multi_costs)
        # self.supply_labels = functions.combine_arrays_1d_pure(new_supply_labels[0:-1], self.supply_labels)
        # self.demand_labels = functions.combine_arrays_1d_pure(new_demand_labels[0:-1], self.demand_labels)

    def write_data_into_double_table(self):
        size_y = 3 + 2 * self.settings["size_y"]
        size_x = 3 + 2 * self.settings["size_x"]
        product_number = len(self.product_names)
        self.multiproduct_table.setRowCount(size_y)
        self.multiproduct_table.setColumnCount(size_x)

        for i in range(product_number, size_x - 1, product_number):
            self.multiproduct_table.setSpan(0, i, 1, product_number)

        for i in range(product_number, size_y - 1, product_number):
            self.multiproduct_table.setSpan(i, 0, product_number, 1)
        
        to_write = [["" for i in range(size_x)]]

        to_write.append(["", ""])
        for i in range(self.settings["size_x"]):
            to_write[1] += self.product_names
        to_write[1] += [""]

        for i in range(self.settings["size_y"]):
            to_write.append(["0" for x in range(size_x)])
            to_write.append(["0" for x in range(size_x)])
            for j in range(len(self.multi_costs[0])):
                to_write[2 * i + 2][2 + 2 * j] = self.multi_costs[i][j][0]
                to_write[2 * i + 3][3 + 2 * j] = self.multi_costs[i][j][1]

            to_write[2 * i + 2][1] = self.product_names[0]
            to_write[2 * i + 3][1] = self.product_names[1]

            to_write[2 * i + 2][-1] = self.multi_supply[i][0]
            to_write[2 * i + 3][-1] = self.multi_supply[i][1]

        to_write.append(["0" for x in range(size_x)])
        
        for i in range(self.settings["size_x"]):
            to_write[-1][2 * i + 2] = self.multi_demand[i][0]
            to_write[-1][2 * i + 3] = self.multi_demand[i][1]
        
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
                    item.setBackground(self.brushes["black"])
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.multiproduct_table.setItem(y, x, item)
    
        for i in range(self.multiproduct_table.columnCount()):
            self.multiproduct_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        
        for i in range(self.multiproduct_table.rowCount()):
            self.multiproduct_table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

    def show_multiproduct_table(self):
        self.control_group.setVisible(True)
        self.stacked_widget.setCurrentWidget(self.multiproduct_page)
        self.solve_btn.setVisible(True)
        self.examples_btn.setVisible(True)
        self.back_btn.setVisible(False)
        self.settings["current"] = "multi"
    
    def q_push_button(self, name, style, function=None, cursor=True):
        btn = QPushButton(name)
        btn.setStyleSheet(style)
        if function:
            btn.clicked.connect(function)
        if cursor:
            btn.setCursor(Qt.PointingHandCursor)
        return btn
    
    def create_controls(self):
        self.control_group = QWidget()
        
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(5, 5, 5, 5)
        control_layout.setSpacing(10)
        
        # self.source_layout = QVBoxLayout()
        # self.source_layout.setSpacing(0)
        # self.source_layout.addWidget(QLabel("Поставщики:"))
        # self.source_spin = QSpinBox()
        # self.source_spin.setRange(1, 10)
        # self.source_spin.setValue(self.settings["size_y"])
        # self.source_spin.valueChanged.connect(self.update_input_table)
        # self.source_layout.addWidget(self.source_spin)
        
        # self.dest_layout = QVBoxLayout()
        # self.dest_layout.setSpacing(0)
        # self.dest_layout.addWidget(QLabel("Потребители:"))
        # self.dest_spin = QSpinBox()
        # self.dest_spin.setRange(1, 10)
        # self.dest_spin.setValue(self.settings["size_x"])
        # self.dest_spin.valueChanged.connect(self.update_input_table)
        # self.dest_layout.addWidget(self.dest_spin)
        
        # #self.text_input_btn = self.q_push_button("Ввести текстом", constants.text_input_btn, self.show_text_input_page)
        # self.solve_btn = self.q_push_button("Решить", constants.solve_btn, self.solve)
        # #self.multiproduct_btn = self.q_push_button("Мультипродуктовая задача", constants.multiproduct_btn_ss, self.show_multiproduct_table)
        # self.examples_btn = self.q_push_button("Примеры", constants.examples_btn_ss, self.show_main_page)
        
        # self.back_btn = self.q_push_button("Назад", constants.back_btn_ss, self.show_input_page)
        # self.back_btn.setVisible(False)
        
        # control_layout.addLayout(self.source_layout)
        # control_layout.addLayout(self.dest_layout)
        # control_layout.addStretch()
        # #control_layout.addWidget(self.text_input_btn)
        # control_layout.addWidget(self.back_btn)
        # control_layout.addWidget(self.examples_btn)
        # control_layout.addWidget(self.solve_btn)
        # #control_layout.addWidget(self.multiproduct_btn)
        
        self.control_group.setLayout(control_layout)
        self.main_layout.addWidget(self.control_group)

    def create_main_page(self):
        main_layout = QHBoxLayout()

        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.setAlignment(Qt.AlignTop)
        back_btn = self.q_push_button("Назад", constants.back_btn_ss, self.show_input_page)
        top_layout.addWidget(back_btn)
        
        bottom_layout = QHBoxLayout()
        
        # Первый ряд - выбор типа задачи
        task_type_group = QGroupBox("Тип задачи")
        task_type_layout = QVBoxLayout()
        task_type_layout.setAlignment(Qt.AlignTop)
        task_type_layout.setSpacing(10)
        
        transport_btn = self.q_push_button("Транспортная задача", "background-color: #4CAF50; color: white; padding: 8px;", 
                                         self.show_input_page)
        # assignment_btn = self.q_push_button("Задача назначения", "background-color: #2196F3; color: white; padding: 8px;", 
        #                                   lambda: self.set_task_type("assignment"))
        multiproduct_btn = self.q_push_button("Мультипродуктовая задача", "background-color: #FF9800; color: white; padding: 8px;", 
                                            self.show_multiproduct_table)
        
        task_type_layout.addWidget(transport_btn)
        # task_type_layout.addWidget(assignment_btn)
        task_type_layout.addWidget(multiproduct_btn)
        task_type_group.setLayout(task_type_layout)
        
        examples_group = QGroupBox("Примеры для заполнения")
        examples_layout = QVBoxLayout()
        examples_layout.setAlignment(Qt.AlignTop)
        examples_layout.setSpacing(10)

        for id, example in constants.examples.items():
            example_btn = self.q_push_button(example["name"], "background-color: #607D8B; color: white; padding: 8px;", 
                                        lambda: self.load_example(id))
            examples_layout.addWidget(example_btn)
        
        
        # example2_btn = self.q_push_button("Пример ТЗ 2", "background-color: #607D8B; color: white; padding: 8px;", 
        #                                 lambda: self.load_example(2))
        # example3_btn = self.q_push_button("Пример ТЗ 3", "background-color: #607D8B; color: white; padding: 8px;", 
        #                                 lambda: self.load_example(3))
        # example4_btn = self.q_push_button("Пример МТЗ", "background-color: #9C27B0; color: white; padding: 8px;", 
        #                                 lambda: self.load_example(4))
        
        
        # examples_layout.addWidget(example2_btn)
        # examples_layout.addWidget(example3_btn)
        # examples_layout.addWidget(example4_btn)
        examples_group.setLayout(examples_layout)
        
        empty_row = QWidget()
        empty_row.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        bottom_layout.addWidget(task_type_group)
        bottom_layout.addWidget(examples_group)
        bottom_layout.addWidget(empty_row)        
        
        main_layout.addLayout(bottom_layout)
        main_layout.addLayout(top_layout)
        
        self.main_page.setLayout(main_layout)

    def show_main_page(self):
        #self.control_group.setVisible(False)
        self.stacked_widget.setCurrentWidget(self.main_page)
        self.solve_btn.setVisible(False)
        self.back_btn.setVisible(False)
        self.examples_btn.setVisible(False)
    
    def load_example(self, id):
        problem = constants.examples[id]

        match problem["type"]:
            case "Транспортная задача":
                self.costs = problem["data"]["costs"]
                self.supply = problem["data"]["supply"]
                self.demand = problem["data"]["demand"]
                self.settings["size_y"] = problem["data"]["size_y"]
                self.settings["size_x"] = problem["data"]["size_x"]
                self.write_data_into_input_table()
                self.show_input_page()
            case "Многопродуктовая транспортная задача":
                self.multi_costs = problem["data"]["costs"]
                self.multi_supply = problem["data"]["supply"]
                self.multi_demand = problem["data"]["demand"]
                self.settings["size_y"] = problem["data"]["size_y"]
                self.settings["size_x"] = problem["data"]["size_x"]
                self.write_data_into_double_table()
                self.show_multiproduct_table()
            case _:
                pass
            
        self.source_spin.setValue(problem["data"]["size_y"])
        self.dest_spin.setValue(problem["data"]["size_x"])

    def create_input_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        group_top = QGroupBox("Настройка задачи")
        match self.problem_type:
            case _:
                group_top_layout = self.transportation_problem.get_top_layout()
        group_top.setLayout(group_top_layout)
        
        group = QGroupBox("Ввод данных задачи")
        group_layout = QVBoxLayout()
        
        self.input_table = QTableWidget()
        self.input_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        
        group_layout.addWidget(self.input_table)
        group.setLayout(group_layout)
        
        layout.addWidget(group_top)
        layout.addWidget(group)
        self.input_page.setLayout(layout)

    def highlight_table_regions(self):
        for row in range(self.combined_table.rowCount()):
            for col in range(self.combined_table.columnCount()):
                item = self.combined_table.item(row, col)
                if item:
                    item.setBackground(self.brushes["white"])
        
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        
        for row in range(1, sources + 1):
            item = self.combined_table.item(row, destinations + 1)
            if item:
                item.setBackground(self.brushes["blue"])
        
        for col in range(1, destinations + 1):
            item = self.combined_table.item(sources + 1, col)
            if item:
                item.setBackground(self.brushes["pink"])
        
        for row in range(1, sources + 1):
            for col in range(1, destinations + 1):
                item = self.combined_table.item(row, col)
                if item:
                    item.setBackground(self.brushes["green"])
    
    def show_input_page(self):        
#        self.control_group.setVisible(True)
        #self.stacked_widget.setCurrentIndex(0)
        self.stacked_widget.setCurrentWidget(self.input_page)
        self.page = "input"
        # self.solve_btn.setVisible(True)
        # self.back_btn.setVisible(False)
        # self.settings["current"] = "standard"
        # self.examples_btn.setVisible(True)
    
    def show_solution_page(self):
        self.control_group.setVisible(True)
        self.stacked_widget.setCurrentIndex(1)
        self.solve_btn.setVisible(False)
        self.back_btn.setVisible(True)
        self.examples_btn.setVisible(False)
    
    def create_solution_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        solution_group = QGroupBox("Оптимальное распределение")
        solution_layout = QVBoxLayout()
        solution_layout.setContentsMargins(5, 5, 5, 5)
        
        self.solution_table = QTableWidget()
        self.solution_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.solution_table.setStyleSheet(constants.solution_table_ss)
        
        s_header = self.solution_table.horizontalHeader()
        s_header.setSectionResizeMode(QHeaderView.Stretch)
        s_header.setDefaultAlignment(Qt.AlignCenter)
        s_header.setStyleSheet(constants.solution_page_h_header_ss)
        
        s_v_header = self.solution_table.verticalHeader()
        s_v_header.setSectionResizeMode(QHeaderView.Stretch)
        s_v_header.setDefaultAlignment(Qt.AlignCenter)
        s_v_header.setStyleSheet(constants.solution_page_v_header_ss)

        self.total_cost_label = QLabel("Общая стоимость: -")
        self.total_cost_label.setAlignment(Qt.AlignCenter)
        self.total_cost_label.setStyleSheet(constants.total_cost_label_ss)
        
        btn_layout = QHBoxLayout()
        
        solution_copy_btn = self.q_push_button(
            "Копировать решение", 
            constants.solution_copy_btn_ss, 
            lambda: self.copy_table_data(self.solution_table)
        )
        
        self.export_csv_btn = self.q_push_button(
            "Выгрузить CSV", 
            constants.export_csv_btn_ss, 
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
        if not self.solution_table.rowCount() or not self.solution_table.columnCount():
            return
        
        for row in range(self.solution_table.rowCount()):
            for col in range(self.solution_table.columnCount()):
                item = self.solution_table.item(row, col)
                if item:
                    item.setBackground(self.brushes["white"])
        
        for row in range(self.solution_table.rowCount()):
            for col in range(self.solution_table.columnCount()):
                item = self.solution_table.item(row, col)
                if item:
                    item.setBackground(self.brushes["lime"])
                    if item.text() != "0" and item.text() != "":
                        item.setBackground(self.brushes["green"])
    
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
    
    def write_data_into_input_table(self):
        sources = self.settings["size_y"]
        destinations = self.settings["size_x"]
        self.combined_table.setRowCount(sources + 2)
        self.combined_table.setColumnCount(destinations + 2)

        to_write = [[""] + self.demand_labels[0:destinations] + [self.demand_labels[-1]]]
        for i in range(0, sources):
            this = [self.supply_labels[i]] + self.costs[i][0:destinations] + [self.supply[i]]
            to_write.append(this)
        to_write.append([self.demand_labels[-1]] + self.demand + [""])

        for y in range(sources + 2):
            for x in range(destinations + 2):
                item = QTableWidgetItem(str(to_write[y][x]))
                item.setTextAlignment(Qt.AlignCenter)
                self.combined_table.setItem(y, x, item)
        
        self.highlight_table_regions()

    def get_data_from_input_table(self):
        rows = self.combined_table.rowCount()
        cols = self.combined_table.columnCount()
        
        if rows < 3 or cols < 3:  # Минимум 1 поставщик, 1 потребитель + заголовки
            raise ValueError("Таблица должна содержать хотя бы одного поставщика и потребителя")
        
        sources = rows - 2
        destinations = cols - 2

        new_demand_labels = []
        for col in range(1, destinations + 2):
            item = self.combined_table.item(0, col)
            new_demand_labels.append(item.text())
        
        new_supply_labels = []
        for row in range(1, sources + 2):
            item = self.combined_table.item(row, 0)
            new_supply_labels.append(item.text())
            
        new_supply = []
        for row in range(1, sources + 1):
            item = self.combined_table.item(row, destinations + 1)
            new_supply.append(int(item.text()) if item and item.text().isdigit() else 0)
        
        new_demand = []
        for col in range(1, destinations + 1):
            item = self.combined_table.item(sources + 1, col)
            new_demand.append(int(item.text()) if item and item.text().isdigit() else 0)
        
        new_costs = []
        for row in range(1, sources + 1):
            cost_row = []
            for col in range(1, destinations + 1):
                item = self.combined_table.item(row, col)
                cost_row.append(int(item.text()) if item and item.text().isdigit() else 0)
            new_costs.append(cost_row)

        self.supply = functions.combine_arrays_1d_pure(new_supply, self.supply)
        self.demand = functions.combine_arrays_1d_pure(new_demand, self.demand)
        self.costs = functions.combine_arrays_pure(new_costs, self.costs)
        self.supply_labels = functions.combine_arrays_1d_pure(new_supply_labels[0:-1], self.supply_labels)
        self.demand_labels = functions.combine_arrays_1d_pure(new_demand_labels[0:-1], self.demand_labels)

    def update_table_size(self):
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()

        self.settings["size_x"] = destinations
        self.settings["size_y"] = sources
        
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
    
    def update_input_table(self):
        self.get_data_from_input_table()
        self.update_table_size()
        self.write_data_into_input_table()

    def solve(self):
        if self.settings["current"] == "multi":
            self.solve_multi()
        else:
            self.solve_problem()
    
    def solve_multi(self):
        self.get_data_from_double_table()
        
        problem = Solver(self.multi_supply, self.multi_demand, self.multi_costs)
        result_matrix, self.total_cost , info = problem.solve_transportation_scipy_double()

        #print(info)

        size_y = 2 + 2 * len(result_matrix)
        size_x = 2 + 2 * len(result_matrix[0])

        self.solution_table.setRowCount(size_y - 1)
        self.solution_table.setColumnCount(size_x - 1)

        for i in range(2, size_x - 2, 2):
            self.solution_table.setSpan(0, i, 1, 2)

        for i in range(2, size_y - 2, 2):
            self.solution_table.setSpan(i, 0, 2, 1)
        
        to_write = [["" for i in range(size_x)]]

        to_write.append(["", "'"])
        for i in range(self.settings["size_x"]):
            to_write[1] += self.product_names
        to_write[1] += [""]

        for i in range(self.settings["size_y"]):
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
                    item.setBackground(self.brushes["black"])
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    
                item.setTextAlignment(Qt.AlignCenter)
                self.solution_table.setItem(y, x, item)

        self.total_cost_label.setText(f"Общая стоимость: {constants.stringify(self.total_cost)}")

        self.show_solution_page()
    
    def solve_problem(self):
        # try:
            
        # except Exception as e:
        #     QMessageBox.critical(self, "Ошибка", f"Не удалось решить задачу:\n{str(e)}")
        #     self.show_status_message(f"Ошибка: {str(e)}")
        self.get_data_from_input_table()
        costs, supply, demand = self.costs, self.supply, self.demand
        
        problem = Solver(supply, demand, costs)
        result_matrix, self.total_cost = problem.solve_transportation_scipy()

        sources = len(result_matrix)
        destinations = len(result_matrix[0]) if sources > 0 else 0

        to_write = [[""] + self.demand_labels[0:self.settings["size_x"]]]

        if destinations > self.settings["size_x"]:
            to_write[0].append("Фиктивный потребитель")

        for i in range(0, self.settings["size_y"]):
            this = [self.supply_labels[i]] + result_matrix[i].tolist()
            to_write.append(this)
    
        if sources > self.settings["size_y"]:
            to_write.append(["Фиктивный поставщик"] + result_matrix[-1].tolist())
        
        self.solution_table.setRowCount(len(to_write))
        self.solution_table.setColumnCount(len(to_write[0]))

        for y in range(len(to_write)):
            for x in range(len(to_write[0])):
                val = to_write[y][x]
                if isinstance(val, float):
                    val = "{0:g}".format(val)
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                self.solution_table.setItem(y, x, item)
        
        self.total_cost_label.setText(f"Общая стоимость: {constants.stringify(self.total_cost)}")
        self.highlight_solution_table()
        
        self.show_solution_page()
        self.show_status_message("Задача решена!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransportationSolver()
    window.show()
    sys.exit(app.exec())
