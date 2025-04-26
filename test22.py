import numpy as np
from scipy.optimize import linprog

# Данные задачи
# costs = np.array([
#     [[595, 780], [480, 665], [455, 640], [430, 815], [0, 0]],
#     [[435, 735], [530, 735], [480, 680], [485, 585], [0, 0]],
#     [[545, 715], [465, 755], [525, 815], [440, 795], [0, 0]],
#     [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
# ])

# supply = np.array([[21, 21], [33, 42], [17, 57], [10, 0]])
# demand = np.array([[15, 20], [22, 26], [12, 22], [32, 42], [0, 10]])

# costs = np.array([
#     [[595, 780], [480, 665], [455, 640], [430, 815]],
#     [[435, 735], [530, 735], [480, 680], [485, 585]],
#     [[545, 715], [465, 755], [525, 815], [440, 795]]
# ])

# supply = np.array([[21, 21], [33, 42], [17, 57]])
# demand = np.array([[15, 20], [22, 26], [12, 22], [32, 42]])

costs = [
    [[595, 780], [480, 665], [455, 640], [430, 815]],
    [[435, 735], [530, 735], [480, 680], [485, 585]],
    [[545, 715], [465, 755], [525, 815], [440, 795]]
]

supply = [[21, 21], [33, 42], [17, 57]]
demand = [[15, 20], [22, 26], [12, 22], [32, 42]]

# # Параметры задачи
n_sources = len(supply)  # количество поставщиков (включая фиктивного)
n_destinations = len(demand)  # количество потребителей (включая фиктивного)
n_products = len(supply[0])  # количество продуктов

for n in range(n_products):
    print(supply)
    supply_n = sum([supply[x][n] for x in range(n_sources)])
    demand_n = sum([demand[x][n] for x in range(n_destinations)])

    if supply_n > demand_n:
        for i in range(len(costs)):
            #costs[i] = np.append(costs[i], np.zeros(n_products))
            costs[i].append([0 for i in range(n_products)])
        new_demand = [0 for i in range(n_products)]
        new_demand[n] = supply_n - demand_n
        #demand = np.vstack((demand, new_demand))
        demand.append(new_demand)
        n_destinations += 1

    if supply_n < demand_n:
        #costs = np.append(costs, np.zeros((n_destinations, n_products)))
        costs.append([[0 for i in range(n_products)] for j in range(n_destinations)])
        new_supply = np.zeros(n_products)
        new_supply[n] = demand_n - supply_n
        #supply = np.vstack((supply, new_supply))
        supply.append(new_supply)
        n_sources += 1

# for n in range(n_products):
#     supply_n = np.sum(supply[:, n])  # More efficient way to sum a column
#     demand_n = np.sum(demand[:, n])  # More efficient way to sum a column

#     if supply_n > demand_n:
#         new_column = np.zeros((costs.shape[0], 1)) 
#         for i in range(len(costs)):
#             costs[i] = np.c_[costs[i], np.full(costs[i].shape[0], np.zeros(n_products))]
#             #costs[i] = np.append(costs[i], [np.zeros(n_products)], axis=0)
        
#         new_demand = np.zeros(n_products)
#         new_demand[n] = supply_n - demand_n
#         demand = np.vstack((demand, new_demand.reshape(1, -1)))  # Ensure 2D shape
#         n_destinations += 1

#     elif supply_n < demand_n:
#         # Add dummy source row for each destination
#         new_row = np.zeros((n_destinations, n_products))
#         #costs = np.vstack((costs, [new_row]))
#         costs = np.append(costs, [new_row], axis=0)
        
#         new_supply = np.zeros(n_products)
#         new_supply[n] = demand_n - supply_n
#         supply = np.vstack((supply, new_supply.reshape(1, -1)))  # Ensure 2D shape
#         n_sources += 1

# Преобразуем задачу в форму линейного программирования
# Целевая функция: минимизация суммарных затрат
# Создаем вектор коэффициентов целевой функции (c)
costs = np.array(costs)
supply = np.array(supply)
demand = np.array(demand)

c_list = []
for i in range(n_sources):
    for j in range(n_destinations):
        for p in range(n_products):
            # print(c_list)
            # print(costs)
            print(i, j, p)
            c_list.append(costs[i, j, p] if i < 3 else 0)  # фиктивный поставщик имеет нулевую стоимость

c = np.array(c_list)

# Ограничения:
# 1. Поставки (для каждого поставщика и каждого продукта)
# 2. Спрос (для каждого потребителя и каждого продукта)

# Матрица ограничений A_eq
num_vars = n_sources * n_destinations * n_products
A_eq = []
b_eq = []

# Ограничения по поставкам (supply)
for i in range(n_sources):
    for p in range(n_products):
        row = np.zeros(num_vars)
        for j in range(n_destinations):
            idx = (i * n_destinations * n_products) + (j * n_products) + p
            row[idx] = 1
        A_eq.append(row)
        b_eq.append(supply[i, p])

# Ограничения по спросу (demand)
for j in range(n_destinations):
    for p in range(n_products):
        row = np.zeros(num_vars)
        for i in range(n_sources):
            idx = (i * n_destinations * n_products) + (j * n_products) + p
            row[idx] = 1
        A_eq.append(row)
        b_eq.append(demand[j, p])

A_eq = np.array(A_eq)
b_eq = np.array(b_eq)

# Границы переменных (x >= 0)
bounds = [(0, None) for _ in range(num_vars)]

# Решение задачи линейного программирования
result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

# Проверка успешности решения
if not result.success:
    raise ValueError("Решение не найдено:", result.message)

# Извлечение решения
solution = result.x.reshape((n_sources, n_destinations, n_products))

# Вывод результатов
print("Оптимальное решение:")
total_cost = 0
for i in range(n_sources):
    for j in range(n_destinations):
        for p in range(n_products):
            if solution[i, j, p] > 1e-6:  # игнорируем очень малые значения
                cost = costs[i, j, p] if i < 3 else 0
                print(f"Поставщик {i+1} -> Потребитель {j+1}, Продукт {p+1}: {solution[i, j, p]:.2f} (стоимость: {cost})")
                total_cost += solution[i, j, p] * cost

print(f"\nОбщая стоимость перевозок: {total_cost:.2f}")

# Проверка ограничений
print("\nПроверка ограничений:")
# Проверка поставок
for i in range(n_sources):
    for p in range(n_products):
        total_supply = sum(solution[i, j, p] for j in range(n_destinations))
        print(f"Поставщик {i+1}, Продукт {p+1}: требуется {supply[i, p]}, выполнено {total_supply:.2f}")

# Проверка спроса
for j in range(n_destinations):
    for p in range(n_products):
        total_demand = sum(solution[i, j, p] for i in range(n_sources))
        print(f"Потребитель {j+1}, Продукт {p+1}: требуется {demand[j, p]}, выполнено {total_demand:.2f}")