import sys
import csv
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QGroupBox, QPushButton, QSizePolicy,
    QLabel, QSpinBox, QMessageBox, QFileDialog, QStackedWidget, QHeaderView,
    QGraphicsOpacityEffect
)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QIcon, QColor, QBrush
from solver import Solver
from TransportationProblem import TransportationProblem
from MultiobjectiveTransportationProblem import MultiobjectiveTransportationProblem
from AssignmentProblem import AssignmentProblem
import constants
import functions
from functools import partial


class TransportationSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение транспортных задач линейного программирования")
        self.settings = functions.get_settings()
        self.page = "main"
        self.problem_type = ""
        self.setGeometry(100, 100, self.settings["width"], self.settings["height"])
        
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

        self.solution_page = QWidget()
        self.create_solution_page()

        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.input_page)
        self.stacked_widget.addWidget(self.solution_page)

        self.main_layout.addWidget(self.stacked_widget)

    def create_main_page(self):
        main_layout = QHBoxLayout()
        
        bottom_layout = QHBoxLayout()
        
        task_type_group = QGroupBox("Тип задачи")
        task_type_layout = QVBoxLayout()
        task_type_layout.setAlignment(Qt.AlignTop)
        task_type_layout.setSpacing(10)
        
        transport_btn = functions.q_push_button("Транспортная задача", "background-color: #4CAF50; color: white; padding: 8px;", 
                                        self.show_transportation_table)
        assignment_btn = functions.q_push_button("Задача о назначениях", "background-color: #2196F3; color: white; padding: 8px;", 
                                        self.show_assignment_table)
        multiproduct_btn = functions.q_push_button("Мультипродуктовая задача", "background-color: #FF9800; color: white; padding: 8px;", 
                                        self.show_multiobject_transportation_table)
        
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
                self.transportation_problem.source_spin.setValue(problem["data"]["size_y"])
                self.transportation_problem.dest_spin.setValue(problem["data"]["size_x"])
                self.transportation_problem.costs = problem["data"]["costs"]
                self.transportation_problem.supply = problem["data"]["supply"]
                self.transportation_problem.demand = problem["data"]["demand"]                
                self.transportation_problem.write_data_into_input_table()
        self.show_input_page()

    def create_input_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.group_top = QStackedWidget()
        self.input_table = QStackedWidget()

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

    # def highlight_table_regions(self):
    #     for row in range(self.combined_table.rowCount()):
    #         for col in range(self.combined_table.columnCount()):
    #             item = self.combined_table.item(row, col)
    #             if item:
    #                 item.setBackground(self.brushes["white"])
        
    #     sources = self.source_spin.value()
    #     destinations = self.dest_spin.value()
        
    #     for row in range(1, sources + 1):
    #         item = self.combined_table.item(row, destinations + 1)
    #         if item:
    #             item.setBackground(self.brushes["blue"])
        
    #     for col in range(1, destinations + 1):
    #         item = self.combined_table.item(sources + 1, col)
    #         if item:
    #             item.setBackground(self.brushes["pink"])
        
    #     for row in range(1, sources + 1):
    #         for col in range(1, destinations + 1):
    #             item = self.combined_table.item(row, col)
    #             if item:
    #                 item.setBackground(self.brushes["green"])
    
    def show_input_page(self):        
        match self.problem_type:
            case "Задача о назначениях":
                self.group_top.setCurrentWidget(self.assignment_problem.group_top)
                self.input_table.setCurrentWidget(self.assignment_problem.table)
            case "Многопродуктовая транспортная задача":
                self.group_top.setCurrentWidget(self.multiobject_transportation_problem.group_top)
                self.input_table.setCurrentWidget(self.multiobject_transportation_problem.table)
            case _:
                self.group_top.setCurrentWidget(self.transportation_problem.group_top)
                self.input_table.setCurrentWidget(self.transportation_problem.table)
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
            lambda: self.copy_table_data(self.solution_table)
        )
        
        self.export_csv_btn = functions.q_push_button(
            "Выгрузить CSV", 
            constants.export_csv_btn_ss, 
            self.export_solution_to_csv
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

    # def highlight_solution_table(self):
    #     if not self.solution_table.rowCount() or not self.solution_table.columnCount():
    #         return
        
    #     for row in range(self.solution_table.rowCount()):
    #         for col in range(self.solution_table.columnCount()):
    #             item = self.solution_table.item(row, col)
    #             if item:
    #                 item.setBackground(self.brushes["white"])
        
    #     for row in range(self.solution_table.rowCount()):
    #         for col in range(self.solution_table.columnCount()):
    #             item = self.solution_table.item(row, col)
    #             if item:
    #                 item.setBackground(self.brushes["lime"])
    #                 if item.text() != "0" and item.text() != "":
    #                     item.setBackground(self.brushes["green"])
    
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

    def solve(self):
        match self.problem_type:
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
                self.transportation_problem.solution_table.clearSpans()
                self.transportation_problem.solve()
                self.solution_table.setCurrentWidget(self.transportation_problem.solution_table) 
        self.show_solution_page()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransportationSolver()
    window.show()
    sys.exit(app.exec())
