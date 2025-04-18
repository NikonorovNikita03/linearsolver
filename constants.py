solve_btn = """
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                padding: 8px;
                margin-top: 18px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

text_input_btn = """
            QPushButton {
                background-color: #9C27B0; 
                color: white; 
                padding: 8px;
                margin-top: 18px;
            }
            QPushButton:hover {
                background-color: #6b2078;
            }
        """


total_cost_label = """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """


text_edit_placeholder = """Введите данные задачи здесь в формате:
Стоимости:
4 8 8
16 24 16
8 16 24
Запасы:
76 82 77
Потребности:
72 102 41
"""

title_label = """
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """

stringify = lambda i: f'{i}' if i % 1 else f'{i:.0f}'