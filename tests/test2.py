import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QGroupBox, QPushButton,
    QLabel, QSpinBox, QComboBox, QTabWidget, QTextEdit
)
from PySide6.QtCore import Qt


class TransportationProblemSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transportation Problem Solver")
        self.setGeometry(100, 100, 900, 700)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        self.create_control_panel()
        self.create_input_tables()
        self.create_solution_display()
        
    def create_control_panel(self):
        """Create the control panel with problem setup options"""
        control_group = QGroupBox("Problem Setup")
        control_layout = QHBoxLayout()
        
        # Source (supply) controls
        source_layout = QVBoxLayout()
        source_layout.addWidget(QLabel("Number of Sources:"))
        self.source_spin = QSpinBox()
        self.source_spin.setRange(1, 20)
        self.source_spin.setValue(3)
        self.source_spin.valueChanged.connect(self.update_tables)
        source_layout.addWidget(self.source_spin)
        
        # Destination (demand) controls
        dest_layout = QVBoxLayout()
        dest_layout.addWidget(QLabel("Number of Destinations:"))
        self.dest_spin = QSpinBox()
        self.dest_spin.setRange(1, 20)
        self.dest_spin.setValue(3)
        self.dest_spin.valueChanged.connect(self.update_tables)
        dest_layout.addWidget(self.dest_spin)
        
        # Method selection
        method_layout = QVBoxLayout()
        method_layout.addWidget(QLabel("Solution Method:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Northwest Corner",
            "Least Cost",
            "Vogel's Approximation",
            "MODI Method"
        ])
        method_layout.addWidget(self.method_combo)
        
        # Solve button
        solve_layout = QVBoxLayout()
        self.solve_button = QPushButton("Solve Problem")
        self.solve_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.solve_button.clicked.connect(self.solve_problem)
        solve_layout.addWidget(self.solve_button)
        
        # Add all control sections to main control layout
        control_layout.addLayout(source_layout)
        control_layout.addLayout(dest_layout)
        control_layout.addLayout(method_layout)
        control_layout.addLayout(solve_layout)
        control_layout.addStretch()
        
        control_group.setLayout(control_layout)
        self.main_layout.addWidget(control_group)
    
    def create_input_tables(self):
        """Create tables for supply, demand, and cost inputs"""
        tables_group = QGroupBox("Problem Data")
        tables_layout = QHBoxLayout()
        
        # Supply table
        supply_group = QGroupBox("Supply")
        self.supply_table = QTableWidget()
        self.supply_table.setColumnCount(1)
        self.supply_table.setRowCount(self.source_spin.value())
        self.supply_table.setHorizontalHeaderLabels(["Supply"])
        self.supply_table.setVerticalHeaderLabels([f"Source {i+1}" for i in range(self.source_spin.value())])
        supply_layout = QVBoxLayout()
        supply_layout.addWidget(self.supply_table)
        supply_group.setLayout(supply_layout)
        
        # Cost table
        cost_group = QGroupBox("Transportation Costs")
        self.cost_table = QTableWidget()
        self.cost_table.setColumnCount(self.dest_spin.value())
        self.cost_table.setRowCount(self.source_spin.value())
        self.cost_table.setHorizontalHeaderLabels([f"Dest {i+1}" for i in range(self.dest_spin.value())])
        self.cost_table.setVerticalHeaderLabels([f"Source {i+1}" for i in range(self.source_spin.value())])
        cost_layout = QVBoxLayout()
        cost_layout.addWidget(self.cost_table)
        cost_group.setLayout(cost_layout)
        
        # Demand table
        demand_group = QGroupBox("Demand")
        self.demand_table = QTableWidget()
        self.demand_table.setColumnCount(self.dest_spin.value())
        self.demand_table.setRowCount(1)
        self.demand_table.setVerticalHeaderLabels(["Demand"])
        self.demand_table.setHorizontalHeaderLabels([f"Dest {i+1}" for i in range(self.dest_spin.value())])
        demand_layout = QVBoxLayout()
        demand_layout.addWidget(self.demand_table)
        demand_group.setLayout(demand_layout)
        
        # Add tables to layout
        tables_layout.addWidget(supply_group)
        tables_layout.addWidget(cost_group)
        tables_layout.addWidget(demand_group)
        
        tables_group.setLayout(tables_layout)
        self.main_layout.addWidget(tables_group)
    
    def create_solution_display(self):
        """Create the area to display the solution"""
        solution_group = QGroupBox("Solution")
        solution_layout = QVBoxLayout()
        
        self.tab_widget = QTabWidget()
        
        # Solution matrix tab
        self.solution_table = QTableWidget()
        self.solution_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tab_widget.addTab(self.solution_table, "Allocation Matrix")
        
        # Step-by-step solution tab
        self.steps_text = QTextEdit()
        self.steps_text.setReadOnly(True)
        self.tab_widget.addTab(self.steps_text, "Solution Steps")
        
        # Summary tab
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.tab_widget.addTab(self.summary_text, "Solution Summary")
        
        solution_layout.addWidget(self.tab_widget)
        
        # Total cost display
        total_layout = QHBoxLayout()
        total_layout.addWidget(QLabel("Total Transportation Cost:"))
        self.total_cost_label = QLabel("0")
        self.total_cost_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        total_layout.addWidget(self.total_cost_label)
        total_layout.addStretch()
        
        solution_layout.addLayout(total_layout)
        solution_group.setLayout(solution_layout)
        self.main_layout.addWidget(solution_group)
    
    def update_tables(self):
        """Update table dimensions when source/destination counts change"""
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        
        # Update supply table
        self.supply_table.setRowCount(sources)
        self.supply_table.setVerticalHeaderLabels([f"Source {i+1}" for i in range(sources)])
        
        # Update cost table
        self.cost_table.setRowCount(sources)
        self.cost_table.setColumnCount(destinations)
        self.cost_table.setVerticalHeaderLabels([f"Source {i+1}" for i in range(sources)])
        self.cost_table.setHorizontalHeaderLabels([f"Dest {i+1}" for i in range(destinations)])
        
        # Update demand table
        self.demand_table.setColumnCount(destinations)
        self.demand_table.setHorizontalHeaderLabels([f"Dest {i+1}" for i in range(destinations)])
    
    def solve_problem(self):
        """Placeholder for solving the transportation problem"""
        # This would be implemented with the actual solving methods
        method = self.method_combo.currentText()
        
        # For now, just display a placeholder solution
        self.display_solution_placeholder(method)
    
    def display_solution_placeholder(self, method):
        """Display placeholder solution data (for UI demonstration)"""
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        
        # Update solution table
        self.solution_table.setRowCount(sources)
        self.solution_table.setColumnCount(destinations)
        self.solution_table.setHorizontalHeaderLabels([f"Dest {i+1}" for i in range(destinations)])
        self.solution_table.setVerticalHeaderLabels([f"Source {i+1}" for i in range(sources)])
        
        # Fill with placeholder values
        for i in range(sources):
            for j in range(destinations):
                item = QTableWidgetItem(f"{i+j+1}")
                item.setTextAlignment(Qt.AlignCenter)
                self.solution_table.setItem(i, j, item)
        
        # Update steps text
        self.steps_text.setPlainText(
            f"Solution steps using {method} method:\n\n"
            "1. Step one description\n"
            "2. Step two description\n"
            "3. Step three description\n"
            "4. Final allocation"
        )
        
        # Update summary
        self.summary_text.setPlainText(
            f"Problem solved using {method} method\n\n"
            f"Sources: {sources}\n"
            f"Destinations: {destinations}\n"
            "Total cost: 1000 (example)"
        )
        
        # Update total cost
        self.total_cost_label.setText("1000")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransportationProblemSolver()
    window.show()
    sys.exit(app.exec())