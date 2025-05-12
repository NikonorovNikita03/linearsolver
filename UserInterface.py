import constants
import functions
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QSizePolicy, QStackedWidget, QMenu, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from LinearProblem import LinearProblem
from TransportationProblem import TransportationProblem
from MultiobjectiveTransportationProblem import MultiobjectiveTransportationProblem
from AssignmentProblem import AssignmentProblem
from functools import partial


class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение транспортных задач линейного программирования")
        self.page = "main"
        self.problem_type = ""
        self.setGeometry(100, 100, 1366, 768)
        
        self.icon = QIcon()
        self.icon.addFile(functions.resource_path('images/calculator.svg'))
        self.setWindowIcon(self.icon)

        self.create_menu_bar()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.stacked_widget = QStackedWidget()

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.main_page = QWidget()
        self.create_main_page()

        self.input_page = QWidget()
        self.create_input_page()

        self.solution_page = QWidget()
        self.create_solution_page()

        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.input_page)
        self.stacked_widget.addWidget(self.solution_page)

        self.main_layout.addWidget(self.stacked_widget)

    def create_menu_bar(self):
        self.menu_bar = self.menuBar()
        
        self.file_menu = self.menu_bar.addMenu("Файл")

        new_menu = QMenu("Создать", self)
        
        action1 = QAction("Новый файл", self)
        action2 = QAction("Задача линейного программирования", self)
        action3 = QAction("Транспортная задача", self)
        action4 = QAction("Задача о назначениях", self)
        action5 = QAction("Многопродуктовая транспортная задача", self)

        new_menu.addAction(action1)
        new_menu.addSeparator()
        new_menu.addAction(action2)
        new_menu.addAction(action3)
        new_menu.addAction(action4)
        new_menu.addAction(action5)

        open_action = QAction("Открыть", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)

        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        self.file_menu.addMenu(new_menu)
        self.file_menu.addAction(open_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(exit_action)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "JSON Files (*.json)")
        if file_name:
            print(file_name)

    def create_main_page(self):
        main_layout = QHBoxLayout()
        
        bottom_layout = QHBoxLayout()
        
        task_type_group = QGroupBox("Тип задачи")
        task_type_layout = QVBoxLayout()
        task_type_layout.setAlignment(Qt.AlignTop)
        task_type_layout.setSpacing(10)

        linear_btn = functions.q_push_button("Задача линейного программирования", "background-color: #4CAF50; color: white; padding: 8px;", 
                                        self.show_linear_table)
        transport_btn = functions.q_push_button("Транспортная задача", "background-color: #4CAF50; color: white; padding: 8px;", 
                                        self.show_transportation_table)
        assignment_btn = functions.q_push_button("Задача о назначениях", "background-color: #2196F3; color: white; padding: 8px;", 
                                        self.show_assignment_table)
        multiproduct_btn = functions.q_push_button("Мультипродуктовая задача", "background-color: #FF9800; color: white; padding: 8px;", 
                                        self.show_multiobject_transportation_table)
        
        task_type_layout.addWidget(linear_btn)
        task_type_layout.addWidget(transport_btn)
        task_type_layout.addWidget(assignment_btn)
        task_type_layout.addWidget(multiproduct_btn)
        task_type_group.setLayout(task_type_layout)
        
        examples_group = QGroupBox("Примеры для заполнения")
        examples_layout = QVBoxLayout()
        examples_layout.setAlignment(Qt.AlignTop)
        examples_layout.setSpacing(10)

        for id, example in constants.examples.items():
            btn = functions.q_push_button(example["name"], "background-color: #607D8B; color: white; padding: 8px;", 
                                        partial(self.load_example, id))
            examples_layout.addWidget(btn)
        
        examples_group.setLayout(examples_layout)
        
        empty_row = QWidget()
        empty_row.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        bottom_layout.addWidget(task_type_group)
        bottom_layout.addWidget(examples_group)
        bottom_layout.addWidget(empty_row)        
        
        main_layout.addLayout(bottom_layout)
        
        self.main_page.setLayout(main_layout)

    def show_linear_table(self):
        self.problem_type = "ЗЛП"
        self.show_input_page()

    def show_transportation_table(self):
        self.problem_type = "Транспортная задача"
        self.show_input_page()
    
    def show_multiobject_transportation_table(self):
        self.problem_type = "Многопродуктовая транспортная задача"
        self.show_input_page()

    def show_assignment_table(self):
        self.problem_type = "Задача о назначениях"
        self.show_input_page()

    def show_main_page(self):
        self.stacked_widget.setCurrentWidget(self.main_page)
        self.page = "main"
    
    def load_example(self, id):
        problem = constants.examples[id]
        self.problem_type = problem["type"]
        match problem["type"]:
            case "Транспортная задача":
                self.transportation_problem.source_spin.setValue(problem["data"]["size_y"])
                self.transportation_problem.dest_spin.setValue(problem["data"]["size_x"])
                self.transportation_problem.costs = problem["data"]["costs"]
                self.transportation_problem.supply = problem["data"]["supply"]
                self.transportation_problem.demand = problem["data"]["demand"]                
                self.transportation_problem.write_data_into_input_table()
            case "Задача о назначениях":
                self.assignment_problem.source_spin.setValue(problem["data"]["size_y"])
                self.assignment_problem.dest_spin.setValue(problem["data"]["size_x"])
                self.assignment_problem.costs = problem["data"]["costs"]
                self.assignment_problem.write_data_into_input_table()
            case "Многопродуктовая транспортная задача":
                self.multiobject_transportation_problem.source_spin.setValue(problem["data"]["size_y"])
                self.multiobject_transportation_problem.dest_spin.setValue(problem["data"]["size_x"])
                self.multiobject_transportation_problem.costs = problem["data"]["costs"]
                self.multiobject_transportation_problem.supply = problem["data"]["supply"]
                self.multiobject_transportation_problem.demand = problem["data"]["demand"]               
                self.multiobject_transportation_problem.write_data_into_input_table()
            case _:
                self.linear_problem.source_spin.setValue(problem["data"]["size_y"])
                self.linear_problem.dest_spin.setValue(problem["data"]["size_x"])
                self.linear_problem.costs = problem["data"]["costs"]
                self.linear_problem.supply = problem["data"]["supply"]
                self.linear_problem.demand = problem["data"]["demand"]                
                self.linear_problem.write_data_into_input_table()
        self.show_input_page()

    def create_input_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.group_top = QStackedWidget()
        self.input_table = QStackedWidget()

        self.linear_problem = LinearProblem()
        self.group_top.addWidget(self.linear_problem.group_top)
        self.input_table.addWidget(self.linear_problem.table)
        self.linear_problem.menu_btn.clicked.connect(self.show_main_page)
        self.linear_problem.solve_btn.clicked.connect(self.solve)

        self.transportation_problem = TransportationProblem(3, 3)
        self.group_top.addWidget(self.transportation_problem.group_top)
        self.input_table.addWidget(self.transportation_problem.table)
        self.transportation_problem.menu_btn.clicked.connect(self.show_main_page)
        self.transportation_problem.solve_btn.clicked.connect(self.solve)        

        self.multiobject_transportation_problem = MultiobjectiveTransportationProblem(3, 3)
        self.group_top.addWidget(self.multiobject_transportation_problem.group_top)
        self.input_table.addWidget(self.multiobject_transportation_problem.table)
        self.multiobject_transportation_problem.menu_btn.clicked.connect(self.show_main_page)
        self.multiobject_transportation_problem.solve_btn.clicked.connect(self.solve)

        self.assignment_problem =  AssignmentProblem(3, 3)
        self.group_top.addWidget(self.assignment_problem.group_top)
        self.input_table.addWidget(self.assignment_problem.table)
        self.assignment_problem.menu_btn.clicked.connect(self.show_main_page)
        self.assignment_problem.solve_btn.clicked.connect(self.solve)
        
        group = QGroupBox("Ввод данных задачи")
        group_layout = QVBoxLayout()
        
        group_layout.addWidget(self.input_table)
        group.setLayout(group_layout)
        
        layout.addWidget(self.group_top)
        layout.addWidget(group, stretch=1)
        self.input_page.setLayout(layout)
    
    def show_input_page(self):        
        match self.problem_type:
            case "Транспортная задача":
                self.group_top.setCurrentWidget(self.transportation_problem.group_top)
                self.input_table.setCurrentWidget(self.transportation_problem.table)
            case "Задача о назначениях":
                self.group_top.setCurrentWidget(self.assignment_problem.group_top)
                self.input_table.setCurrentWidget(self.assignment_problem.table)
            case "Многопродуктовая транспортная задача":
                self.group_top.setCurrentWidget(self.multiobject_transportation_problem.group_top)
                self.input_table.setCurrentWidget(self.multiobject_transportation_problem.table)
            case _:
                self.group_top.setCurrentWidget(self.linear_problem.group_top)
                self.input_table.setCurrentWidget(self.linear_problem.table)
        self.stacked_widget.setCurrentWidget(self.input_page)
        self.page = "input"
    
    def show_solution_page(self):
        self.stacked_widget.setCurrentWidget(self.solution_page)
        self.page = "solution"
    
    def create_solution_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        solution_group = QGroupBox("Оптимальное распределение")
        solution_layout = QVBoxLayout()        

        self.solution_table = QStackedWidget()
        self.solution_table.addWidget(self.transportation_problem.solution_table)
        self.solution_table.addWidget(self.multiobject_transportation_problem.solution_table)
        self.solution_table.addWidget(self.assignment_problem.solution_table)

        self.btn_gbox = QGroupBox()
        
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(5, 25, 5, 5)
        btn_layout.setSpacing(10)
        
        solution_copy_btn = functions.q_push_button(
            "Копировать решение", 
            constants.solution_copy_btn_ss, 
            # lambda: self.copy_table_data(self.solution_table)
        )
        
        self.export_csv_btn = functions.q_push_button(
            "Выгрузить CSV", 
            constants.export_csv_btn_ss, 
            # self.export_solution_to_csv
        )

        back_btn = functions.q_push_button(
            "Назад",
            constants.export_csv_btn_ss, 
            self.show_input_page
        )
        
        btn_layout.addWidget(solution_copy_btn)
        btn_layout.addWidget(self.export_csv_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(back_btn)

        solution_layout.addWidget(self.solution_table)

        self.btn_gbox.setLayout(btn_layout)
        solution_group.setLayout(solution_layout)
        
        layout.addWidget(self.btn_gbox)
        layout.addWidget(solution_group)
        self.solution_page.setLayout(layout)

    def solve(self):
        match self.problem_type:
            case "Транспортная задача":
                self.transportation_problem.solution_table.clearSpans()
                self.transportation_problem.solve()
                self.solution_table.setCurrentWidget(self.transportation_problem.solution_table) 
            case "Задача о назначениях":
                self.assignment_problem.solution_table.clearSpans()
                self.assignment_problem.solve()
                self.solution_table.setCurrentWidget(self.assignment_problem.solution_table)
                pass
            case "Многопродуктовая транспортная задача":
                self.multiobject_transportation_problem.solution_table.clearSpans()
                self.multiobject_transportation_problem.solve()
                self.solution_table.setCurrentWidget(self.multiobject_transportation_problem.solution_table)
            case _:
                self.linear_problem.solution_table.clearSpans()
                self.linear_problem.solve()
                self.solution_table.setCurrentWidget(self.linear_problem.solution_table)
        self.show_solution_page()
