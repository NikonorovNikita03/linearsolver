from ortools.linear_solver import pywraplp

def solve_assignment_problem(cost_matrix):
    """
    Решает задачу о назначениях с использованием OR-Tools.
    
    Параметры:
        cost_matrix (list[list[float]]): Матрица стоимостей, где cost_matrix[i][j] - стоимость назначения работника i на работу j.
    
    Возвращает:
        tuple: (общая стоимость, список назначений), где каждое назначение представлено как (работник, работа).
    """
    # Проверка входных данных
    if not cost_matrix:
        return (0, [])
    
    num_workers = len(cost_matrix)
    num_jobs = len(cost_matrix[0]) if num_workers > 0 else 0
    
    # Создаем решатель
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    # Создаем переменные: x[i][j] = 1 если работник i назначен на работу j
    x = {}
    for i in range(num_workers):
        for j in range(num_jobs):
            x[i, j] = solver.IntVar(0, 1, f'x[{i},{j}]')
    
    # Каждый работник назначается не более чем на одну работу
    for i in range(num_workers):
        solver.Add(solver.Sum([x[i, j] for j in range(num_jobs)]) <= 1)
    
    # Каждая работа выполняется ровно одним работником
    for j in range(num_jobs):
        solver.Add(solver.Sum([x[i, j] for i in range(num_workers)]) == 1)
    
    # Целевая функция: минимизация общей стоимости
    objective_terms = []
    for i in range(num_workers):
        for j in range(num_jobs):
            objective_terms.append(cost_matrix[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))
    
    # Решаем задачу
    status = solver.Solve()
    
    # Собираем результаты
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        total_cost = solver.Objective().Value()
        assignments = []
        for i in range(num_workers):
            for j in range(num_jobs):
                if x[i, j].solution_value() > 0.5:
                    assignments.append((i, j))
        return (total_cost, assignments)
    else:
        return (float('inf'), [])  # Если решение не найдено

# Пример использования
if __name__ == "__main__":
    # Матрица стоимостей: работники (строки) -> работы (столбцы)
    cost_matrix2 = [
        [90, 80, 75, 70],
        [35, 85, 55, 65],
        [125, 95, 90, 95],
        [45, 110, 95, 115]
    ]

    cost_matrix = [
        [3, 4, 9, 18, 9, 6],
        [16, 8, 12, 13, 20, 4],
        [8, 6, 13, 1, 6, 9],
        [16, 9, 6, 8, 1, 11],
        [8, 12, 17, 5, 3, 5],
        [2, 9, 1, 10, 5, 17]
    ]
    
    total_cost, assignments = solve_assignment_problem(cost_matrix)

    print(total_cost)
    print(assignments)

    # print(f"Общая стоимость: {total_cost}")
    # print("Назначения:")
    # for worker, job in assignments:
    #     print(f"  Работник {worker} назначен на работу {job}")