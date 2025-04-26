import re
from collections import defaultdict, Counter

class TransportProblemParser:
    def __init__(self, text):
        self.cost_matrix_from_text = None
        self.text = text.strip()
        self.lines = [line.strip() for line in self.text.split('\n') if line.strip()]

    def parse_named_problem(self):
        suppliers = {}
        consumers = {}
        cost_matrix = defaultdict(dict)
        
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
                match = re.match(r'([A-Za-zА-Яа-я]+)\s*=\s*(\d+)', line)
                if match:
                    supplier, amount = match.groups()
                    suppliers[supplier] = int(amount)
                    
            elif consumer_section:
                match = re.match(r'([A-Za-zА-Яа-я0-9]+)\s*=\s*(\d+)', line)
                if match:
                    consumer, amount = match.groups()
                    consumers[consumer] = int(amount)
                    
            elif cost_matrix_section:
                if re.match(r'^\s*[A-Za-zА-Яа-я]+\s+[\d\s]+$', line):
                    parts = re.split(r'\s{2,}', line.strip())
                    supplier = parts[0]
                    costs = [int(num) for num in re.findall(r'\d+', ' '.join(parts[1:]))]
                    
                    if len(costs) == len(consumers):
                        for i, cost in enumerate(costs):
                            consumer = list(consumers.keys())[i]
                            cost_matrix[supplier][consumer] = cost
        if suppliers and consumers and cost_matrix:
            m = len(suppliers)
            n = len(consumers)
            supply = list(suppliers.values())
            demand = list(consumers.values())
            
            cost_matrix_flat = []
            for supplier in suppliers:
                for consumer in consumers:
                    cost_matrix_flat.append(cost_matrix[supplier][consumer])
            
            return [(m, n, supply, demand, cost_matrix_flat)]
        return []

    def extract_numbers(self):
        return list(map(int, re.findall(r'\d+', self.text)))
    
    def evaluate_variant(self, variant, all_numbers):
        m, n, supply, demand, cost_matrix, _ = variant
        used_numbers = supply + demand + cost_matrix
        return Counter(used_numbers) == Counter(all_numbers)
    
    def parse_cost_matrix(self):
        self.cost_matrix_from_text = None
        number_lines = []
        for line in self.lines:
            numbers = list(map(int, re.findall(r'\d+', line)))
            if numbers:
                number_lines.append((len(numbers), numbers))
        
        if not number_lines:
            return None
        
        sequences = []
        current_sequence = []
        current_length = number_lines[0][0]
        
        for length, numbers in number_lines:
            if length == current_length:
                current_sequence.append(numbers)
            else:
                if len(current_sequence) >= 2:
                    sequences.append((current_length, current_sequence))
                current_sequence = [numbers]
                current_length = length
        
        if len(current_sequence) >= 2:
            sequences.append((current_length, current_sequence))
        
        if not sequences:
            return None
        
        best_sequence = max(sequences, key=lambda x: x[0])
        
        if all(len(row) == best_sequence[0] for row in best_sequence[1]):
            self.cost_matrix_from_text = best_sequence[1]
        
        return self.cost_matrix_from_text
        
    def compare_matrices(self, numeric_matrix, text_matrix):
        if not numeric_matrix or not text_matrix:
            return 0.0
        
        if isinstance(numeric_matrix, list) and isinstance(numeric_matrix[0], int): 
            m = len(text_matrix)
            n = len(text_matrix[0]) if m > 0 else 0
            if m * n == len(numeric_matrix):
                numeric_matrix = [numeric_matrix[i*n:(i+1)*n] for i in range(m)]
            else:
                return 0.0
        
        m1 = len(numeric_matrix)
        n1 = len(numeric_matrix[0]) if m1 > 0 else 0
        m2 = len(text_matrix)
        n2 = len(text_matrix[0]) if m2 > 0 else 0
        
        if m1 == 0 or n1 == 0 or m2 == 0 or n2 == 0:
            return 0.0
        
        max_matches = 0
        min_rows = min(m1, m2)
        min_cols = min(n1, n2)
        
        for row_offset in range(abs(m1 - m2) + 1):
            for col_offset in range(abs(n1 - n2) + 1):
                matches = 0
                for i in range(min_rows):
                    for j in range(min_cols):
                        if (row_offset + i < m1 and col_offset + j < n1 and 
                            i < m2 and j < n2 and 
                            numeric_matrix[row_offset + i][col_offset + j] == text_matrix[i][j]):
                            matches += 1
                max_matches = max(max_matches, matches)
        
        total_elements_in_overlap = min(m1 * n1, m2 * n2)
        return max_matches / total_elements_in_overlap if total_elements_in_overlap > 0 else 0.0

    def parse_numeric_problem(self):
        numbers = self.extract_numbers()
        total_numbers = len(numbers)
        variants = []

        for m in range(1, total_numbers // 2):
            for n in range(1, total_numbers // 2):
                if m * n <= total_numbers - m - n:
                    supply = numbers[:m]
                    demand = numbers[m:m+n]
                    cost_matrix_long = numbers[m+n:m+n+m*n]
                    cost_matrix = [cost_matrix_long[i:i+len(demand)] for i in range(0, len(cost_matrix_long), len(demand))]
                    if len(cost_matrix_long) == m * n:
                        variant = (m, n, supply, demand, cost_matrix_long, cost_matrix)
                        if self.evaluate_variant(variant, numbers):
                            variants.append(variant)

                    demand = numbers[:n]
                    supply = numbers[n:n+m]
                    cost_matrix_long = numbers[n+m:n+m+m*n]
                    cost_matrix = [cost_matrix_long[i:i+len(demand)] for i in range(0, len(cost_matrix_long), len(demand))]
                    
                    if len(cost_matrix_long) == m * n:
                        variant = (m, n, supply, demand, cost_matrix_long, cost_matrix)
                        if self.evaluate_variant(variant, numbers):
                            variants.append(variant)

                    cost_matrix_long = numbers[:m*n]
                    supply = numbers[m*n:m*n+m]
                    demand = numbers[m*n+m:m*n+m+n]
                    cost_matrix = [cost_matrix_long[i:i+len(demand)] for i in range(0, len(cost_matrix_long), len(demand))]
                    
                    if len(cost_matrix_long) == m * n:
                        variant = (m, n, supply, demand, cost_matrix_long, cost_matrix)
                        if self.evaluate_variant(variant, numbers):
                            variants.append(variant)

        if not variants:
            named_supplies = {}
            named_demands = {}
            other_numbers = []
            
            for line in self.lines:
                match = re.match(r'^([A-Za-zА-Яа-я0-9]+)\s*=\s*(\d+)', line)
                if match:
                    name, value = match.groups()
                    value = int(value)
                    if re.match(r'^[A-Za-zА-Яа-я]+$', name):
                        named_supplies[name] = value
                    else:
                        named_demands[name] = value
                else:
                    other_numbers.extend(list(map(int, re.findall(r'\d+', line))))
            
            if named_supplies and named_demands:
                m = len(named_supplies)
                n = len(named_demands)
                supply = list(named_supplies.values())
                demand = list(named_demands.values())
                
                required_matrix_size = m * n
                if len(other_numbers) >= required_matrix_size:
                    cost_matrix_long = other_numbers[:required_matrix_size]
                    cost_matrix = [cost_matrix_long[i:i+n] for i in range(0, len(cost_matrix_long), n)]
                    variant = (m, n, supply, demand, cost_matrix_long, cost_matrix)
                    if self.evaluate_variant(variant, numbers):
                        variants.append(variant)

        if not variants:
            single_number_lines = []
            for line in self.lines:
                nums = list(map(int, re.findall(r'\d+', line)))
                if len(nums) == 1:
                    single_number_lines.append(nums[0])
            
            if len(single_number_lines) >= 2:
                for split_point in range(1, len(single_number_lines)):
                    supply = single_number_lines[:split_point]
                    demand = single_number_lines[split_point:]
                    
                    remaining_numbers = [num for num in numbers if num not in supply and num not in demand]
                    
                    m = len(supply)
                    n = len(demand)
                    
                    if m * n == len(remaining_numbers):
                        cost_matrix_long = remaining_numbers
                        cost_matrix = [cost_matrix_long[i:i+n] for i in range(0, len(cost_matrix_long), n)]
                        variant = (m, n, supply, demand, cost_matrix_long, cost_matrix)
                        if self.evaluate_variant(variant, numbers):
                            variants.append(variant)


        max_score = 0
        scores = []
        for i in variants:
            score = self.compare_matrices(i[5], self.cost_matrix_from_text)
            if score > max_score:
                max_score = score
            scores.append([i, score])
        vars = []
        for sc in scores:
            if sc[1] == max_score:
                vars.append(sc[0])
        
        return vars

    def parse_transport_problem(self):
        named_result = self.parse_named_problem()
        if named_result:
            return named_result
        
        self.parse_cost_matrix()
        return self.parse_numeric_problem()