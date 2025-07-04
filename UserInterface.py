import constants
import functions
from ProblemDatabase import ProblemDatabase
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QGroupBox, QSizePolicy, QStackedWidget, QLabel, QFrame, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont
from LinearProblem import LinearProblem
from TransportationProblem import TransportationProblem
from MultiobjectiveTransportationProblem import MultiobjectiveTransportationProblem
from AssignmentProblem import AssignmentProblem
from random import randint


class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Инструментарий для решения задач линейного программирования")
        self.page = "main"
        self.problem_type = ""
        self.setGeometry(100, 100, 656, 480)
        self.size_modifier = 0

        self.pdb = ProblemDatabase()
        
        self.font_small = QFont()
        self.font_small.setPointSize(7)
        
        self.font_medium = QFont()
        self.font_medium.setPointSize(10)

        self.mode = "big"

        self.icon = QIcon()
        self.icon.addFile(functions.resource_path('images/calculator.svg'))
        self.setWindowIcon(self.icon)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.stacked_widget = QStackedWidget()

        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        self.main_page = QWidget()
        self.create_main_page()

        self.input_page = QWidget()
        self.create_input_page()

        self.solution_page = QWidget()
        self.create_solution_page()

        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.input_page)
        self.stacked_widget.addWidget(self.solution_page)

        self.central_layout.addWidget(self.stacked_widget)

        self.resize()

    def resize(self):
        width = self.width()
        print(width)

        if width < 950 and self.mode == "big":
            self.mode = "small"
            for btn in self.category_buttons:
                btn.setFixedSize(145, 60)
                btn.setFont(self.font_small)
                
            for btn in self.var_btns:
                btn.setFixedSize(90, 50)
                btn.setFont(self.font_small)
            self.buttons_scroll.setFixedWidth(120)
            self.text_display.setStyleSheet("QLabel {font-size: 15px;}")
            self.type_buttons_layout.setSpacing(10)
        if width >= 950 and self.mode == "small":
            self.mode = "big"
            for btn in self.category_buttons:
                btn.setFixedSize(205, 70)   
                btn.setFont(self.font_medium)
            
            for btn in self.var_btns:
                btn.setFixedSize(160, 50)
                btn.setFont(self.font_medium)
            self.buttons_scroll.setFixedWidth(200)
            self.text_display.setStyleSheet("QLabel {font-size: 20px;}")
            self.type_buttons_layout.setSpacing(20)

    def resizeEvent(self, event):
        self.resize()

    def create_main_page(self):
        self.main_layout = QVBoxLayout()

        self.create_level1()
        self.create_level2()

        self.level2_widget.hide()
        
        self.main_page.setLayout(self.main_layout)
    
    def copy_solution_to_clipboard(self):
        current_table = self.solution_table.currentWidget()
        
        if not current_table:
            return
        
        rows = current_table.rowCount()
        cols = current_table.columnCount()
        
        data = []
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = current_table.item(row, col)
                if item:
                    row_data.append(item.text())
                else:
                    if current_table.item(row, col) is None:
                        found = False
                        for r in range(row, -1, -1):
                            for c in range(col, -1, -1):
                                if current_table.item(r, c) and \
                                (r + current_table.rowSpan(r, c) > row) and \
                                (c + current_table.columnSpan(r, c) > col):
                                    item = current_table.item(r, c)
                                    row_data.append(item.text())
                                    found = True
                                    break
                            if found:
                                break
                        if not found:
                            row_data.append("")
                    else:
                        row_data.append("")
            data.append(row_data)
        
        text = "\n".join(["\t".join(row) for row in data if any(cell.strip() for cell in row)])
        
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def create_level1(self):
        self.level1_widget = QWidget()
        level1_layout = QVBoxLayout(self.level1_widget)
        level1_layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel("Выберите тип задачи:")
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        level1_layout.addWidget(label, alignment=Qt.AlignLeft)
        
        self.type_buttons_layout = QHBoxLayout()
        self.type_buttons_layout.setSpacing(20)
        
        categories = ["Каноническая задача\nлинейного программирования", "Транспортная задача", "Задача о назначениях", "Многопродуктовая\nтранспортная задача"]
        
        self.category_buttons = []
        
        for category in categories:
            btn = functions.q_push_button(category, constants.solve_btn)
            btn.setFixedSize(200, 70)
            btn.clicked.connect(lambda _, cat=category: self.show_level2(cat))
            self.type_buttons_layout.addWidget(btn)
            self.category_buttons.append(btn)
        
        level1_layout.addLayout(self.type_buttons_layout)
        self.main_layout.addWidget(self.level1_widget, stretch=0, alignment=Qt.AlignTop)
    
    def create_level2(self):
        self.level2_widget = QWidget()
        self.level2_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        level2_layout = QVBoxLayout(self.level2_widget)
        level2_layout.setContentsMargins(0, 10, 0, 0)
        
        self.level2_label = QLabel()
        self.level2_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.level2_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        level2_layout.addWidget(self.level2_label, alignment=Qt.AlignLeft)

        self.level2_container = QWidget()
        level2_container_layout = QHBoxLayout(self.level2_container)
        level2_container_layout.setContentsMargins(10, 0, 0, 0)
        level2_layout.addWidget(self.level2_container)
        
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        level2_container_layout.addWidget(buttons_widget, stretch=0)

        self.pick_buttons = []

        btn_new_problem = functions.q_push_button("Новая задача", constants.solve_btn, self.show_input_page)
        self.pick_buttons.append(btn_new_problem)

        btn_pick_problem = functions.q_push_button("Выбрать задачу", constants.solve_btn)
        btn_pick_problem.clicked.connect(lambda _, opt="ВЗ": self.show_level3(opt))
        self.pick_buttons.append(btn_pick_problem)

        btn_rand_problem = functions.q_push_button("Случайная задача", constants.solve_btn)
        btn_rand_problem.clicked.connect(lambda _, opt="СЗ": self.random_problem(opt))
        self.pick_buttons.append(btn_rand_problem)

        for btn in self.pick_buttons:
            btn.setFixedSize(135, 55)
            buttons_layout.addWidget(btn)

        buttons_layout.addStretch()

        self.create_level3()

        level2_container_layout.addWidget(self.level3_widget, stretch=0)

        self.main_layout.addWidget(self.level2_widget, stretch=0)

    def random_problem(self, opt):
        self.problem_id = randint(1, 25)
        self.show_level3(opt)
        prob = self.problems[self.problem_type][self.problem_id]
        self.show_text([prob['id'], prob['problem_text']])

    def create_level3(self):
        self.level3_widget = QWidget()
        problem_layout = QHBoxLayout(self.level3_widget)
        problem_layout.setContentsMargins(20, 17, 0, 0)
        
        self.problems = {"Каноническая задача линейного программирования": [], "Транспортная задача": [], "Задача о назначениях": [], "Многопродуктовая транспортная задача": []}
        for pt in self.problems:
            self.problems[pt] = self.pdb.get_all_problems(pt)

        self.buttons_stacked_widget = QStackedWidget()
        self.btn_widgets = {}
        self.var_btns = []
        for pt in self.problems:
            self.btn_widgets[pt] = QWidget()
            btn_layout = QVBoxLayout(self.btn_widgets[pt])
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.setSpacing(0)

            for problem in self.problems[pt].values():
                btn_text = functions.split_by_newline_without_word_break(problem['name'], 30)
                button = functions.q_push_button(btn_text, constants.variant_btn)
                button.clicked.connect(lambda checked, text=(problem['id'], problem['problem_text']): self.show_text(text))
                button.setFixedSize(140, 50)
                self.var_btns.append(button)
                btn_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignHCenter)
                btn_layout.addStretch()

            self.buttons_stacked_widget.addWidget(self.btn_widgets[pt])    
        
        self.buttons_scroll = QScrollArea()
        self.buttons_scroll.setWidget(self.buttons_stacked_widget)
        self.buttons_scroll.setWidgetResizable(True)
        self.buttons_scroll.setFrameShape(QFrame.NoFrame)
        self.buttons_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.buttons_scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        text_container = QWidget()
        text_container_layout = QVBoxLayout(text_container)
        text_container_layout.setContentsMargins(0, 0, 0, 0)
        text_container_layout.setSpacing(10)
        
        self.text_display = QLabel("Выберите задачу")
        self.text_display.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.text_display.setWordWrap(True)
        self.text_display.setStyleSheet("QLabel {font-size: 20px;}")
        
        self.confirm_btn = functions.q_push_button("Подтвердить", constants.solve_btn)
        self.confirm_btn.setFixedSize(150, 60)
        self.confirm_btn.clicked.connect(self.load_example)
        self.confirm_btn.hide()
        
        text_container_layout.addWidget(self.text_display)
        text_container_layout.addWidget(self.confirm_btn, alignment=Qt.AlignRight)
        
        text_scroll = QScrollArea()
        text_scroll.setWidget(text_container)
        text_scroll.setWidgetResizable(True)
        text_scroll.setFrameShape(QFrame.NoFrame)
        
        splitter = QFrame()
        splitter.setFrameShape(QFrame.VLine)
        splitter.setFrameShadow(QFrame.Sunken)
        splitter.setStyleSheet("background-color: #ccc;")
        
        problem_layout.addWidget(self.buttons_scroll)
        self.buttons_scroll.setFixedWidth(200)
        problem_layout.addWidget(splitter)
        problem_layout.addWidget(text_scroll, 1)

        self.level3_widget.hide()
    
    def show_text(self, text):
        self.problem_id = text[0]
        self.text_display.setText(text[1])
        self.confirm_btn.show()
    
    def show_level2(self, category):
        self.problem_type = category.replace('\n', ' ')
        self.level2_label.setText(f"Действие для задачи: {self.problem_type}")
        self.level2_widget.show()
        self.level3_widget.hide()
        self.confirm_btn.hide()
    
    def show_level3(self, category):
        self.text_display.setText("Выберите задачу")
        self.buttons_stacked_widget.setCurrentWidget(self.btn_widgets[self.problem_type])
        self.level3_widget.show()

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
    
    def load_example(self):
        match self.problem_type:
            case "Транспортная задача":
                problem = self.problems["Транспортная задача"][self.problem_id]
                self.transportation_problem.source_spin.setValue(len(problem["costs"]))
                self.transportation_problem.dest_spin.setValue(len(problem["costs"][0]))
                self.transportation_problem.costs = problem["costs"]
                self.transportation_problem.supply = problem["supply"]
                self.transportation_problem.demand = problem["demand"]                
                self.transportation_problem.variable_names_x = problem["names_x"]
                self.transportation_problem.variable_names_y = problem["names_y"]
                self.transportation_problem.update_table_size()
                self.transportation_problem.write_data_into_input_table()
            case "Задача о назначениях":
                problem = self.problems["Задача о назначениях"][self.problem_id]
                self.assignment_problem.source_spin.setValue(len(problem["costs"]))
                self.assignment_problem.dest_spin.setValue(len(problem["costs"][0]))
                self.assignment_problem.costs = problem["costs"]
                self.assignment_problem.variable_names_x = problem["names_x"]
                self.assignment_problem.variable_names_y = problem["names_y"]
                self.assignment_problem.update_table_size()
                self.assignment_problem.write_data_into_input_table()
            case "Многопродуктовая транспортная задача":
                problem = self.problems["Многопродуктовая транспортная задача"][self.problem_id]
                self.multiobject_transportation_problem.source_spin.setValue(len(problem["supply"]))
                self.multiobject_transportation_problem.dest_spin.setValue(len(problem["demand"]))
                self.multiobject_transportation_problem.costs = problem["costs"]
                self.multiobject_transportation_problem.supply = problem["supply"]
                self.multiobject_transportation_problem.demand = problem["demand"]               
                self.assignment_problem.update_table_size()
                self.multiobject_transportation_problem.write_data_into_input_table()
            case "Каноническая задача линейного программирования":
                problem = self.problems["Каноническая задача линейного программирования"][self.problem_id]
                self.linear_problem.source_spin.setValue(len(problem["constraints"]))
                self.linear_problem.dest_spin.setValue(len(problem["function"]))
                self.linear_problem.problem_type = problem["problem_type"]
                self.linear_problem.costs = problem["costs"]
                self.linear_problem.function = problem["function"]
                self.linear_problem.constraints = problem["constraints"]                
                self.linear_problem.signs = problem["signs"]
                self.linear_problem.variable_names = problem["names_x"]
                self.linear_problem.variable_names_y = problem["names_y"]
                self.linear_problem.update_table_size()
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
        self.solution_table.addWidget(self.linear_problem.solution_table)

        self.btn_gbox = QGroupBox()
        
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(5, 5, 5, 5)
        btn_layout.setSpacing(10)

        copy_btn = functions.q_push_button(
            "Копировать",
            constants.solve_btn, 
            self.copy_solution_to_clipboard
        )

        back_btn = functions.q_push_button(
            "Назад",
            constants.solve_btn, 
            self.show_input_page
        )
        
        btn_layout.addStretch()
        btn_layout.addWidget(copy_btn)
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
