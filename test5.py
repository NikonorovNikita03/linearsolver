import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit

class InputWithLabel(QWidget):
    def __init__(self):
        super().__init__()
        
        # Основной layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)  # Это spacing между группами полей
        
        # Первое поле с начальным текстом
        self.create_input_field(layout, "Логин:", "Введите ваш логин", text="user123", spacing=0)
        
        # Второе поле без начального текста
        self.create_input_field(layout, "Пароль:", "Введите пароль", spacing=2)
        
        # Настройки окна
        self.setWindowTitle("Стилизованные поля ввода")
        self.resize(300, 150)
    
    def create_input_field(self, layout, label_text, placeholder, text=None, spacing=0):
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(spacing)
        
        label = QLabel(label_text)
        label.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 12px;
                font-weight: bold;
                margin: 0;
                padding: 0;
            }
        """)
        label.setContentsMargins(0, 0, 0, 0)
        
        # Поле ввода
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        
        if text is not None:
            line_edit.setText(text)
        
        line_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 4px 6px;
                font-size: 14px;
                margin: 0;
            }
            QLineEdit:focus {
                border: 1px solid #0066ff;
            }
        """)
        line_edit.setContentsMargins(0, 0, 0, 0)
        
        container_layout.addWidget(label)
        container_layout.addWidget(line_edit)
        
        layout.addWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyleSheet("""
        QWidget {
            background-color: #f5f5f5;
            font-family: 'Segoe UI', Arial;
        }
    """)
    
    window = InputWithLabel()
    window.show()
    
    sys.exit(app.exec())