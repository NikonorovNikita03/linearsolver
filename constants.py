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

title_label = """
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """

stringify = lambda i: f'{i}' if i % 1 else f'{i:.0f}'

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
    1 : {
        "id": 1,
        "type": "Задача о назначениях",
        "name": "ЗоН 1",
        "data": {
            "costs": [
                [3, 4, 9, 18, 9, 6],
                [16, 8, 12, 13, 20, 4],
                [8, 6, 13, 1, 6, 9],
                [16, 9, 6, 8, 1, 11],
                [8, 12, 17, 5, 3, 5],
                [2, 9, 1, 10, 5, 17]
            ],
            "size_x": 6,
            "size_y": 6
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