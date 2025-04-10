import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QGroupBox, QPushButton,
    QLabel, QSpinBox, QComboBox, QTextEdit, QMessageBox, QTabWidget, QStatusBar,
    QHeaderView
)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QClipboard, QPalette, QColor


class TransportationSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение транспортной задачи")
        self.setGeometry(100, 100, 800, 600)
        
        # Флаг текущей темы (True - темная, False - светлая)
        self.dark_theme = True
        self.apply_theme()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        # Создаём отдельный виджет для статуса
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        
        self.create_controls()
        self.create_input_table()
        self.create_solution_tabs()
        
        # Добавляем виджет статуса в основной layout
        self.main_layout.addWidget(self.status_label)
        
        # Initialize with default problem size
        self.update_table_size()
    
    def apply_theme(self):
        """Apply the current theme (dark or light)"""
        palette = QPalette()
        
        if self.dark_theme:
            # Темная тема
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(35, 35, 35))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
            palette.setColor(QPalette.HighlightedText, Qt.black)
            palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
            palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
            
            self.setStyleSheet("""
                QGroupBox {
                    border: 1px solid #444;
                    border-radius: 3px;
                    margin-top: 10px;
                    padding-top: 13px;
                    background: #353535;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 7px;
                    padding: 0 3px;
                }
                QStatusBar {
                    background: #353535;
                    color: white;
                }
                QTabBar::tab {
                    background: #353535;
                    color: white;
                    border: 1px solid #444;
                }
                QTabBar::tab:selected {
                    background: #555;
                }
            """)
        else:
            # Светлая тема
            palette.setColor(QPalette.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
            palette.setColor(QPalette.HighlightedText, Qt.white)
            palette.setColor(QPalette.Disabled, QPalette.Text, Qt.gray)
            palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.gray)
            
            self.setStyleSheet("""
                QGroupBox {
                    border: 1px solid #ccc;
                    border-radius: 3px;
                    margin-top: 10px;
                    padding-top: 13px;
                    background: #f0f0f0;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 7px;
                    padding: 0 3px;
                }
                QStatusBar {
                    background: #f0f0f0;
                    color: black;
                }
                QTabBar::tab {
                    background: #f0f0f0;
                    color: black;
                    border: 1px solid #ccc;
                }
                QTabBar::tab:selected {
                    background: white;
                }
            """)
        
        QApplication.setPalette(palette)
    
    def create_controls(self):
        """Create control panel with problem setup options"""
        control_group = QGroupBox("Настройка задачи")
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(5, 5, 5, 5)
        control_layout.setSpacing(10)
        
        # Source controls
        source_layout = QVBoxLayout()
        source_layout.setSpacing(0)
        source_layout.addWidget(QLabel("Поставщики:"))
        self.source_spin = QSpinBox()
        self.source_spin.setRange(1, 10)
        self.source_spin.setValue(3)
        self.source_spin.valueChanged.connect(self.update_table_size)
        source_layout.addWidget(self.source_spin)
        
        # Destination controls
        dest_layout = QVBoxLayout()
        dest_layout.setSpacing(0)
        dest_layout.addWidget(QLabel("Потребители:"))
        self.dest_spin = QSpinBox()
        self.dest_spin.setRange(1, 10)
        self.dest_spin.setValue(3)
        self.dest_spin.valueChanged.connect(self.update_table_size)
        dest_layout.addWidget(self.dest_spin)
        
        # Method selection
        method_layout = QVBoxLayout()
        method_layout.setSpacing(0)
        method_layout.addWidget(QLabel("Метод:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Северо-западный угол",
            "Минимальный элемент",
            "Метод Фогеля",
            "Метод MODI"
        ])
        method_layout.addWidget(self.method_combo)
        
        # Theme toggle button
        self.theme_btn = QPushButton("Светлая тема" if self.dark_theme else "Темная тема")
        self.theme_btn.setFixedHeight(30)
        self.theme_btn.clicked.connect(self.toggle_theme)
        
        # Solve button
        self.solve_btn = QPushButton("Решить")
        self.solve_btn.setFixedHeight(60)
        self.solve_btn.clicked.connect(self.solve_problem)
        
        # Update button styles
        self.update_button_styles()
        
        # Add all controls to layout
        control_layout.addLayout(source_layout)
        control_layout.addLayout(dest_layout)
        control_layout.addLayout(method_layout)
        control_layout.addStretch()
        control_layout.addWidget(self.theme_btn)
        control_layout.addWidget(self.solve_btn)
        
        control_group.setLayout(control_layout)
        self.main_layout.addWidget(control_group)
    
    def update_button_styles(self):
        """Update button styles according to current theme"""
        if self.dark_theme:
            self.solve_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50; 
                    color: white; 
                    padding: 8px;
                    margin-top: 18px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            self.theme_btn.setStyleSheet("""
                QPushButton {
                    background-color: #555; 
                    color: white; 
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #666;
                }
            """)
        else:
            self.solve_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50; 
                    color: white; 
                    padding: 8px;
                    margin-top: 18px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            self.theme_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e0e0e0; 
                    color: black; 
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
            """)
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        self.dark_theme = not self.dark_theme
        self.theme_btn.setText("Светлая тема" if self.dark_theme else "Темная тема")
        self.apply_theme()
        self.update_button_styles()
        
        # Обновляем стили таблиц
        table_style = "QTableWidget { font-size: 12px; background: %s; color: %s; gridline-color: %s; }" % (
            "#353535" if self.dark_theme else "white",
            "white" if self.dark_theme else "black",
            "#444" if self.dark_theme else "#ccc"
        )
        self.input_table.setStyleSheet(table_style)
        self.solution_table.setStyleSheet(table_style)
        
        # Обновляем стиль текстового поля
        text_style = "font-family: monospace; background: %s; color: %s;" % (
            "#353535" if self.dark_theme else "white",
            "white" if self.dark_theme else "black"
        )
        self.solution_text.setStyleSheet(text_style)
        
        # Обновляем стиль статусной строки
        status_style = "padding: 3px; background: %s; color: %s; border-top: 1px solid %s;" % (
            "#353535" if self.dark_theme else "#f0f0f0",
            "white" if self.dark_theme else "black",
            "#444" if self.dark_theme else "#ccc"
        )
        self.status_label.setStyleSheet(status_style)
    
    def create_input_table(self):
        """Create the main input table for all problem data"""
        input_group = QGroupBox("Исходные данные")
        layout = QVBoxLayout()
        
        # Create table
        self.input_table = QTableWidget()
        self.input_table.setStyleSheet("QTableWidget { font-size: 12px; background: #353535; color: white; gridline-color: #444; }")
        self.input_table.itemChanged.connect(self.update_balance_cell)
        
        # Configure table headers and resize behavior
        header = self.input_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignCenter)
        
        v_header = self.input_table.verticalHeader()
        v_header.setSectionResizeMode(QHeaderView.Stretch)
        v_header.setDefaultAlignment(Qt.AlignCenter)
        
        # Create button row
        btn_layout = QHBoxLayout()
        
        # Copy button
        copy_btn = QPushButton("Копировать данные")
        copy_btn.setStyleSheet("background-color: #2196F3; color: white;")
        copy_btn.clicked.connect(lambda: self.copy_table_data(self.input_table))
        
        # Paste button
        paste_btn = QPushButton("Вставить данные")
        paste_btn.setStyleSheet("background-color: #FF9800; color: white;")
        paste_btn.clicked.connect(self.paste_data_to_table)
        
        btn_layout.addStretch()
        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(paste_btn)
        
        layout.addWidget(self.input_table)
        layout.addLayout(btn_layout)
        input_group.setLayout(layout)
        self.main_layout.addWidget(input_group)
    
    def create_solution_tabs(self):
        """Create tab widget for solution display"""
        self.tabs = QTabWidget()
        
        # Tab 1: Solution matrix
        self.solution_tab = QWidget()
        solution_layout = QVBoxLayout()
        
        self.solution_table = QTableWidget()
        self.solution_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.solution_table.setStyleSheet("QTableWidget { font-size: 12px; background: #353535; color: white; gridline-color: #444; }")
        
        # Configure solution table resize behavior
        s_header = self.solution_table.horizontalHeader()
        s_header.setSectionResizeMode(QHeaderView.Stretch)
        s_header.setDefaultAlignment(Qt.AlignCenter)
        
        s_v_header = self.solution_table.verticalHeader()
        s_v_header.setSectionResizeMode(QHeaderView.Stretch)
        s_v_header.setDefaultAlignment(Qt.AlignCenter)
        
        solution_copy_btn = QPushButton("Копировать решение")
        solution_copy_btn.setStyleSheet("background-color: #2196F3; color: white;")
        solution_copy_btn.clicked.connect(lambda: self.copy_table_data(self.solution_table))
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(solution_copy_btn)
        
        solution_layout.addWidget(QLabel("Оптимальное распределение:"))
        solution_layout.addWidget(self.solution_table)
        solution_layout.addLayout(btn_layout)
        self.solution_tab.setLayout(solution_layout)
        
        # Tab 2: Solution summary
        self.summary_tab = QWidget()
        summary_layout = QVBoxLayout()
        
        self.solution_text = QTextEdit()
        self.solution_text.setReadOnly(True)
        self.solution_text.setStyleSheet("font-family: monospace; background: #353535; color: white;")
        
        summary_layout.addWidget(QLabel("Результаты:"))
        summary_layout.addWidget(self.solution_text)
        self.summary_tab.setLayout(summary_layout)
        
        # Add tabs
        self.tabs.addTab(self.solution_tab, "Распределение")
        self.tabs.addTab(self.summary_tab, "Результаты")
        
        self.main_layout.addWidget(self.tabs)
    
    def copy_table_data(self, table):
        """Copy only the cell values without headers to clipboard"""
        if not table:
            return
            
        # Get all data from the table
        data = []
        for row in range(table.rowCount()):
            row_data = []
            for col in range(table.columnCount()):
                item = table.item(row, col)
                row_data.append(item.text() if item else "")
            data.append("\t".join(row_data))
        
        # Put the data in clipboard
        clipboard = QApplication.clipboard()
        mime_data = QMimeData()
        mime_data.setText("\n".join(data))
        clipboard.setMimeData(mime_data)
        
        # Show temporary status message
        self.show_status_message("Данные скопированы в буфер обмена!")
    
    def paste_data_to_table(self):
        """Paste data from clipboard to input table"""
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        
        if not text:
            self.show_status_message("Буфер обмена пуст!")
            return
        
        # Split clipboard data into rows
        rows = [row for row in text.split('\n') if row.strip()]
        if not rows:
            self.show_status_message("Нет данных в буфере обмена!")
            return
        
        # Split each row into columns
        data = [row.split('\t') for row in rows]
        
        # Disconnect itemChanged signal to avoid multiple updates
        self.input_table.itemChanged.disconnect(self.update_balance_cell)
        
        try:
            # Insert as much data as possible without errors
            for row_idx in range(min(len(data), self.input_table.rowCount())):
                for col_idx in range(min(len(data[row_idx]), self.input_table.columnCount())):
                    # Skip bottom-right cell (balance cell)
                    if row_idx == self.input_table.rowCount()-1 and col_idx == self.input_table.columnCount()-1:
                        continue
                        
                    value = data[row_idx][col_idx]
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.input_table.setItem(row_idx, col_idx, item)
            
            self.show_status_message("Данные вставлены успешно!")
        except Exception as e:
            self.show_status_message(f"Ошибка при вставке данных: {str(e)}")
        finally:
            # Reconnect signal and update balance
            self.input_table.itemChanged.connect(self.update_balance_cell)
            self.update_balance_cell()
    
    def update_balance_cell(self):
        """Update the balance cell (bottom-right) with supply-demand difference"""
        # Disconnect signal to avoid recursion
        #self.input_table.itemChanged.disconnect(self.update_balance_cell)
        try:
            if self.input_table.receivers(self.input_table.itemChanged) > 0:
                self.input_table.itemChanged.disconnect(self.update_balance_cell)
        except RuntimeError:
            pass 
        
        try:
            sources = self.source_spin.value()
            destinations = self.dest_spin.value()
            
            # Calculate total supply
            total_supply = 0
            for i in range(sources):
                item = self.input_table.item(i, destinations)
                if item and item.text().isdigit():
                    total_supply += int(item.text())
            
            # Calculate total demand
            total_demand = 0
            for j in range(destinations):
                item = self.input_table.item(sources, j)
                if item and item.text().isdigit():
                    total_demand += int(item.text())
            
            # Update balance cell
            balance = total_supply - total_demand
            balance_item = self.input_table.item(sources, destinations)
            if not balance_item:
                balance_item = QTableWidgetItem()
                balance_item.setFlags(balance_item.flags() & ~Qt.ItemIsEditable)
                balance_item.setTextAlignment(Qt.AlignCenter)
                self.input_table.setItem(sources, destinations, balance_item)
            
            balance_item.setText(str(balance))
            
            # Color coding for balance
            if balance > 0:
                balance_item.setBackground(Qt.green)
            elif balance < 0:
                balance_item.setBackground(Qt.red)
            else:
                balance_item.setBackground(Qt.transparent)
                
        except Exception as e:
            print(f"Error updating balance: {e}")
        finally:
            # Reconnect signal
            self.input_table.itemChanged.connect(self.update_balance_cell)
    
    def show_status_message(self, message):
        """Display status message in the dedicated label"""
        self.status_label.setText(message)
    
    def update_table_size(self):
        """Update the input table dimensions based on sources/destinations"""
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        
        # Disconnect signal to avoid multiple updates
        self.input_table.itemChanged.disconnect(self.update_balance_cell)
        
        # Set row and column count (sources + 1 for demand row, destinations + 1 for supply column)
        self.input_table.setRowCount(sources + 1)
        self.input_table.setColumnCount(destinations + 1)
        
        # Set headers
        headers = [f"Потр. {j+1}" for j in range(destinations)] + ["Запасы"]
        self.input_table.setHorizontalHeaderLabels(headers)
        
        row_headers = [f"Пост. {i+1}" for i in range(sources)] + ["Потребности"]
        self.input_table.setVerticalHeaderLabels(row_headers)
        
        # Clear existing content
        self.input_table.clearContents()
        
        # Set placeholder values
        for i in range(sources):
            for j in range(destinations):
                item = QTableWidgetItem("10")
                item.setTextAlignment(Qt.AlignCenter)
                self.input_table.setItem(i, j, item)
            
            # Supply column
            item = QTableWidgetItem("100")
            item.setTextAlignment(Qt.AlignCenter)
            self.input_table.setItem(i, destinations, item)
        
        # Demand row
        for j in range(destinations):
            item = QTableWidgetItem("80")
            item.setTextAlignment(Qt.AlignCenter)
            self.input_table.setItem(sources, j, item)
        
        # Bottom-right cell (balance cell)
        balance_item = QTableWidgetItem()
        balance_item.setFlags(balance_item.flags() & ~Qt.ItemIsEditable)
        balance_item.setTextAlignment(Qt.AlignCenter)
        self.input_table.setItem(sources, destinations, balance_item)
        
        # Update balance and reconnect signal
        self.update_balance_cell()
        self.input_table.itemChanged.connect(self.update_balance_cell)
    
    def solve_problem(self):
        """Generate and display dummy solution"""
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        method = self.method_combo.currentText()
        
        # Create solution table
        self.solution_table.setRowCount(sources)
        self.solution_table.setColumnCount(destinations)
        self.solution_table.setHorizontalHeaderLabels([f"Потр. {j+1}" for j in range(destinations)])
        self.solution_table.setVerticalHeaderLabels([f"Пост. {i+1}" for i in range(sources)])
        
        # Fill with dummy solution values
        total_cost = 0
        for i in range(sources):
            for j in range(destinations):
                # Simple dummy allocation pattern
                value = (i + j + 1) * 10
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.solution_table.setItem(i, j, item)
                total_cost += value * (i + j + 1)  # Dummy cost calculation
        
        # Generate solution summary
        summary = f"""=== Решение транспортной задачи ===
Метод: {method}

Поставщики: {sources}
Потребители: {destinations}

Общая стоимость: {total_cost}

Распределение:
"""
        for i in range(sources):
            for j in range(destinations):
                value = self.solution_table.item(i, j).text()
                summary += f"Поставщик {i+1} → Потребитель {j+1}: {value} единиц\n"
        
        self.solution_text.setPlainText(summary)
        self.tabs.setCurrentIndex(0)  # Switch to solution tab
        self.show_status_message("Задача решена!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransportationSolver()
    window.show()
    sys.exit(app.exec())