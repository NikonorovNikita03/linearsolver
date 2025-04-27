import sys
import csv
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QGroupBox, QPushButton,
    QLabel, QSpinBox, QMessageBox, QFileDialog, QStackedWidget, QHeaderView,
    #QTextEdit
)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QIcon, QColor, QBrush
from solver import Solver
#from TransportProblemParser import TransportProblemParser
import constants
import functions


class TransportationSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение задач линейного программирования")
        self.settings = functions.get_settings()
        self.setGeometry(100, 100, self.settings["width"], self.settings["height"])

        self.costs = [
            [4, 8, 8],
            [16, 24, 16],
            [8, 16, 24]
        ]
        self.supply = [76, 82, 77]
        self.demand = [72, 102, 41]
        # self.costs = [[1 for x in range(self.settings["size_x"])] for y in range(self.settings["size_y"])]
        # self.supply = [2 for y in range(self.settings["size_y"])]
        # self.demand = [3 for x in range(self.settings["size_x"])]
        self.total_cost = 0

        self.supply_labels =  [f"Поставщик {x}" for x in range(1, self.settings["size_y"] + 1)] + ["Потребители"]
        self.demand_labels = [f"Потребитель {x}" for x in range(1, self.settings["size_x"] + 1)] + ["Поставщики"]

        self.brushes = {}
        for color in constants.colors.items():
            self.brushes[color[0]] = QBrush(QColor(*color[1]))

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
        self.create_combined_input_table()
        
        self.solution_page = QWidget()
        self.create_solution_page()
        
        # self.text_input_page = QWidget()
        # self.create_text_input_page()
        
        self.stacked_widget.addWidget(self.input_page)
        self.stacked_widget.addWidget(self.solution_page)
        # self.stacked_widget.addWidget(self.text_input_page)
        
        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.addWidget(self.status_label)

        self.update_table_size()
        self.write_data_into_input_table()
    
    def q_push_button(self, name, style, function, cursor=True):
        btn = QPushButton(name)
        btn.setStyleSheet(style)
        btn.clicked.connect(function)
        if cursor:
            btn.setCursor(Qt.PointingHandCursor)
        return btn

    # def create_text_input_page(self):
    #     layout = QVBoxLayout()
    #     layout.setContentsMargins(20, 20, 20, 20)
        
    #     title_label = QLabel("Текстовый ввод данных")
    #     title_label.setAlignment(Qt.AlignCenter)
    #     title_label.setStyleSheet(constants.title_label)
    #     layout.addWidget(title_label)
        
    #     self.text_edit = QTextEdit()
    #     self.text_edit.setPlaceholderText(constants.text_edit_placeholder)
    #     layout.addWidget(self.text_edit)
        
    #     button_layout = QHBoxLayout()
        
    #     back_btn = self.q_push_button("Назад", "background-color: #607D8B; color: white;", self.show_input_page)
    #     enter_btn = self.q_push_button("Ввести", "background-color: #4CAF50; color: white;", self.process_text_input)

    #     button_layout.addWidget(back_btn)
    #     button_layout.addStretch()
    #     button_layout.addWidget(enter_btn)
        
    #     layout.addLayout(button_layout)
    #     self.text_input_page.setLayout(layout)
    
    def create_controls(self):
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(5, 5, 5, 5)
        control_layout.setSpacing(10)
        
        source_layout = QVBoxLayout()
        source_layout.setSpacing(0)
        source_layout.addWidget(QLabel("Поставщики:"))
        self.source_spin = QSpinBox()
        self.source_spin.setRange(1, 10)
        self.source_spin.setValue(self.settings["size_y"])
        self.source_spin.valueChanged.connect(self.update_input_table)
        source_layout.addWidget(self.source_spin)
        
        dest_layout = QVBoxLayout()
        dest_layout.setSpacing(0)
        dest_layout.addWidget(QLabel("Потребители:"))
        self.dest_spin = QSpinBox()
        self.dest_spin.setRange(1, 10)
        self.dest_spin.setValue(self.settings["size_x"])
        self.dest_spin.valueChanged.connect(self.update_input_table)
        dest_layout.addWidget(self.dest_spin)
        
        #self.text_input_btn = self.q_push_button("Ввести текстом", constants.text_input_btn, self.show_text_input_page)
        self.solve_btn = self.q_push_button("Решить", constants.solve_btn, self.solve_problem)
        
        self.back_btn = self.q_push_button("Назад", constants.back_btn_ss, self.show_input_page)
        self.back_btn.setVisible(False)
        
        control_layout.addLayout(source_layout)
        control_layout.addLayout(dest_layout)
        control_layout.addStretch()
        #control_layout.addWidget(self.text_input_btn)
        control_layout.addWidget(self.back_btn)
        control_layout.addWidget(self.solve_btn)
        
        self.control_group.setLayout(control_layout)
        self.main_layout.addWidget(self.control_group)

    def create_combined_input_table(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        group = QGroupBox("Ввод данных задачи")
        group_layout = QVBoxLayout()
        
        self.combined_table = QTableWidget()
        self.combined_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        
        btn_layout = QHBoxLayout()
        copy_btn = self.q_push_button("Копировать", "background-color: #2196F3; color: white;", 
                                    lambda: self.copy_table_data(self.combined_table))
        paste_btn = self.q_push_button("Вставить", "background-color: #FF9800; color: white;", 
                                    lambda: self.paste_data_to_table(self.combined_table))
        
        btn_layout.addStretch()
        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(paste_btn)
        
        group_layout.addWidget(self.combined_table)
        group_layout.addLayout(btn_layout)
        group.setLayout(group_layout)
        
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

    # def process_text_input(self):
    #     tpp = TransportProblemParser(self.text_edit.toPlainText())
    #     print(tpp.parse_transport_problem())
    #     self.show_input_page()
    
    # def show_text_input_page(self):        
    #     self.control_group.setVisible(False)
    #     self.stacked_widget.setCurrentIndex(2)
    #     self.solve_btn.setVisible(False)
    #     self.back_btn.setVisible(False)
    #     #self.text_input_btn.setVisible(False)
    
    def show_input_page(self):        
        self.control_group.setVisible(True)
        self.stacked_widget.setCurrentIndex(0)
        self.solve_btn.setVisible(True)
        self.back_btn.setVisible(False)
        #self.text_input_btn.setVisible(True)
    
    def show_solution_page(self):
        self.control_group.setVisible(True)
        self.stacked_widget.setCurrentIndex(1)
        self.solve_btn.setVisible(False)
        self.back_btn.setVisible(True)
        #self.text_input_btn.setVisible(False)
    
    def create_solution_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
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
    
    def get_data_from_input_table(self):
        rows = self.combined_table.rowCount()
        cols = self.combined_table.columnCount()
        
        if rows < 2 or cols < 2:
            raise ValueError("Таблица должна содержать хотя бы одного поставщика и потребителя")
        
        self.supply = []
        for row in range(1, rows):
            item = self.combined_table.item(row, 0)
            self.supply.append(int(item.text()) if item and item.text().isdigit() else 0)
        
        self.demand = []
        for col in range(1, cols):
            item = self.combined_table.item(0, col)
            self.demand.append(int(item.text()) if item and item.text().isdigit() else 0)
        
        self.costs = []
        for row in range(1, rows):
            cost_row = []
            for col in range(1, cols):
                item = self.combined_table.item(row, col)
                cost_row.append(int(item.text()) if item and item.text().isdigit() else 0)
            self.costs.append(cost_row)
    
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
    
    def solve_problem(self):
        # try:
            
        # except Exception as e:
        #     QMessageBox.critical(self, "Ошибка", f"Не удалось решить задачу:\n{str(e)}")
        #     self.show_status_message(f"Ошибка: {str(e)}")

        self.get_data_from_input_table()
        costs, supply, demand = self.costs, self.supply, self.demand
        
        print(supply, demand, costs)
        problem = Solver(supply, demand, costs)
        result_matrix, self.total_cost = problem.solve_transportation_scipy()

        sources = len(result_matrix)
        destinations = len(result_matrix[0]) if sources > 0 else 0

        

        print(self.demand_labels)
        to_write = [[""] + self.demand_labels[0:self.settings["size_x"]]]
        #if 
        print(result_matrix)
        for i in range(0, self.settings["size_y"]):
            print(i)
            this = [self.supply_labels[i]] + result_matrix[i].tolist()
            to_write.append(this)
        
        self.solution_table.setRowCount(len(to_write))
        self.solution_table.setColumnCount(len(to_write[0]))

        for y in range(len(to_write)):
            for x in range(len(to_write[0])):
                print(y, x)
                item = QTableWidgetItem(str(to_write[y][x]))
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