import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QMessageBox, QFileDialog
from PySide6.QtGui import QIcon, QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример приложения с меню")
        self.setGeometry(100, 100, 800, 600)
        # self.setContentsMargins(0, 0, 0, 0)
        
        # Установка иконки приложения
        self.setWindowIcon(QIcon("images/calculator.svg"))
        
        self.create_menu_bar()

        # self.menuBar().setStyleSheet("""
        #     QMenuBar {
        #         margin-left: 0px;
        #         padding-left: 0px; /* Убираем отступ слева */
        #     }
        # """)
        
    def create_menu_bar(self):
        # Создаем менюбар
        menubar = self.menuBar()
        # menubar.setContentsMargins(0, 0, 0, 0)
        
        # 1. Меню "Файл" с подменю и действиями
        file_menu = menubar.addMenu("Файл")
        # file_menu.setContentsMargins(0, 0, 0, 0)
        
        # Подменю "Создать"
        new_menu = QMenu("Создать", self)
        
        new_file_action = QAction(QIcon("images/calculator.svg"), "Файл", self)
        new_file_action.setShortcut("Ctrl+N")
        new_file_action.triggered.connect(self.new_file)
        
        new_folder_action = QAction("Папку", self)
        new_folder_action.triggered.connect(self.new_folder)
        
        new_menu.addAction(new_file_action)
        new_menu.addAction(new_folder_action)
        
        # Другие действия меню "Файл"
        open_action = QAction(QIcon("images/calculator.svg"), "Открыть...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        
        save_action = QAction("Сохранить", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        
        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        
        # Добавляем все в меню "Файл"
        file_menu.addMenu(new_menu)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        # 2. Меню "Правка"
        edit_menu = menubar.addMenu("Правка")
        
        undo_action = QAction("Отменить", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo)
        
        redo_action = QAction("Повторить", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo)
        
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        
        # 3. Меню "Справка"
        help_menu = menubar.addMenu("Справка")
        
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        
        help_action = QAction("Помощь", self)
        help_action.setShortcut("F1")
        help_action.triggered.connect(self.show_help)
        
        help_menu.addAction(help_action)
        help_menu.addSeparator()
        help_menu.addAction(about_action)
    
    # Методы-обработчики действий
    def new_file(self):
        QMessageBox.information(self, "Создание файла", "Создан новый файл")
    
    def new_folder(self):
        QMessageBox.information(self, "Создание папки", "Создана новая папка")
    
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Все файлы (*);;Текстовые файлы (*.txt)")
        if file_name:
            QMessageBox.information(self, "Файл открыт", f"Выбран файл: {file_name}")
    
    def save_file(self):
        QMessageBox.information(self, "Сохранение", "Файл сохранен")
    
    def undo(self):
        QMessageBox.information(self, "Отмена", "Последнее действие отменено")
    
    def redo(self):
        QMessageBox.information(self, "Повтор", "Последнее действие повторено")
    
    def show_about(self):
        QMessageBox.about(self, "О программе", 
                         "Пример приложения с меню\nВерсия 1.0\n\nИконка: calculator.svg")
    
    def show_help(self):
        QMessageBox.information(self, "Помощь", 
                              "Это пример приложения с меню.\n\n"
                              "Используйте меню для выполнения различных действий.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())