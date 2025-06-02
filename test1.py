import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QLabel, QListWidget, 
                              QListWidgetItem, QSizePolicy)
from PySide6.QtCore import Qt
import random


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Трехуровневое меню")
        self.setFixedSize(1366, 768)  # Фиксированное разрешение 1366x768
        
        # Центральный виджет и основной макет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # Создаем разделы для каждого уровня меню
        self.create_level1()
        self.create_level2()
        self.create_level3()
        
        # Изначально скрываем 2 и 3 уровни
        self.level2_widget.hide()
        self.level3_widget.hide()
    
    def create_level1(self):
        """Первый уровень - выбор категории"""
        self.level1_widget = QWidget()
        level1_layout = QVBoxLayout(self.level1_widget)
        level1_layout.setContentsMargins(0, 0, 0, 0)
        
        # Заголовок
        label = QLabel("1. Выберите категорию:")
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        level1_layout.addWidget(label, alignment=Qt.AlignLeft)
        
        # Горизонтальное расположение кнопок
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        
        categories = ["Программирование", "Математика", "Физика", "Литература"]
        self.category_buttons = []
        
        for category in categories:
            btn = QPushButton(category)
            btn.setFixedSize(250, 50)  # Фиксированный размер кнопок
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    font-weight: bold;
                    padding: 5px;
                    border: 2px solid #2c3e50;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #3498db;
                    color: white;
                }
            """)
            btn.clicked.connect(lambda _, cat=category: self.show_level2(cat))
            buttons_layout.addWidget(btn)
            self.category_buttons.append(btn)
        
        level1_layout.addLayout(buttons_layout)
        self.main_layout.addWidget(self.level1_widget, alignment=Qt.AlignTop)
    
    def create_level2(self):
        """Второй уровень - выбор действия"""
        self.level2_widget = QWidget()
        level2_layout = QVBoxLayout(self.level2_widget)
        level2_layout.setContentsMargins(0, 0, 0, 0)
        
        # Заголовок
        self.level2_label = QLabel()
        self.level2_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.level2_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        level2_layout.addWidget(self.level2_label, alignment=Qt.AlignLeft)
        
        # Горизонтальное расположение кнопок
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        
        options = ["Новая задача", "Выбрать задачу", "Случайная задача"]
        self.action_buttons = []
        
        for option in options:
            btn = QPushButton(option)
            btn.setFixedSize(250, 50)  # Фиксированный размер кнопок
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    font-weight: bold;
                    padding: 5px;
                    border: 2px solid #2c3e50;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #3498db;
                    color: white;
                }
            """)
            btn.clicked.connect(lambda _, opt=option: self.show_level3(opt))
            buttons_layout.addWidget(btn)
            self.action_buttons.append(btn)
        
        level2_layout.addLayout(buttons_layout)
        self.main_layout.addWidget(self.level2_widget, alignment=Qt.AlignTop)
    
    def create_level3(self):
        """Третий уровень - отображение задач"""
        self.level3_widget = QWidget()
        level3_layout = QVBoxLayout(self.level3_widget)
        level3_layout.setContentsMargins(0, 0, 0, 0)
        
        # Заголовок
        self.level3_label = QLabel()
        self.level3_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.level3_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        level3_layout.addWidget(self.level3_label, alignment=Qt.AlignLeft)
        
        # Область задач с фиксированной высотой
        self.task_list = QListWidget()
        self.task_list.setFixedHeight(400)  # Фиксированная высота списка задач
        self.task_list.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                border: 2px solid #2c3e50;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        level3_layout.addWidget(self.task_list)
        
        self.main_layout.addWidget(self.level3_widget, alignment=Qt.AlignTop)
        self.main_layout.addStretch()  # Добавляем растягивающееся пространство
    
    def show_level2(self, category):
        """Показываем второй уровень"""
        self.current_category = category
        self.level2_label.setText(f"2. Действие для категории: {category}")
        self.level2_widget.show()
        self.level3_widget.hide()
    
    def show_level3(self, action):
        """Показываем третий уровень"""
        self.level3_label.setText(f"3. Результат: {self.current_category} - {action}")
        
        self.task_list.clear()
        
        if action == "Новая задача":
            self.task_list.addItem("Введите новую задачу...")
        elif action == "Случайная задача":
            tasks = self.generate_tasks(self.current_category)
            self.task_list.addItem(random.choice(tasks))
        elif action == "Выбрать задачу":
            tasks = self.generate_tasks(self.current_category)
            self.task_list.addItems(tasks)
        
        self.level3_widget.show()
    
    def generate_tasks(self, category):
        """Генерируем примеры задач для разных категорий"""
        tasks = {
            "Программирование": [
                "Написать функцию сортировки списка",
                "Создать GUI приложение на PySide6",
                "Реализовать алгоритм поиска пути",
                "Оптимизировать SQL-запрос",
                "Разработать REST API сервис",
                "Написать unit-тесты для модуля",
                "Рефакторинг legacy кода",
                "Реализовать кэширование данных"
            ],
            "Математика": [
                "Решить квадратное уравнение x² - 5x + 6 = 0",
                "Найти производную функции f(x) = 3x³ - 2x² + x - 5",
                "Вычислить интеграл ∫(2x + 3)dx от 0 до 1",
                "Доказать теорему Пифагора",
                "Решить систему линейных уравнений",
                "Найти обратную матрицу",
                "Построить график функции",
                "Вычислить предел последовательности"
            ],
            "Физика": [
                "Рассчитать скорость свободного падения на Марсе",
                "Решить задачу на закон Ома для цепи переменного тока",
                "Рассчитать энергию фотона с длиной волны 500 нм",
                "Определить центр масс системы из 3 тел",
                "Решить задачу на термодинамику идеального газа",
                "Рассчитать траекторию движения снаряда",
                "Определить КПД тепловой машины",
                "Решить задачу на закон сохранения импульса"
            ],
            "Литература": [
                "Проанализировать образ Печорина в 'Герое нашего времени'",
                "Сравнить 'Войну и мир' Толстого и 'Тихий Дон' Шолохова",
                "Написать эссе на тему 'Образ города в русской литературе'",
                "Разобрать стихотворение 'Я помню чудное мгновенье'",
                "Анализ сюжета 'Преступления и наказания'",
                "Характеристика главного героя 'Отцы и дети'",
                "Сравнительный анализ поэзии Пушкина и Лермонтова",
                "Тема маленького человека в произведениях Гоголя"
            ]
        }
        return tasks.get(category, ["Нет доступных задач для этой категории"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())