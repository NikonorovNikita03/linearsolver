import re
from collections import defaultdict, Counter

class TransportProblemParser:
    def __init__(self, text):
        self.text = text.strip()
        self.lines = [line.strip() for line in self.text.split('\n') if line.strip()]

    def parse_named_problem(self):
        suppliers = {}
        consumers = {}
        cost_matrix = defaultdict(dict)
        
        # Парсинг поставщиков
        supplier_section = False
        consumer_section = False
        cost_matrix_section = False
        
        for line in self.lines:
            if "поставщик" in line.lower() or "запасы" in line.lower():
                supplier_section = True
                consumer_section = False
                cost_matrix_section = False
                continue
            elif "потребител" in line.lower() or "потребности" in line.lower():
                supplier_section = False
                consumer_section = True
                cost_matrix_section = False
                continue
            elif "стоимости" in line.lower() or "перевозок" in line.lower() or "матриц" in line.lower():
                supplier_section = False
                consumer_section = False
                cost_matrix_section = True
                continue
                
            if supplier_section:
                # Парсим строки типа: A = 120 т
                match = re.match(r'([A-Za-zА-Яа-я]+)\s*=\s*(\d+)', line)
                if match:
                    supplier, amount = match.groups()
                    suppliers[supplier] = int(amount)
                    
            elif consumer_section:
                # Парсим строки типа: 1 = 70 т
                match = re.match(r'([A-Za-zА-Яа-я0-9]+)\s*=\s*(\d+)', line)
                if match:
                    consumer, amount = match.groups()
                    consumers[consumer] = int(amount)
                    
            elif cost_matrix_section:
                # Парсим матрицу стоимостей
                if re.match(r'^\s*[A-Za-zА-Яа-я]+\s+[\d\s]+$', line):
                    parts = re.split(r'\s{2,}', line.strip())
                    supplier = parts[0]
                    costs = [int(num) for num in re.findall(r'\d+', ' '.join(parts[1:]))]
                    
                    if len(costs) == len(consumers):
                        for i, cost in enumerate(costs):
                            consumer = list(consumers.keys())[i]
                            cost_matrix[supplier][consumer] = cost
        
        if suppliers and consumers and cost_matrix:
            # Преобразуем в числовой формат для совместимости
            m = len(suppliers)
            n = len(consumers)
            supply = list(suppliers.values())
            demand = list(consumers.values())
            
            # Создаем матрицу стоимостей в правильном порядке
            cost_matrix_flat = []
            for supplier in suppliers:
                for consumer in consumers:
                    cost_matrix_flat.append(cost_matrix[supplier][consumer])
            
            return [(m, n, supply, demand, cost_matrix_flat)]
        return []

    def extract_numbers(self):
        return list(map(int, re.findall(r'\d+', self.text)))
    
    def evaluate_variant(self, variant, all_numbers):
        m, n, supply, demand, cost_matrix = variant
        used_numbers = supply + demand + cost_matrix
        return Counter(used_numbers) == Counter(all_numbers)

    def parse_numeric_problem(self):
        numbers = self.extract_numbers()
        total_numbers = len(numbers)
        variants = []

        for m in range(1, total_numbers // 2):
            for n in range(1, total_numbers // 2):
                if m * n <= total_numbers - m - n:
                    # Вариант 1: Запасы, Потребности, Матрица стоимостей
                    supply = numbers[:m]
                    demand = numbers[m:m+n]
                    cost_matrix = numbers[m+n:m+n+m*n]
                    if len(cost_matrix) == m * n:
                        variant = (m, n, supply, demand, cost_matrix)
                        if self.evaluate_variant(variant, numbers):
                            variants.append(variant)

                    # Вариант 2: Потребности, Запасы, Матрица стоимостей
                    demand = numbers[:n]
                    supply = numbers[n:n+m]
                    cost_matrix = numbers[n+m:n+m+m*n]
                    if len(cost_matrix) == m * n:
                        variant = (m, n, supply, demand, cost_matrix)
                        if self.evaluate_variant(variant, numbers):
                            variants.append(variant)

                    # Вариант 3: Матрица стоимостей, Запасы, Потребности
                    cost_matrix = numbers[:m*n]
                    supply = numbers[m*n:m*n+m]
                    demand = numbers[m*n+m:m*n+m+n]
                    if len(cost_matrix) == m * n:
                        variant = (m, n, supply, demand, cost_matrix)
                        if self.evaluate_variant(variant, numbers):
                            variants.append(variant)

        return variants

    def parse_transport_problem(self):
        # Сначала пробуем распарсить как задачу с именами
        named_result = self.parse_named_problem()
        if named_result:
            return named_result
        
        # Если не получилось, пробуем числовой вариант
        return self.parse_numeric_problem()

# Пример использования
# if __name__ == "__main__":
#     text1 = """
#     Есть 4 поставщика (A, B, C, D) с запасами груза:
#     A = 120 т
#     B = 80 т
#     C = 100 т
#     D = 60 т
#     5 потребителей (1, 2, 3, 4, 5) с потребностями:
#     1 = 70 т
#     2 = 90 т
#     3 = 50 т
#     4 = 110 т
#     5 = 40 т
#     Стоимости перевозок (у.е./т) заданы матрицей:
#          1   2   3   4   5
#     A   5   8   6   7   4
#     B   4   3   2   5   6
#     C   7   5   4   6   8
#     D   3   6   7   4   5
#     """

#     text2 = """
#     30 50 80 25 45 55 25
#     3 1 7 4
#     2 6 5 9
#     8 3 3 2
#     """

#     parser1 = TransportProblemParser(text1)
#     variants1 = parser1.parse_transport_problem()

#     parser2 = TransportProblemParser(text2)
#     variants2 = parser2.parse_transport_problem()

#     def print_variants(variants):
#         for i, (m, n, supply, demand, cost_matrix) in enumerate(variants):
#             print(f"Вариант {i + 1}:")
#             print(f"Поставщики (m): {m}")
#             print(f"Потребители (n): {n}")
#             print(f"Запасы: {supply}")
#             print(f"Потребности: {demand}")
#             print(f"Матрица стоимостей: {cost_matrix}")
#             print()

#     print("Результат для текста с именами:")
#     print_variants(variants1)

#     print("\nРезультат для числового текста:")
#     print_variants(variants2)