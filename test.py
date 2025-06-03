import json

def array_to_json(arr):
    """
    Преобразует одномерный или двумерный массив (список) в JSON строку.
    
    Параметры:
    arr (list): одномерный или двумерный список
    
    Возвращает:
    str: JSON строка, представляющая массив
    """
    if not isinstance(arr, list):
        raise ValueError("Входные данные должны быть списком (одномерным или двумерным)")
    
    # Проверяем, является ли массив двумерным
    is_2d = all(isinstance(row, list) for row in arr) if arr else False
    
    if is_2d:
        # Для двумерного массива создаем объект с описанием структуры
        result = {
            "type": "2d_array",
            "data": arr
        }
    else:
        # Для одномерного массива
        result = {
            "type": "1d_array",
            "data": arr
        }
    
    return json.dumps(arr, ensure_ascii=False, indent=3)

# Примеры использования:
if __name__ == "__main__":
    # Одномерный массив
    arr2d = [
        [45, 50, 48, 52],
        [24, 15, 18, 17],
        [25, 30, 28, 27],
        [5, 4, 4.5, 4.2],
        [2, 1.8, 1.5, 2.1],
        [0.3, 0, 0, 0],
        [0, 0.2, 0, 0],
        [0, 0, 0.4, 0],
        [0, 0, 0, 0.25]
    ]
    # print(array_to_json(arr2d))
    json_var = json.dumps(arr2d)
    print(json_var)
    # print(json.loads(json_var))