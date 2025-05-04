import numpy as np
from scipy.optimize import linear_sum_assignment

def solve_assignment(cost_matrix):
    """
    Решает задачу о назначениях с минимальной стоимостью используя алгоритм Джона-Кёрнси (венгерский алгоритм)
    
    :param cost_matrix: Матрица затрат (N x M), где элемент [i][j] - стоимость назначения работника i на работу j
    :return: Кортеж (total_cost, assignments), где:
             total_cost - общая минимальная стоимость,
             assignments - список кортежей (работник, работа)
    """
    # Преобразуем в numpy array для надежности
    cost_matrix = np.array(cost_matrix)
    
    # Находим оптимальные назначения (индексы строк и столбцов)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    
    # Собираем назначения в список кортежей
    assignments = list(zip(row_ind, col_ind))
    
    # Вычисляем общую стоимость
    total_cost = cost_matrix[row_ind, col_ind].sum()
    
    return total_cost, assignments

# Пример использования
if __name__ == "__main__":
    # Матрица затрат (работники x работы)
    # cost_matrix = [
    #     [9, 2, 7, 8],
    #     [6, 4, 3, 7],
    #     [5, 8, 1, 8],
    #     [7, 6, 9, 4]
    # ]
    cost_matrix2 = [
        [3, 4, 9, 18, 9, 6],
        [16, 8, 12, 13, 20, 4],
        [8, 6, 13, 1, 6, 9],
        [16, 9, 6, 8, 1, 11],
        [8, 12, 17, 5, 3, 5],
        [2, 9, 1, 10, 5, 17]
    ]
    cost_matrix = [
        [75, 30, 10, 25],
        [20, 35, 40, 50],
        [15, 55, 70, 65],
        [25, 30, 20, 100],
        [30, 40, 55, 60],
        [70, 80, 25, 30]
    ]
    
    
    total_cost, assignments = solve_assignment(cost_matrix)
    
    print(f"Общая минимальная стоимость: {total_cost}")
    print("Оптимальные назначения:")
    print([(int(x), int(y)) for (x, y) in assignments])
    # for worker, job in assignments:
    #     print(f"Работник {worker + 1} -> Работа {job + 1} (стоимость: {cost_matrix[worker][job]})")