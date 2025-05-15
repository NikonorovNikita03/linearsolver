import sys
import os
from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush

def get_settings():
    with open("settings.txt") as f:
        settings = f.read()
        
    try:
        lines = settings.strip().split('\n')
        result = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                result[key.strip()] = int(value.strip())
        return result
    except:
        return {
            "size_x": 4,
            "size_y": 4,
            "width": 1366,
            "height": 768
        }
    
def combine_arrays_pure(arr1, arr2):
    rows1, cols1 = len(arr1), len(arr1[0]) if arr1 else 0
    rows2, cols2 = len(arr2), len(arr2[0]) if arr2 else 0
    
    if rows1 > rows2 or cols1 > cols2:
        return arr1
    
    result = [row.copy() for row in arr2]
    
    for i in range(rows1):
        for j in range(cols1):
            result[i][j] = arr1[i][j]
    
    return result

def combine_arrays_1d_pure(arr1, arr2):
    len1, len2 = len(arr1), len(arr2)
    
    if len1 >= len2:
        return arr1
    
    result = arr1.copy() + arr2[len1:]
    
    return result

def str_to_number(s):
    try:
        f = float(s)
        return int(f) if f.is_integer() else f
    except:
        return 0
    
def q_push_button(name, style, function = None, cursor=True):
    btn = QPushButton(name)
    btn.setStyleSheet(style)
    if function:
        btn.clicked.connect(function)
    if cursor:
        btn.setCursor(Qt.PointingHandCursor)
    return btn

def input_field(label_text, placeholder=None, text=None, max_length=None, spacing=0):
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
    
    line_edit = QLineEdit()

    if placeholder is not None:
        line_edit.setPlaceholderText(placeholder)
    
    if text is not None:
        line_edit.setText(text)

    if max_length is not None:
        print(max_length)
        line_edit.setMaxLength(max_length)
    
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
    
    return container

colors = {
    "white": (255, 255, 255),
    "blue": (230, 240, 255),
    "pink": (255, 230, 230),
    "lime": (230, 255, 230),
    "green": (200, 255, 200),
    "black": (0, 0, 0)
}
brushes = {}
for color in colors:
    brushes[color] = QBrush(QColor(*color[1]))

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)