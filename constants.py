solve_btn = """
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                padding: 8px;
                margin-top: 18px;
                width: 50px;
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
                width: 50px;
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
    "green": (200, 255, 200)
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