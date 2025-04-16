from scipy.optimize import linprog
import numpy as np

def solve_transportation_scipy(a, b, C):
    m, n = C.shape
    # Целевая функция (минимизация суммарной стоимости)
    c = C.flatten()
    # Ограничения: сумма по строкам = a, сумма по столбцам = b
    A_eq = []
    # Ограничения по запасам (каждая строка)
    for i in range(m):
        row = np.zeros((m, n))
        row[i, :] = 1
        A_eq.append(row.flatten())
    # Ограничения по потребностям (каждый столбец)
    for j in range(n):
        col = np.zeros((m, n))
        col[:, j] = 1
        A_eq.append(col.flatten())
    A_eq = np.array(A_eq)
    b_eq = np.concatenate([a, b])
    
    # Решение задачи линейного программирования
    res = linprog(c, A_eq=A_eq[:-1], b_eq=b_eq[:-1], bounds=(0, None))
    X = res.x.reshape((m, n))
    total_cost = np.sum(X * C)
    return X, total_cost

a = np.array([7, 9, 18])
b = np.array([5, 8, 7, 14])
c = np.array([
    [19, 30, 50, 10],
    [70, 30, 40, 60],
    [40, 8, 70, 20]
])

X, cost = solve_transportation_scipy(a, b, c)

print("Оптимальный план (scipy):")
print(X)
print(f"Общая стоимость: {cost}")