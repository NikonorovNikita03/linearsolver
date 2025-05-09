from ortools.linear_solver import pywraplp

def solve_transportation_problem(supply, demand, costs):
    """
    Решает транспортную задачу минимизации стоимости перевозок.
    
    Параметры:
        supply: список запасов у поставщиков
        demand: список спросов у потребителей
        costs: матрица стоимостей перевозок (supply x demand)
    
    Возвращает:
        Словарь с результатами: общая стоимость, матрица перевозок
    """
    # Создаем решатель
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        raise Exception('Не удалось создать решатель')
    
    num_suppliers = len(supply)
    num_consumers = len(demand)
    
    # Создаем переменные: x[i][j] - количество перевозимого от i к j
    x = []
    for i in range(num_suppliers):
        x.append([])
        for j in range(num_consumers):
            x[i].append(solver.NumVar(0, solver.infinity(), f'x_{i}_{j}'))
    
    # Ограничения по запасам у поставщиков
    for i in range(num_suppliers):
        solver.Add(sum(x[i][j] for j in range(num_consumers)) <= supply[i])
    
    # Ограничения по спросу у потребителей
    for j in range(num_consumers):
        solver.Add(sum(x[i][j] for i in range(num_suppliers)) >= demand[j])
    
    # Целевая функция: минимизация общей стоимости
    objective = solver.Objective()
    for i in range(num_suppliers):
        for j in range(num_consumers):
            objective.SetCoefficient(x[i][j], costs[i][j])
    objective.SetMinimization()
    
    # Решаем задачу
    status = solver.Solve()
    
    # Формируем результаты
    if status == pywraplp.Solver.OPTIMAL:
        transport_matrix = []
        for i in range(num_suppliers):
            transport_matrix.append([x[i][j].solution_value() for j in range(num_consumers)])
        
        return {
            'total_cost': objective.Value(),
            'transport_matrix': transport_matrix,
            'status': 'OPTIMAL'
        }
    else:
        return {
            'total_cost': None,
            'transport_matrix': None,
            'status': 'NOT_OPTIMAL'
        }

# Пример использования
if __name__ == '__main__':
    # Данные примера
    supply = [20, 30]  # Запасы поставщиков
    demand = [10, 28, 12]  # Спрос потребителей
    costs = [
        [3, 5, 7],  # Стоимости перевозок от поставщика 0
        [5, 4, 2]   # Стоимости перевозок от поставщика 1
    ]
    data = {
        "costs": [[7, 8, 1, 2], [4, 5, 9, 8], [9, 2, 3, 6]],
        "supply": [160, 140, 170],
        "demand": [120, 50, 190, 110]
    }
    
    # Решаем задачу
    # result = solve_transportation_problem(supply, demand, costs)
    result = solve_transportation_problem(data["supply"], data['demand'], data['costs'])
    print(result)
    
    # Выводим результаты
    print(f"Общая стоимость: {result['total_cost']}")
    print("Матрица перевозок:")
    for row in result['transport_matrix']:
        print(row)