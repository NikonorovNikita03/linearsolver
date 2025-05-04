import numpy as np
from scipy.optimize import linprog

class Solver(object):

    def __init__(self, s_v, d_v, c_m, time_vector=None, speed_matrix=None, bound_top = None, bound_down = None):
        self.supply_vector = s_v
        self.demand_vector = d_v
        self.cost_matrix = c_m

        self.time_vector = time_vector
        self.speed_matrix = speed_matrix
        self.bound_top = bound_top
        self.bound_down = bound_down

    
    # def solve_transportation_scipy(self):
    #     problem = "standard"
        
    #     if True:
    #         problem = "time"
    #     match problem:
    #         case "time":
    #             return self.solve_transportation_scipy_time()
    #         case _:
    #             return self.solve_transportation_scipy_standard()

    def solve_transportation_scipy_double(self):
        supply = self.supply_vector
        demand = self.demand_vector
        costs = self.cost_matrix

        n_sources = len(supply)  # количество поставщиков (включая фиктивного)
        n_destinations = len(demand)  # количество потребителей (включая фиктивного)
        n_products = len(supply[0])  # количество продуктов

        info = {
            "balanced": True
        }

        for n in range(n_products):
            supply_n = sum([supply[x][n] for x in range(n_sources)])
            demand_n = sum([demand[x][n] for x in range(n_destinations)])

            if supply_n > demand_n:
                info["balanced"] = False
                if not "balanced_demand_items" in info:
                    info["balanced_demand_items"] = {}
                for i in range(len(costs)):
                    costs[i].append([0 for i in range(n_products)])
                new_demand = [0 for i in range(n_products)]
                new_demand[n] = supply_n - demand_n
                info["balanced_demand_items"][f"Продукт {n+1}"] = supply_n - demand_n
                demand.append(new_demand)
                n_destinations += 1

            if supply_n < demand_n:
                info["balanced"] = False
                if not "balanced_supply_items" in info:
                    info["balanced_supply_items"] = {}
                costs.append([[0 for i in range(n_products)] for j in range(n_destinations)])
                new_supply = np.zeros(n_products)
                new_supply[n] = demand_n - supply_n
                info["balanced_supply_items"][f"Продукт {n+1}"] = demand_n - supply_n
                supply.append(new_supply)
                n_sources += 1

        costs = np.array(costs)
        supply = np.array(supply)
        demand = np.array(demand)

        c_list = []
        for i in range(n_sources):
            for j in range(n_destinations):
                for p in range(n_products):
                    c_list.append(costs[i, j, p] if i < 3 else 0)  # фиктивный поставщик имеет нулевую стоимость

        c = np.array(c_list)

        num_vars = n_sources * n_destinations * n_products
        A_eq = []
        b_eq = []

        for i in range(n_sources):
            for p in range(n_products):
                row = np.zeros(num_vars)
                for j in range(n_destinations):
                    idx = (i * n_destinations * n_products) + (j * n_products) + p
                    row[idx] = 1
                A_eq.append(row)
                b_eq.append(supply[i, p])

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

        bounds = [(0, None) for _ in range(num_vars)]

        result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        return result.x.reshape((n_sources, n_destinations, n_products)), result.fun, info


    def solve_transportation_scipy(self):
        if self.bound_top:
            
            supply_index = self.bound_top[0]
            old_supply = self.supply_vector[supply_index]
            self.supply_vector[supply_index] = self.bound_top[2]        
            self.supply_vector = np.insert(np.copy(self.supply_vector), supply_index + 1, old_supply - self.bound_top[2])
            #self.supply_vector.insert(supply_index + 1, old_supply - self.bound_top[2])

            row_i = self.cost_matrix[supply_index, :].copy()
            new_row_for_i_b = row_i.copy()
            new_row_for_i_b[self.bound_top[1]] = 0

            self.cost_matrix = np.insert(np.copy(self.cost_matrix), supply_index + 1, new_row_for_i_b, axis=0)

        if self.bound_down:
            self.supply_vector[self.bound_down[0]] -= self.bound_down[2]
            self.demand_vector[self.bound_down[1]] -= self.bound_down[2]

        a, b, _, C = self.__surplus()
        if self.bound_top:
            result = self.nwc_rule()
            return result[0], result[1]

        m, n = C.shape
        c = C.flatten()
        
        A_eq = []
        for i in range(m):
            row = np.zeros((m, n))
            row[i, :] = 1
            A_eq.append(row.flatten())
        for j in range(n):
            col = np.zeros((m, n))
            col[:, j] = 1
            A_eq.append(col.flatten())
        A_eq = np.array(A_eq)
        b_eq = np.concatenate([a, b])

        bounds = (0, None)
        if self.time_vector and self.speed_matrix:
            tv = np.array(self.time_vector)
            sm = np.array(self.speed_matrix)
            bounds = []
            for row in sm:
                for i in range(len(row)):
                    bounds.append((0, tv[i] * row[i]))
        

        res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
        X = res.x.reshape((m, n))

        if self.bound_down:
            X[self.bound_down[0], self.bound_down[1]] += self.bound_down[2]

        total_cost = np.sum(X * C)
        return X, total_cost

    def solve_transportation_scipy_time_(self, time_vector, speed_matrix):
        a, b, _, C = self.__surplus()
        m, n = C.shape
        c = C.flatten()
        time_vector, speed_matrix = np.array(time_vector), np.array(speed_matrix)
        
        A_eq = []
        for i in range(m):
            row = np.zeros((m, n))
            row[i, :] = 1
            A_eq.append(row.flatten())
        for j in range(n):
            col = np.zeros((m, n))
            col[:, j] = 1
            A_eq.append(col.flatten())
        A_eq = np.array(A_eq)
        b_eq = np.concatenate([a, b])

        bounds = []
        for row in speed_matrix:
            for i in range(len(row)):
                bounds.append((0, time_vector[i] * row[i]))
        
        res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
        X = res.x.reshape((m, n))
        total_cost = np.sum(X * C)
        return X, total_cost

    def solve_transportation_scipy_standard(self):
        a, b, _, C = self.__surplus()
        m, n = C.shape
        c = C.flatten()

        A_eq = []
        for i in range(m):
            row = np.zeros((m, n))
            row[i, :] = 1
            A_eq.append(row.flatten())
        for j in range(n):
            col = np.zeros((m, n))
            col[:, j] = 1
            A_eq.append(col.flatten())
        A_eq = np.array(A_eq)
        b_eq = np.concatenate([a, b])
        
        # print(A_eq)
        # print(A_eq[:-1])

        # print(b_eq)
        # print(b_eq[:-1])
        #res = linprog(c, A_eq=A_eq[:-1], b_eq=b_eq[:-1], bounds=(0, None))
        res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=(0, None))
        X = res.x.reshape((m, n))
        total_cost = np.sum(X * C)
        return X, total_cost

    def double_preference(self):
        s_v_tmp, d_v_tmp, t_m_tmp, c_m_tmp = self.__surplus()

        mins = {}

        for i in range(len(s_v_tmp)):
            min_val = np.min(c_m_tmp[i])
            mins_to_add = [x for x in range(len(d_v_tmp)) if c_m_tmp[i][x] == min_val]
            for k in mins_to_add:
                if (i, k) in mins:
                    mins[(i, k)] += 1
                else:
                    mins[(i, k)] = 1
        for j in range(len(d_v_tmp)):
            col = [c_m_tmp[x][j] for x in range(len(s_v_tmp))]
            min_val = np.min(col)
            mins_to_add = [x for x in range(len(s_v_tmp)) if col[x] == min_val]
            for k in mins_to_add:
                if (k, j) in mins:
                    mins[(k, j)] += 1
                else:
                    mins[(k, j)] = 1
        
        d_2 = {}
        d_1 = {}

        for i, k in mins:
            if mins[(i, k)] == 2:
                d_2[(i, k)] = (c_m_tmp[i][k])
            if mins[(i, k)] == 1:
                d_1[(i, k)] = (c_m_tmp[i][k])
        
        #print(sorted(d_2, key=d_2.get) + sorted(d_1, key=d_1.get))
        for i, k in sorted(d_2, key=d_2.get) + sorted(d_1, key=d_1.get):
            # print(s_v_tmp[i], d_v_tmp[k])
            # print(s_v_tmp)
            min_val = min(s_v_tmp[i], d_v_tmp[k])
            s_v_tmp[i] -= min_val
            d_v_tmp[k] -= min_val
            t_m_tmp[i][k] = min_val
            #print(t_m_tmp)
        
        


        total_costs, surplus = self.__costs(t_m_tmp)

        return t_m_tmp, total_costs, surplus

    def vogel_rule(self):
        s_v_tmp, d_v_tmp, t_m_tmp, c_m_tmp = self.__surplus()

        turn_off = []
        while(sum(s_v_tmp) + sum(d_v_tmp) > 0):
            rows_cols = []
            diffs = []
            for i in range(len(s_v_tmp)):
                new_diff = []
                cords = []
                for j in range(len(d_v_tmp)):
                    if not (i, j) in turn_off:
                        new_diff.append(c_m_tmp[i][j])
                        cords.append((i, j))
                if new_diff:
                    rows_cols.append([new_diff, cords])
            for j in range(len(d_v_tmp)):
                new_diff = []
                cords = []
                for i in range(len(s_v_tmp)):
                    if not (i, j) in turn_off:
                        new_diff.append(c_m_tmp[i][j])
                        cords.append((i, j))
                if new_diff:
                    rows_cols.append([new_diff, cords]) 
            
            for rc in rows_cols:
                diff = sorted(set(rc[0]))[1] - min(rc[0]) if len(rc[0]) != 1 else 0
                diffs.append(diff)
            
            if diffs:
                max_diff = np.argmax(diffs)
                min_cord = np.argmin(rows_cols[max_diff][0])
                needed_cords = rows_cols[max_diff][1][min_cord]    
            else:
                needed_cords = (np.argmax(s_v_tmp), np.argmax(d_v_tmp))

            min_val = min(s_v_tmp[needed_cords[0]], d_v_tmp[needed_cords[1]])
            s_v_tmp[needed_cords[0]] -= min_val
            d_v_tmp[needed_cords[1]] -= min_val
            t_m_tmp[needed_cords[0]][needed_cords[1]] = min_val

            if diffs:
                for cord in rows_cols[max_diff][1]:
                    if not cord in turn_off:
                        turn_off.append(cord)
        
        total_costs, surplus = self.__costs(t_m_tmp)

        return t_m_tmp, total_costs, surplus

    def nwc_rule(self):
        j = 0
        i = 0
        s_v_tmp, d_v_tmp, t_m_tmp, c_m_tmp = self.__surplus()

        print(t_m_tmp)

        while j < d_v_tmp.size and i < s_v_tmp.size:
            amount = min(d_v_tmp[j], s_v_tmp[i])

            d_v_tmp[j] = d_v_tmp[j] - amount
            s_v_tmp[i] = s_v_tmp[i] - amount
            t_m_tmp[i][j] = amount

            if s_v_tmp[i] == 0:
                i += 1
            else:
                j += 1

        total_costs, surplus = self.__costs(t_m_tmp)

        return t_m_tmp, total_costs, surplus

    def cm_rule(self):
        s_v_tmp, d_v_tmp, t_m_tmp, c_m_tmp = self.__surplus()

        columns = list(range(0, d_v_tmp.size))
        rows = list(range(0, s_v_tmp.size))
        infinity = np.inf

        while len(columns) > 0:

            j = min(columns)

            tmp = c_m_tmp[:, j]
            tmp = tmp.tolist()

            minima = min(tmp)
            i = tmp.index(minima)

            while i not in rows:
                if self.surplus == "demand" and len(rows) == 1:
                    i = s_v_tmp.size - 1
                    break

                tmp[i] = infinity
                minima = min(tmp)
                i = tmp.index(minima)

                if not rows:
                    break

            if d_v_tmp[j] >= s_v_tmp[i]:
                amount = s_v_tmp[i]
            else:
                amount = d_v_tmp[j]

            d_v_tmp[j] = d_v_tmp[j] - amount
            s_v_tmp[i] = s_v_tmp[i] - amount
            t_m_tmp[i][j] = amount

            if s_v_tmp[i] == 0 or (np.sum(d_v_tmp) == 0 and s_v_tmp[i] == infinity):
                rows.remove(i)
            if d_v_tmp[j] == 0 or (np.sum(s_v_tmp) == 0 and d_v_tmp[j] == infinity):
                columns.remove(j)

        total_costs, surplus = self.__costs(t_m_tmp)

        return t_m_tmp, total_costs, surplus

    def __costs(self, transport_matrix):
        surplus = 0
        transport_matrix = np.copy(transport_matrix)

        if self.surplus == "demand":
            surplus = np.sum(transport_matrix[-1, :])
            surplus = surplus * -1
            transport_matrix = np.delete(transport_matrix, -1, axis=0)

        if self.surplus == "supply":
            surplus = np.sum(transport_matrix[:, -1])
            transport_matrix = np.delete(transport_matrix, -1, axis=1)

        tmp = np.multiply(transport_matrix, self.cost_matrix)

        return tmp.sum(), surplus

    def __surplus(self):
        s_v_tmp = np.copy(self.supply_vector)
        d_v_tmp = np.copy(self.demand_vector)
        t_m_tmp = np.copy(np.zeros((s_v_tmp.size, d_v_tmp.size)))
        c_m_tmp = np.copy(self.cost_matrix)

        infinity = np.inf

        if np.sum(s_v_tmp) > np.sum(d_v_tmp):
            d_v_tmp = np.append(d_v_tmp, np.sum(s_v_tmp) - np.sum(d_v_tmp))
            new_column_tmp = np.zeros((s_v_tmp.size, 1))
            t_m_tmp = np.append(t_m_tmp, new_column_tmp, axis=1)
            c_m_tmp = np.append(c_m_tmp, new_column_tmp, axis=1)
            self.surplus = "supply"
        elif np.sum(s_v_tmp) < np.sum(d_v_tmp):
            s_v_tmp = np.append(s_v_tmp, np.sum(d_v_tmp) - np.sum(s_v_tmp))
            new_row_t_tmp = np.zeros((1, d_v_tmp.size))
            #new_row_c_tmp = np.full((1, d_v_tmp.size), infinity)
            t_m_tmp = np.append(t_m_tmp, new_row_t_tmp, axis=0)
            c_m_tmp = np.append(c_m_tmp, new_row_t_tmp, axis=0)
            #c_m_tmp = np.append(c_m_tmp, new_row_c_tmp, axis=0)
            self.surplus = "demand"
        else:
            self.surplus = "equal"

        return s_v_tmp, d_v_tmp, t_m_tmp, c_m_tmp

    def row_minina(self):
        supply, demand, t_m_tmp, cost = self.__surplus()
        big_number = np.sum(cost)

        row_number = 0
        while row_number < len(cost):        
            smallest_cost = min(cost[row_number])

            supply_change_index = row_number
            demand_change_index = np.where(cost[row_number] == smallest_cost)[0][0]

            supply_bigger = supply[supply_change_index] > demand[demand_change_index]
            demand_bigger = supply[supply_change_index] < demand[demand_change_index]

            allocation = supply[supply_change_index] if not supply_bigger else demand[demand_change_index]

            t_m_tmp[supply_change_index][demand_change_index] = allocation
            demand[demand_change_index] -= allocation
            supply[supply_change_index] -= allocation

            if not demand_bigger:
                for i in range(len(supply)):
                    cost[i][demand_change_index] = big_number

            if not supply_bigger:
                row_number += 1
                for i in range(len(demand)):
                    cost[supply_change_index][i] = big_number

        total_costs, surplus = self.__costs(t_m_tmp)
        return t_m_tmp, total_costs, surplus
    
    def column_minima(self):
        supply, demand, t_m_tmp, cost = self.__surplus()
        big_number = np.sum(cost)

        column_number = 0
        while column_number < len(cost[0]):
            current_column = [cost[i][column_number] for i in range(len(supply))]
            smallest_cost = min(current_column)
            
            supply_change_index = np.where(current_column == smallest_cost)[0][0]
            demand_change_index = column_number

            supply_bigger = supply[supply_change_index] > demand[demand_change_index]
            demand_bigger = supply[supply_change_index] < demand[demand_change_index]

            allocation = supply[supply_change_index] if not supply_bigger else demand[demand_change_index]

            t_m_tmp[supply_change_index][demand_change_index] = allocation
            demand[demand_change_index] -= allocation
            supply[supply_change_index] -= allocation

            if not demand_bigger:
                column_number += 1
                for i in range(len(supply)):
                    cost[i][demand_change_index] = big_number

            if not supply_bigger:
                for i in range(len(demand)):
                    cost[supply_change_index][i] = big_number
        
        total_costs, surplus = self.__costs(t_m_tmp)
        return t_m_tmp, total_costs, surplus
    
    def russell_approximation(self):
        supply, demand, t_m_tmp, cost = self.__surplus()
        big_number = np.sum(cost)

        zero_matrix = np.copy(t_m_tmp)
        while np.sum(cost) != big_number * len(supply) * len(demand):
            supply_largest = []
            for row_index in range(len(supply)):
                row = [x for x in cost[row_index] if x != big_number]
                supply_largest.append(max(row) if row else 0)
            
            demand_largest = []
            for col_index in range(len(demand)):
                col = [
                    x for x in 
                    [cost[i][col_index] for i in range(len(supply))]
                    if x != big_number
                ]
                demand_largest.append(max(col) if col else 0)
            reduced_cost = np.copy(zero_matrix)

            negative_largest = [0, 0, 0]
            for supply_index in range(len(supply)):
                for demand_index in range(len(demand)):
                    if cost[supply_index][demand_index] == big_number:
                        continue
                    negative_cost = cost[supply_index][demand_index] - supply_largest[supply_index] - demand_largest[demand_index]
                    reduced_cost[supply_index][demand_index] = negative_cost
                    if negative_largest[0] >= negative_cost:
                        negative_largest = [negative_cost, supply_index, demand_index]
            allocation = min(supply[negative_largest[1]], demand[negative_largest[2]])

            t_m_tmp[negative_largest[1]][negative_largest[2]] = allocation
            supply[negative_largest[1]] -= allocation
            demand[negative_largest[2]] -= allocation

            if supply[negative_largest[1]] == 0:
                for i in range(len(demand)):
                    cost[negative_largest[1]][i] = big_number
            
            if demand[negative_largest[2]] == 0:
                for i in range(len(supply)):
                    cost[i][negative_largest[2]] = big_number

        total_costs, surplus = self.__costs(t_m_tmp)
        return t_m_tmp, total_costs, surplus
    
    def heuristic_1(self):
        supply, demand, t_m_tmp, cost = self.__surplus()
        big_number = np.sum(cost)

        max_sum = big_number * len(supply) * len(demand)
        while np.sum(cost) != max_sum:
            supply_pxt = []
            demand_pxt = []

            for row_index in range(len(supply)):
                if np.sum(cost[row_index]) == big_number * len(demand):
                    supply_pxt.append(big_number * big_number)
                    continue
                
                min_elem_index = np.argmin(cost[row_index])
                row_penalty = min(np.delete(cost[row_index], min_elem_index)) - cost[row_index][min_elem_index]
                pxt = sum(np.delete(cost[row_index], np.where(cost[row_index] == big_number)[0])) * row_penalty 
                supply_pxt.append(pxt)
            
            for col_index in range(len(demand)):
                column = [cost[i][col_index] for i in range(len(supply))]
                if np.sum(column) == big_number * len(supply):
                    demand_pxt.append(big_number * big_number)
                    continue

                min_elem_index = np.argmin(column)
                col_penalty = min(np.delete(column, min_elem_index)) - column[min_elem_index]
                pxt = sum(np.delete(column, np.where(column == big_number))) * col_penalty
                demand_pxt.append(pxt)
            
            spxt_min_index = np.argmin(supply_pxt)
            dpxt_min_index = np.argmin(demand_pxt)

            if supply_pxt[spxt_min_index] <= demand_pxt[dpxt_min_index]:
                supply_index = spxt_min_index
                demand_index = np.argmin(cost[spxt_min_index])
            else:
                column = [cost[i][dpxt_min_index] for i in range(len(supply))]
                supply_index = np.argmin(column)
                demand_index = dpxt_min_index
            
            allocation = min(supply[supply_index], demand[demand_index])
            t_m_tmp[supply_index][demand_index] = allocation
            supply[supply_index] -= allocation
            demand[demand_index] -= allocation

            if supply[supply_index] == 0:
                for i in range(len(demand)):
                    cost[supply_index][i] = big_number

            if demand[demand_index] == 0:
                for i in range(len(supply)):
                    cost[i][demand_index] = big_number

        total_costs, surplus = self.__costs(t_m_tmp)
        return t_m_tmp, total_costs, surplus

    def heuristic_2(self):
        supply, demand, t_m_tmp, cost = self.__surplus()
        big_number = np.sum(cost)

        max_sum = big_number * len(supply) * len(demand)
        
        while np.sum(cost) != max_sum:
            supply_penalties = []
            demand_penalties = []
            for row_index in range(len(supply)):
                if sum(cost[row_index]) == big_number * len(demand):
                    supply_penalties.append(-big_number)
                    continue

                row = np.delete(cost[row_index], np.where(cost[row_index] == big_number))
                supply_penalties.append(max(row) - min(row))
            
            for column_index in range(len(demand)):
                col = [cost[i][column_index] for i in range(len(supply))]
                if sum(col) == big_number * len(supply):
                    demand_penalties.append(-big_number)
                    continue

                col = np.delete(col, np.where(col == big_number))
                demand_penalties.append(max(col) - min(col))

            supply_max_arg = np.argmax(supply_penalties)
            demand_max_arg = np.argmax(demand_penalties)

            if supply_penalties[supply_max_arg] >= demand_penalties[demand_max_arg]:
                supply_index = supply_max_arg
                demand_index = np.argmin(cost[supply_max_arg])
            else:
                column = [cost[i][demand_max_arg] for i in range(len(supply))]
                supply_index = np.argmin(column)
                demand_index = demand_max_arg

            allocation = min(supply[supply_index], demand[demand_index])
            t_m_tmp[supply_index][demand_index] = allocation
            supply[supply_index] -= allocation
            demand[demand_index] -= allocation

            if supply[supply_index] == 0:
                for i in range(len(demand)):
                    cost[supply_index][i] = big_number

            if demand[demand_index] == 0:
                for i in range(len(supply)):
                    cost[i][demand_index] = big_number

        total_costs, surplus = self.__costs(t_m_tmp)
        return t_m_tmp, total_costs, surplus
    
    def modi_method(self):
        supply, demand, _, cost = self.__surplus()
        t_m_tmp, _, surplus = self.vogel_rule()
        big_number = np.sum(cost)

        occupied_cells_supply = [-big_number for i in range(len(supply))]
        occupied_cells_demand = [-big_number for i in range(len(demand))]

        occupied_cells = [-big_number for i in range(len(supply) + len(demand))]

        max_positive = [0, 0]
        for i in range(len(supply) + len(demand)):
            ar = t_m_tmp[i] if i < len(supply) else t_m_tmp[:, i - len(supply)]
            ar_sum = sum(np.array(ar > 0))
            if max_positive[0] <= ar_sum:
                max_positive = [ar_sum, i]
        
        num = max_positive[1]
        occupied_cells[num] = 0
        print(num)
        if num < len(supply):
            print("eba")    
        else:
            for i in range(len(supply)):
                if t_m_tmp[i][num - len(supply)] != 0:
                    occupied_cells[i] = cost[i][num - len(supply)]
                    for k in range(len(demand)):
                        if t_m_tmp[i][k] != 0:
                            occupied_cells[k + len(supply)] = cost[i][k] - occupied_cells[i]
        
        for i in range(len(supply)):
            for k in range(len(demand)):
                if t_m_tmp[i][k] != 0:
                    continue
                t_m_tmp[i][k] = cost[i][k] - occupied_cells[i] - occupied_cells[k + len(supply)]

        print(t_m_tmp)
        





        total_costs, surplus = self.__costs(t_m_tmp)
        return t_m_tmp, total_costs, surplus
