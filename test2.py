import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                               QTableWidget, QTableWidgetItem, QComboBox, 
                               QMessageBox, QSpinBox)
from PySide6.QtCore import Qt
from scipy.optimize import linprog
import numpy as np


class LPPSolverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решатель задач линейного программирования")
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Настройка задачи
        setup_layout = QHBoxLayout()
        
        # Количество переменных
        vars_layout = QVBoxLayout()
        vars_layout.addWidget(QLabel("Количество переменных:"))
        self.var_spin = QSpinBox()
        self.var_spin.setRange(2, 10)
        self.var_spin.setValue(2)
        vars_layout.addWidget(self.var_spin)
        
        # Количество ограничений
        constraints_layout = QVBoxLayout()
        constraints_layout.addWidget(QLabel("Количество ограничений:"))
        self.constraint_spin = QSpinBox()
        self.constraint_spin.setRange(1, 10)
        self.constraint_spin.setValue(2)
        constraints_layout.addWidget(self.constraint_spin)
        
        # Тип задачи
        problem_type_layout = QVBoxLayout()
        problem_type_layout.addWidget(QLabel("Тип задачи:"))
        self.problem_type = QComboBox()
        self.problem_type.addItems(["Минимизация", "Максимизация"])
        problem_type_layout.addWidget(self.problem_type)
        
        setup_layout.addLayout(vars_layout)
        setup_layout.addLayout(constraints_layout)
        setup_layout.addLayout(problem_type_layout)
        
        main_layout.addLayout(setup_layout)
        
        # Коэффициенты целевой функции
        main_layout.addWidget(QLabel("Коэффициенты целевой функции:"))
        self.objective_table = QTableWidget()
        self.objective_table.setRowCount(1)
        self.objective_table.setColumnCount(self.var_spin.value())
        main_layout.addWidget(self.objective_table)
        
        # Ограничения
        constraints_label = QLabel("Ограничения (левая часть <= правой части):")
        main_layout.addWidget(constraints_label)
        
        self.constraints_table = QTableWidget()
        self.constraints_table.setRowCount(self.constraint_spin.value())
        self.constraints_table.setColumnCount(self.var_spin.value() + 1)  # +1 для правой части
        main_layout.addWidget(self.constraints_table)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        self.update_button = QPushButton("Обновить таблицы")
        self.update_button.clicked.connect(self.update_tables)
        buttons_layout.addWidget(self.update_button)
        
        self.solve_button = QPushButton("Решить задачу")
        self.solve_button.clicked.connect(self.solve_problem)
        buttons_layout.addWidget(self.solve_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Результат
        self.result_label = QLabel("Решение появится здесь...")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        main_layout.addWidget(self.result_label)
        
        self.central_widget.setLayout(main_layout)
        
        # Инициализация таблиц
        self.update_tables()
        
    def update_tables(self):
        var_count = self.var_spin.value()
        constraint_count = self.constraint_spin.value()
        
        # Обновить таблицу целевой функции
        self.objective_table.setColumnCount(var_count)
        for i in range(var_count):
            if self.objective_table.item(0, i) is None:
                item = QTableWidgetItem("0")
                self.objective_table.setItem(0, i, item)
            self.objective_table.setHorizontalHeaderItem(i, QTableWidgetItem(f"x{i+1}"))
        
        # Обновить таблицу ограничений
        self.constraints_table.setRowCount(constraint_count)
        self.constraints_table.setColumnCount(var_count + 1)
        
        for i in range(var_count):
            if self.constraints_table.horizontalHeaderItem(i) is None:
                self.constraints_table.setHorizontalHeaderItem(i, QTableWidgetItem(f"x{i+1}"))
        
        if self.constraints_table.horizontalHeaderItem(var_count) is None:
            self.constraints_table.setHorizontalHeaderItem(var_count, QTableWidgetItem("RHS"))
        
        for row in range(constraint_count):
            for col in range(var_count + 1):
                if self.constraints_table.item(row, col) is None:
                    item = QTableWidgetItem("0")
                    self.constraints_table.setItem(row, col, item)
    
    def solve_problem(self):
        try:
            # Получить данные из таблиц
            var_count = self.var_spin.value()
            constraint_count = self.constraint_spin.value()
            
            # Целевая функция
            c = []
            for i in range(var_count):
                item = self.objective_table.item(0, i)
                c.append(float(item.text()))
            c = np.array(c)
            
            # Ограничения
            A = []
            b = []
            for row in range(constraint_count):
                row_data = []
                for col in range(var_count):
                    item = self.constraints_table.item(row, col)
                    row_data.append(float(item.text()))
                
                rhs_item = self.constraints_table.item(row, var_count)
                rhs = float(rhs_item.text())
                
                A.append(row_data)
                b.append(rhs)
            
            A = np.array(A)
            b = np.array(b)
            
            # Решить задачу
            if self.problem_type.currentText() == "Максимизация":
                result = linprog(-c, A_ub=A, b_ub=b, method='highs')
                result.fun = -result.fun  # Инвертируем обратно для максимизации
            else:
                result = linprog(c, A_ub=A, b_ub=b, method='highs')
            
            # Отобразить результат
            if result.success:
                solution = ", ".join([f"x{i+1} = {val:.2f}" for i, val in enumerate(result.x)])
                output = (f"Оптимальное значение: {result.fun:.2f}\n"
                          f"Решение: {solution}\n"
                          f"Итераций: {result.nit}")
                self.result_label.setText(output)
            else:
                self.result_label.setText("Решение не найдено. Проверьте ограничения.")
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
            self.result_label.setText("Ошибка при решении задачи.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LPPSolverApp()
    window.show()
    sys.exit(app.exec())