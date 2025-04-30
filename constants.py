solve_btn = """
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                padding: 8px;
                margin-top: 18px;
                width: 60px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

multiproduct_btn_ss = """
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                padding: 8px;
                margin-top: 18px;
                width: 60px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

back_btn_ss = """
            QPushButton {
                background-color: #607D8B; 
                color: white; 
                padding: 8px;
                margin-top: 18px;
                width: 60px;
            }
            QPushButton:hover {
                background-color: #485e69;
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

examples_btn_ss = """
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                padding: 8px;
                margin-top: 18px;
                width: 60px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
# total_cost_label = """
#             QLabel {
#                 font-size: 16px;
#                 font-weight: bold;
#                 padding: 10px;
#                 background: #f5f5f5;
#                 border: 1px solid #ddd;
#                 border-radius: 5px;
#             }
#         """


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

colors = {
    "white": (255, 255, 255),
    "blue": (230, 240, 255),
    "pink": (255, 230, 230),
    "lime": (230, 255, 230),
    "green": (200, 255, 200),
    "black": (0, 0, 0)
}

solution_table_ss = """
QTableWidget {
                font-size: 12px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 5px;
            }
"""

solution_page_h_header_ss = """
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #e0e0e0;
            }
        """

solution_page_v_header_ss = """
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #e0e0e0;
            }
        """

total_cost_label_ss = """
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                background-color: #e8f5e9;
                border: 1px solid #c8e6c9;
                border-radius: 4px;
            }
        """

solution_copy_btn_ss = """
            QPushButton {
                background-color: #2196F3; 
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            """

export_csv_btn_ss = """
            QPushButton {
                background-color: #4CAF50; 
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
            """

examples = {
    0: {
        "id": 0,
        "type": "Транспортная задача",
        "name": "ТЗ 1",
        "data": {
            "costs": [[7, 8, 1, 2], [4, 5, 9, 8], [9, 2, 3, 6]],
            "supply": [160, 140, 170],
            "demand": [120, 50, 190, 110],
            "size_x": 4,
            "size_y": 3
        }
    },
    3 : {
        "id": 3,
        "type": "Многопродуктовая транспортная задача",
        "name": "МТЗ 1",
        "data": {
            "costs": [
                [[595, 780], [480, 665], [455, 640], [430, 815]],
                [[435, 735], [530, 735], [480, 680], [485, 585]],
                [[545, 715], [465, 755], [525, 815], [440, 795]]
            ],
            "supply": [[21, 21], [33, 42], [17, 57]],
            "demand": [[15, 20], [22, 26], [12, 22], [32, 42]],
            "size_x": 4,
            "size_y": 3
        }
    }
}