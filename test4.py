import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Qt

class InputWithLabel(QWidget):
    def __init__(self):
        super().__init__()
        
        # Основной layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Первое поле
        self.create_input_field(layout, "Логин:", "Введите ваш логин")
        
        # Второе поле (пароль)
        self.create_input_field(layout, "Пароль:", "Введите пароль", True)
        
        # Настройки окна
        self.setWindowTitle("Стилизованные поля ввода")
        self.resize(300, 150)
    
    def create_input_field(self, layout, label_text, placeholder, is_password=False):
        """Создаёт стилизованное поле ввода с меткой"""
        # Метка
        label = QLabel(label_text)
        label.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 12px;
                font-weight: bold;
                padding-bottom: 2px;
            }
        """)
        
        # Поле ввода
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        
        if is_password:
            line_edit.setEchoMode(QLineEdit.Password)
        
        line_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;         
                padding: 6px;
                font-size: 14px;
                min-height: 25px;
            }
            QLineEdit:focus {
                border: 1px solid #0066ff;
            }
        """)
        
        # Добавляем в layout
        layout.addWidget(label)
        layout.addWidget(line_edit)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Установим базовый стиль для всего приложения
    app.setStyleSheet("""
        QWidget {
            background-color: #f5f5f5;
            font-family: 'Segoe UI', Arial;
        }
    """)
    
    window = InputWithLabel()
    window.show()
    
    sys.exit(app.exec())