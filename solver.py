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

    def solve_transportation_scipy_double(self):
        supply = self.supply_vector
        demand = self.demand_vector
        costs = self.cost_matrix

        n_sources = len(supply) 
        n_destinations = len(demand)
        n_products = len(supply[0])

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
                    c_list.append(costs[i, j, p] if i < 3 else 0)

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

        if np.sum(s_v_tmp) > np.sum(d_v_tmp):
            d_v_tmp = np.append(d_v_tmp, np.sum(s_v_tmp) - np.sum(d_v_tmp))
            new_column_tmp = np.zeros((s_v_tmp.size, 1))
            t_m_tmp = np.append(t_m_tmp, new_column_tmp, axis=1)
            c_m_tmp = np.append(c_m_tmp, new_column_tmp, axis=1)
            self.surplus = "supply"
        elif np.sum(s_v_tmp) < np.sum(d_v_tmp):
            s_v_tmp = np.append(s_v_tmp, np.sum(d_v_tmp) - np.sum(s_v_tmp))
            new_row_t_tmp = np.zeros((1, d_v_tmp.size))
            t_m_tmp = np.append(t_m_tmp, new_row_t_tmp, axis=0)
            c_m_tmp = np.append(c_m_tmp, new_row_t_tmp, axis=0)
            self.surplus = "demand"
        else:
            self.surplus = "equal"

        return s_v_tmp, d_v_tmp, t_m_tmp, c_m_tmp