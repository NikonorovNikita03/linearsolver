btn_green = """
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
    },
    4 : {
        "id":4,
        "type": "Транспортная задача",
        "name": "ТЗ 2",
        "data": {
            "costs": [[595, 480, 455, 430], [435, 530, 480, 485], [545, 465, 525, 440]],
            "supply": [21, 33, 17],
            "demand": [15, 22, 12, 32],
            "size_x": 4,
            "size_y": 3
        }
    },
    5 : {
        "id": 5,
        "type": "ЗЛП",
        "name": "ЗЛП1",
        "data": {
            "problem_type": "max",
            "costs": [[0.02, 0.01], [0.03, 0.01], [0.03, 0.02]],
            "constraints": [60, 70, 100],
            "signs": ["<=", "<=", "<="],
            "function": [10, 4],
            "size_x": 2,
            "size_y": 3
        }
    },
    6 : {
        "id": 6,
        "type": "ЗЛП",
        "name": "ЗЛП2",
        "data": {
            "problem_type": "max",
            "costs": [[2, 1], [-4, 5], [-1, 2], [-1, 5]],
            "constraints": [20, 10, -2, 15],
            "signs": ["<=", "<=", ">=", "="],
            "function": [1, 2],
            "size_x": 2,
            "size_y": 4
        }
    },
    # 7 : {
    #     "id": 7,
    #     "type": "ЗЛП",
    #     "name": "ЗЛП3",
    #     "data": {
    #         "problem_type": "min",
    #         "costs": [[340, 80], [298, 545], [0.7, 5.9], [73.5, 59]],
    #         "constraints": [1000, 2000, 20, 200],
    #         "signs": ["<=", ">=", ">=", ">="],
    #         "function": [174.99, 84.99]
    #     }
    # }
    7 : {
        "id": 7,
        "type": "ЗЛП",
        "name": "ЗЛП3",
        "data": {
            "problem_type": "min",
            "costs": [[519, 490, 420], [6.5, 1.5, 2.5], [30.3, 26, 8.5], [58.2, 64, 83]],
            "constraints": [1500, 15, 80, 200],
            "signs": [">=", ">=", "<=", ">="],
            "function": [54.99, 149.97, 104.97]
        }
    }
}

items = {
    "marshmallow": {
        "Цена": 480,
        "Состав": {
            "Сахар-песок": 256.11,
            "Белок": 256.11,
            "Начинка фруктовая": 512.21,
            "Агар пищевой": 3.84,
            "Краситель пищевой": 1.27
        }
    }
}

items2 = {
    "Зефир Крем-броле Сокол": {
        "Вес": 340,
        "Цена": 174.99,
        "Пищевая ценность": {
            "Ккал": 298,
            "Белки": 0.7,
            "Углеводы": 73.5
        }
    },
    "Шоколад Alpen Gold белый Миндаль и кокос": {
        "Вес": 80,
        "Цена": 84.99,
        "Пищевая ценность": {
            "Ккал": 545,
            "Белки": 5.9,
            "Углеводы": 59
        }
    }
}

items3 = {
    "Конфеты Конфил Маэстро Виртуоз": {
        "Цена": 54.99,
        "Пищевая ценность": {
            "Ккал": 519,
            "Белки": 6.5,
            "Жиры": 30.3,
            "Углеводы": 58.2
        }
    },
    "Конфеты Конти Золотая Лилия": {
        "Цена": 149.97,
        "Пищевая ценность": {
            "Ккал": 490,
            "Белки": 1.5,
            "Жиры": 26,
            "Углеводы": 64
        }
    },
    "Конфета Азовская на сливках Азовская КФ": {
        "Цена": 104.97,
        "Пищевая ценность": {
            "Ккал": 420,
            "Белки": 2.5,
            "Жиры": 8.5,
            "Углеводы": 83
        }
    }
}