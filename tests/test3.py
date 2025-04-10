import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QGroupBox, QPushButton,
    QLabel, QSpinBox, QComboBox, QTextEdit
)
from PySide6.QtCore import Qt


class TransportationSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transportation Problem Solver")
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        self.create_controls()
        self.create_input_table()
        self.create_output_display()
        
        # Initialize with default problem size
        self.update_table_size()
    
    def create_controls(self):
        """Create control panel with problem setup options"""
        control_group = QGroupBox("Problem Setup")
        control_layout = QHBoxLayout()
        
        # Source controls
        source_layout = QVBoxLayout()
        source_layout.addWidget(QLabel("Sources:"))
        self.source_spin = QSpinBox()
        self.source_spin.setRange(1, 10)
        self.source_spin.setValue(3)
        self.source_spin.valueChanged.connect(self.update_table_size)
        source_layout.addWidget(self.source_spin)
        
        # Destination controls
        dest_layout = QVBoxLayout()
        dest_layout.addWidget(QLabel("Destinations:"))
        self.dest_spin = QSpinBox()
        self.dest_spin.setRange(1, 10)
        self.dest_spin.setValue(3)
        self.dest_spin.valueChanged.connect(self.update_table_size)
        dest_layout.addWidget(self.dest_spin)
        
        # Method selection
        method_layout = QVBoxLayout()
        method_layout.addWidget(QLabel("Method:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Northwest Corner",
            "Least Cost",
            "Vogel's Approximation",
            "MODI Method"
        ])
        method_layout.addWidget(self.method_combo)
        
        # Solve button
        self.solve_btn = QPushButton("Solve")
        self.solve_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        self.solve_btn.clicked.connect(self.solve_problem)
        
        # Add all controls to layout
        control_layout.addLayout(source_layout)
        control_layout.addLayout(dest_layout)
        control_layout.addLayout(method_layout)
        control_layout.addWidget(self.solve_btn)
        control_layout.addStretch()
        
        control_group.setLayout(control_layout)
        self.main_layout.addWidget(control_group)
    
    def create_input_table(self):
        """Create the main input table for all problem data"""
        self.input_table = QTableWidget()
        self.input_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        
        # Configure table headers
        self.input_table.horizontalHeader().setStretchLastSection(True)
        self.input_table.verticalHeader().setStretchLastSection(True)
        
        input_group = QGroupBox("Problem Data")
        layout = QVBoxLayout()
        layout.addWidget(self.input_table)
        input_group.setLayout(layout)
        self.main_layout.addWidget(input_group)
    
    def create_output_display(self):
        """Create the output display area"""
        output_group = QGroupBox("Solution")
        layout = QVBoxLayout()
        
        # Solution matrix
        self.solution_table = QTableWidget()
        self.solution_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.solution_table.setStyleSheet("QTableWidget { font-size: 12px; }")
        
        # Solution summary
        self.solution_text = QTextEdit()
        self.solution_text.setReadOnly(True)
        self.solution_text.setStyleSheet("font-family: monospace;")
        
        layout.addWidget(QLabel("Optimal Allocation:"))
        layout.addWidget(self.solution_table)
        layout.addWidget(QLabel("Solution Summary:"))
        layout.addWidget(self.solution_text)
        
        output_group.setLayout(layout)
        self.main_layout.addWidget(output_group)
    
    def update_table_size(self):
        """Update the input table dimensions based on sources/destinations"""
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        
        # Set row and column count (sources + 1 for demand row, destinations + 1 for supply column)
        self.input_table.setRowCount(sources + 1)
        self.input_table.setColumnCount(destinations + 1)
        
        # Set headers
        headers = [f"Dest {j+1}" for j in range(destinations)] + ["Supply"]
        self.input_table.setHorizontalHeaderLabels(headers)
        
        row_headers = [f"Source {i+1}" for i in range(sources)] + ["Demand"]
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
        
        # Bottom-right cell (should be empty or show balance)
        item = QTableWidgetItem()
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.input_table.setItem(sources, destinations, item)
    
    def solve_problem(self):
        """Generate and display dummy solution"""
        sources = self.source_spin.value()
        destinations = self.dest_spin.value()
        method = self.method_combo.currentText()
        
        # Create solution table
        self.solution_table.setRowCount(sources)
        self.solution_table.setColumnCount(destinations)
        self.solution_table.setHorizontalHeaderLabels([f"Dest {j+1}" for j in range(destinations)])
        self.solution_table.setVerticalHeaderLabels([f"Source {i+1}" for i in range(sources)])
        
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
        summary = f"""=== Transportation Problem Solution ===
Method: {method}

Sources: {sources}
Destinations: {destinations}

Total Cost: {total_cost}

Allocation Summary:
"""
        for i in range(sources):
            for j in range(destinations):
                value = self.solution_table.item(i, j).text()
                summary += f"Source {i+1} → Dest {j+1}: {value} units\n"
        
        self.solution_text.setPlainText(summary)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransportationSolver()
    window.show()
    sys.exit(app.exec())