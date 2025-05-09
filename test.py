import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def solve_integer_programming(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None, integrality=None):
    """
    Решает задачу целочисленного линейного программирования:
    Минимизировать c^T * x
    при условиях:
    A_ub * x <= b_ub,
    A_eq * x == b_eq,
    bounds - границы переменных,
    integrality - указание целочисленности переменных.

    Параметры:
    c : 1-D array
        Коэффициенты целевой функции.
    A_ub : 2-D array, optional
        Матрица коэффициентов неравенств (<=).
    b_ub : 1-D array, optional
        Вектор правых частей неравенств.
    A_eq : 2-D array, optional
        Матрица коэффициентов равенств (==).
    b_eq : 1-D array, optional
        Вектор правых частей равенств.
    bounds : sequence, optional
        Границы переменных, например, [(0, None), (0, 5)].
    integrality : 1-D array, optional
        Указание целочисленности переменных (1 - целая, 0 - непрерывная).

    Возвращает:
    result : OptimizeResult
        Результат оптимизации, включая x - решение.
    """
    # Ограничения
    constraints = []
    if A_ub is not None and b_ub is not None:
        constraints.append(LinearConstraint(A_ub, -np.inf, b_ub))
    if A_eq is not None and b_eq is not None:
        constraints.append(LinearConstraint(A_eq, b_eq, b_eq))
    
    # Границы переменных (по умолчанию 0 <= x_i <= +inf)
    if bounds is None:
        bounds = Bounds(0, np.inf)
    else:
        bounds = Bounds(lb=[b[0] for b in bounds], ub=[b[1] for b in bounds])
    
    # Целочисленность переменных (по умолчанию все непрерывные)
    if integrality is None:
        integrality = 0
    
    # Решение задачи
    result = milp(
        c=c,
        constraints=constraints,
        bounds=bounds,
        integrality=integrality,
    )
    
    return result

# Пример использования
if __name__ == "__main__":
    # Целевая функция: минимизировать -x - y
    c = np.array([-1, -1])
    
    # Ограничения:
    # 2x + y <= 20
    # -4x + 5y <= 10
    # -x + 2y >= -2
    A_ub = np.array([[2, 1], [-4, 5], [1, -2]])
    b_ub = np.array([20, 10, 2])
    
    # Границы переменных: x >= 0, y >= 0
    bounds = [(0, None), (0, None)]
    
    # Целочисленность: обе переменные целые
    integrality = np.array([1, 1])
    
    # Решение задачи
    result = solve_integer_programming(
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        bounds=bounds,
        integrality=integrality,
    )
    
    print(result)
    # print("Статус решения:", result.message)
    # print("Оптимальное значение:", -result.fun)  # Так как мы минимизировали -x - y
    # print("Оптимальные переменные:", result.x)