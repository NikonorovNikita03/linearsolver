from ortools.linear_solver import pywraplp

def balance_problem(costs, supply, demand):
    """Балансирует транспортную задачу, добавляя фиктивных поставщиков или потребителей."""
    total_supply = sum(supply)
    total_demand = sum(demand)
    
    if total_supply == total_demand:
        return costs, supply, demand
    
    if total_supply > total_demand:
        # Добавляем фиктивного потребителя
        num_suppliers = len(supply)
        for i in range(num_suppliers):
            costs[i].append(0)  # Нулевая стоимость для фиктивного потребителя
        demand.append(total_supply - total_demand)
    else:
        # Добавляем фиктивного поставщика
        num_demanders = len(demand)
        new_row = [0] * num_demanders  # Нулевая стоимость от фиктивного поставщика
        costs.append(new_row)
        supply.append(total_demand - total_supply)
    
    return costs, supply, demand

def solve_single_product_transportation(costs, supply, demand):
    """Решает однопродуктовую транспортную задачу с балансировкой."""
    # Сначала балансируем задачу
    costs, supply, demand = balance_problem(costs, supply, demand)
    
    num_suppliers = len(supply)
    num_demanders = len(demand)
    
    # Создаем решатель
    solver = pywraplp.Solver.CreateSolver('GLOP')
    
    # Создаем переменные
    x = {}
    for i in range(num_suppliers):
        for j in range(num_demanders):
            x[i, j] = solver.NumVar(0, solver.infinity(), f'x_{i}_{j}')
    
    # Ограничения по предложению
    for i in range(num_suppliers):
        solver.Add(sum(x[i, j] for j in range(num_demanders)) <= supply[i])
    
    # Ограничения по спросу
    for j in range(num_demanders):
        solver.Add(sum(x[i, j] for i in range(num_suppliers)) >= demand[j])
    
    # Целевая функция - минимизация затрат
    objective = solver.Objective()
    for i in range(num_suppliers):
        for j in range(num_demanders):
            objective.SetCoefficient(x[i, j], costs[i][j])
    objective.SetMinimization()
    
    # Решаем задачу
    status = solver.Solve()
    
    # Собираем результаты
    if status == pywraplp.Solver.OPTIMAL:
        solution = [[0] * num_demanders for _ in range(num_suppliers)]
        total_cost = 0
        for i in range(num_suppliers):
            for j in range(num_demanders):
                solution[i][j] = x[i, j].solution_value()
                total_cost += solution[i][j] * costs[i][j]
            
        return solution, total_cost
    else:
        return None, None

# Исходные данные
costs = [
    [[595, 780], [480, 665], [455, 640], [430, 815]],
    [[435, 735], [530, 735], [480, 680], [485, 585]],
    [[545, 715], [465, 755], [525, 815], [440, 795]]
]

supply = [[21, 21], [33, 42], [17, 57]]
demand = [[15, 20], [22, 26], [12, 22], [32, 42]]

# Разделяем данные на два продукта
# Продукт 1
costs_product1 = [[row[0] for row in col] for col in costs]
supply_product1 = [s[0] for s in supply]
demand_product1 = [d[0] for d in demand]

# Продукт 2
costs_product2 = [[row[1] for row in col] for col in costs]
supply_product2 = [s[1] for s in supply]
demand_product2 = [d[1] for d in demand]

# Проверяем баланс для каждого продукта
print("Баланс для продукта 1:")
print(f"Суммарное предложение: {sum(supply_product1)}")
print(f"Суммарный спрос: {sum(demand_product1)}")
print("Сбалансировано" if sum(supply_product1) == sum(demand_product1) else "Не сбалансировано")

print("\nБаланс для продукта 2:")
print(f"Суммарное предложение: {sum(supply_product2)}")
print(f"Суммарный спрос: {sum(demand_product2)}")
print("Сбалансировано" if sum(supply_product2) == sum(demand_product2) else "Не сбалансировано")

# Решаем для продукта 1
sol1, cost1 = solve_single_product_transportation(costs_product1, supply_product1, demand_product1)

# Решаем для продукта 2
sol2, cost2 = solve_single_product_transportation(costs_product2, supply_product2, demand_product2)

# Выводим результаты
print("\nРешение для продукта 1:")
for row in sol1:
    print([round(x, 2) for x in row])
print(f"Общая стоимость продукта 1: {cost1}\n")

print("Решение для продукта 2:")
for row in sol2:
    print([round(x, 2) for x in row])
print(f"Общая стоимость продукта 2: {cost2}\n")

print(f"Суммарная общая стоимость: {cost1 + cost2}")