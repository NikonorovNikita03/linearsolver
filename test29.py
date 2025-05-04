import numpy as np

class AssignmentProblemSolver:
    def __init__(self, cost_matrix):
        """
        Инициализация решателя задачи о назначениях.
        
        :param cost_matrix: Матрица затрат (N x N), где элемент [i][j] - стоимость назначения работника i на работу j
        """
        self.cost_matrix = np.array(cost_matrix, dtype=float)
        self.n = len(cost_matrix)
        
    def solve(self):
        """
        Решает задачу о назначениях с минимальной стоимостью.
        
        :return: Кортеж (total_cost, assignments), где:
                 total_cost - общая минимальная стоимость,
                 assignments - список кортежей (работник, работа)
        """
        # Шаг 1: Редукция строк
        reduced_matrix = self.cost_matrix.copy()
        reduced_matrix -= reduced_matrix.min(axis=1)[:, np.newaxis]
        
        # Шаг 2: Редукция столбцов
        reduced_matrix -= reduced_matrix.min(axis=0)
        
        # Шаг 3: Поиск оптимального назначения
        while True:
            # Находим минимальное количество линий, покрывающих все нули
            marked_rows, marked_cols = self._draw_lines(reduced_matrix)
            
            # Если количество линий равно размеру матрицы, найдено оптимальное решение
            if len(marked_rows) + len(marked_cols) == self.n:
                break
                
            # Шаг 4: Создание дополнительных нулей
            reduced_matrix = self._create_additional_zeros(reduced_matrix, marked_rows, marked_cols)
        
        # Находим оптимальные назначения
        assignments = self._find_assignments(reduced_matrix)
        total_cost = sum(self.cost_matrix[i, j] for i, j in assignments)
        
        return total_cost, assignments
    
    def _draw_lines(self, matrix):
        """
        Находит минимальное количество линий (горизонтальных и вертикальных),
        покрывающих все нули в матрице.
        """
        marked_rows = []
        marked_cols = []
        
        # Копируем матрицу для работы
        temp_matrix = matrix.copy()
        
        # Пока есть нули в матрице
        while True:
            zero_positions = np.where(temp_matrix == 0)
            if len(zero_positions[0]) == 0:
                break
                
            # Находим строку или столбец с наибольшим количеством нулей
            row_counts = np.zeros(self.n)
            col_counts = np.zeros(self.n)
            
            for i, j in zip(*zero_positions):
                row_counts[i] += 1
                col_counts[j] += 1
                
            max_row = np.argmax(row_counts)
            max_col = np.argmax(col_counts)
            
            if row_counts[max_row] >= col_counts[max_col]:
                marked_rows.append(max_row)
                temp_matrix[max_row, :] = np.inf
            else:
                marked_cols.append(max_col)
                temp_matrix[:, max_col] = np.inf
                
        return marked_rows, marked_cols
    
    def _create_additional_zeros(self, matrix, marked_rows, marked_cols):
        """
        Создает дополнительные нули в матрице путем вычитания минимального
        непокрытого элемента из всех непокрытых элементов и добавления его
        к элементам, покрытым двумя линиями.
        """
        # Находим минимальный непокрытый элемент
        uncovered_rows = [i for i in range(self.n) if i not in marked_rows]
        uncovered_cols = [j for j in range(self.n) if j not in marked_cols]
        
        min_val = np.inf
        for i in uncovered_rows:
            for j in uncovered_cols:
                if matrix[i, j] < min_val:
                    min_val = matrix[i, j]
        
        # Вычитаем минимальное значение из непокрытых элементов
        for i in uncovered_rows:
            for j in uncovered_cols:
                matrix[i, j] -= min_val
                
        # Добавляем минимальное значение к элементам, покрытым двумя линиями
        for i in marked_rows:
            for j in marked_cols:
                matrix[i, j] += min_val
                
        return matrix
    
    def _find_assignments(self, matrix):
        """
        Находит оптимальные назначения по редуцированной матрице.
        """
        assignments = []
        assigned_rows = set()
        assigned_cols = set()
        
        # Назначаем сначала уникальные нули
        for _ in range(self.n):
            for i in range(self.n):
                if i in assigned_rows:
                    continue
                zero_cols = [j for j in range(self.n) if matrix[i, j] == 0 and j not in assigned_cols]
                if len(zero_cols) == 1:
                    j = zero_cols[0]
                    assignments.append((i, j))
                    assigned_rows.add(i)
                    assigned_cols.add(j)
                    break
        
        # Назначаем оставшиеся нули
        for i in range(self.n):
            if i in assigned_rows:
                continue
            for j in range(self.n):
                if j not in assigned_cols and matrix[i, j] == 0:
                    assignments.append((i, j))
                    assigned_rows.add(i)
                    assigned_cols.add(j)
                    break
                    
        return assignments


# Пример использования
if __name__ == "__main__":
    # Матрица затрат (работники x работы)
    cost_matrix = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4]
    ]
    
    solver = AssignmentProblemSolver(cost_matrix)
    total_cost, assignments = solver.solve()
    
    print(f"Общая минимальная стоимость: {total_cost}")
    print("Оптимальные назначения:")
    for worker, job in assignments:
        print(f"Работник {worker + 1} -> Работа {job + 1} (стоимость: {cost_matrix[worker][job]})")