import sqlite3
import json
from typing import Dict, Any, List, Optional

class ProblemDatabase:
    def __init__(self, db_name: str = "problems.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS linear_programming_problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            problem_text TEXT,
            problem_type TEXT CHECK(problem_type IN ('max', 'min')),
            costs_json TEXT NOT NULL,
            constraints_json TEXT NOT NULL,
            signs_json TEXT NOT NULL,
            function_json TEXT NOT NULL,
            names_x_json TEXT NOT NULL,
            names_y_json TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignment_problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            problem_text TEXT,
            costs_json TEXT NOT NULL,
            names_x_json TEXT NOT NULL,
            names_y_json TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transport_problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            problem_text TEXT,
            costs_json TEXT NOT NULL,
            supply_json TEXT NOT NULL,
            demand_json TEXT NOT NULL,
            names_x_json TEXT NOT NULL,
            names_y_json TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS multi_transport_problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            problem_text TEXT,
            costs_json TEXT NOT NULL,
            supply_json TEXT NOT NULL,
            demand_json TEXT NOT NULL
        )
        """)
        self.conn.commit()

    def _get_table_name(self, problem_type: str) -> str:
        table_map = {
            "ЗЛП": "linear_programming_problems",
            "Задача о назначениях": "assignment_problems",
            "Транспортная задача": "transport_problems",
            "Многопродуктовая транспортная задача": "multi_transport_problems"
        }
        return table_map.get(problem_type)

    def create_problem(self, problem_data: Dict[str, Any], problem_text: str = "") -> bool:
        problem_type = problem_data.get("type")
        if not problem_type:
            return False

        table_name = self._get_table_name(problem_type)
        if not table_name:
            return False

        try:
            if problem_type == "ЗЛП":
                self.cursor.execute(
                    """INSERT INTO linear_programming_problems 
                    (id, name, problem_text, problem_type, costs_json, constraints_json, 
                     signs_json, function_json, names_x_json, names_y_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        problem_data["id"],
                        problem_data["name"],
                        problem_text,
                        problem_data["data"]["problem_type"],
                        json.dumps(problem_data["data"]["costs"]),
                        json.dumps(problem_data["data"]["constraints"]),
                        json.dumps(problem_data["data"]["signs"]),
                        json.dumps(problem_data["data"]["function"]),
                        json.dumps(problem_data["data"]["names_x"]),
                        json.dumps(problem_data["data"]["names_y"])
                    )
                )
            elif problem_type == "Задача о назначениях":
                self.cursor.execute(
                    """INSERT INTO assignment_problems 
                    (id, name, problem_text, costs_json, names_x_json, names_y_json)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        problem_data["id"],
                        problem_data["name"],
                        problem_text,
                        json.dumps(problem_data["data"]["costs"]),
                        json.dumps(problem_data["data"]["names_x"]),
                        json.dumps(problem_data["data"]["names_y"])
                    )
                )
            elif problem_type == "Транспортная задача":
                self.cursor.execute(
                    """INSERT INTO transport_problems 
                    (id, name, problem_text, costs_json, supply_json, demand_json, names_x_json, names_y_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        problem_data["id"],
                        problem_data["name"],
                        problem_text,
                        json.dumps(problem_data["data"]["costs"]),
                        json.dumps(problem_data["data"]["supply"]),
                        json.dumps(problem_data["data"]["demand"]),
                        json.dumps(problem_data["data"]["names_x"]),
                        json.dumps(problem_data["data"]["names_y"])
                    )
                )
            elif problem_type == "Многопродуктовая транспортная задача":
                self.cursor.execute(
                    """INSERT INTO multi_transport_problems 
                    (id, name, problem_text, costs_json, supply_json, demand_json)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        problem_data["id"],
                        problem_data["name"],
                        problem_text,
                        json.dumps(problem_data["data"]["costs"]),
                        json.dumps(problem_data["data"]["supply"]),
                        json.dumps(problem_data["data"]["demand"])
                    )
                )
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def read_problem(self, problem_id: int, problem_type: str) -> Optional[Dict[str, Any]]:
        table_name = self._get_table_name(problem_type)
        if not table_name:
            return None

        try:
            if problem_type == "ЗЛП":
                self.cursor.execute(
                    """SELECT name, problem_text, problem_type, costs_json, constraints_json, 
                    signs_json, function_json, names_x_json, names_y_json
                    FROM linear_programming_problems WHERE id = ?""",
                    (problem_id,)
                )
                row = self.cursor.fetchone()
                if not row:
                    return None
                
                name, problem_text, problem_type, costs, constraints, signs, function, names_x, names_y = row
                return {
                    "id": problem_id,
                    "name": name,
                    "problem_text": problem_text,
                    "problem_type": problem_type,
                    "costs": json.loads(costs),
                    "constraints": json.loads(constraints),
                    "signs": json.loads(signs),
                    "function": json.loads(function),
                    "names_x": json.loads(names_x),
                    "names_y": json.loads(names_y)
                }
            elif problem_type == "Задача о назначениях":
                self.cursor.execute(
                    """SELECT name, problem_text, costs_json, names_x_json, names_y_json
                    FROM assignment_problems WHERE id = ?""",
                    (problem_id,)
                )
                row = self.cursor.fetchone()
                if not row:
                    return None
                
                name, problem_text, costs, names_x, names_y = row
                return {
                    "id": problem_id,
                    "name": name,
                    "problem_text": problem_text,
                    "costs": json.loads(costs),
                    "names_x": json.loads(names_x),
                    "names_y": json.loads(names_y)
                }
            elif problem_type == "Транспортная задача":
                self.cursor.execute(
                    """SELECT name, problem_text, costs_json, supply_json, demand_json, names_x_json, names_y_json
                    FROM transport_problems WHERE id = ?""",
                    (problem_id,)
                )
                row = self.cursor.fetchone()
                if not row:
                    return None
                
                name, problem_text, costs, supply, demand, names_x, names_y = row
                return {
                    "id": problem_id,
                    "name": name,
                    "problem_text": problem_text,
                    "costs": json.loads(costs),
                    "supply": json.loads(supply),
                    "demand": json.loads(demand),
                    "names_x": json.loads(names_x),
                    "names_y": json.loads(names_y)
                }
            elif problem_type == "Многопродуктовая транспортная задача":
                self.cursor.execute(
                    """SELECT name, problem_text, costs_json, supply_json, demand_json
                    FROM multi_transport_problems WHERE id = ?""",
                    (problem_id,)
                )
                row = self.cursor.fetchone()
                if not row:
                    return None
                
                name, problem_text, costs, supply, demand = row
                return {
                    "id": problem_id,
                    "name": name,
                    "problem_text": problem_text,
                    "costs": json.loads(costs),
                    "supply": json.loads(supply),
                    "demand": json.loads(demand)
                }
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def update_problem(self, problem_data: Dict[str, Any], problem_text: str = "") -> bool:
        problem_type = problem_data.get("type")
        if not problem_type:
            return False

        table_name = self._get_table_name(problem_type)
        if not table_name:
            return False

        try:
            if problem_type == "ЗЛП":
                self.cursor.execute(
                    """UPDATE linear_programming_problems 
                    SET name = ?, problem_text = ?, problem_type = ?, costs_json = ?, 
                    constraints_json = ?, signs_json = ?, function_json = ?, 
                    names_x_json = ?, names_y_json = ?
                    WHERE id = ?""",
                    (
                        problem_data["name"],
                        problem_text,
                        problem_data["data"]["problem_type"],
                        json.dumps(problem_data["data"]["costs"]),
                        json.dumps(problem_data["data"]["constraints"]),
                        json.dumps(problem_data["data"]["signs"]),
                        json.dumps(problem_data["data"]["function"]),
                        json.dumps(problem_data["data"]["names_x"]),
                        json.dumps(problem_data["data"]["names_y"]),
                        problem_data["id"]
                    )
                )
            elif problem_type == "Задача о назначениях":
                self.cursor.execute(
                    """UPDATE assignment_problems 
                    SET name = ?, problem_text = ?, costs_json = ?, names_x_json = ?, names_y_json = ?
                    WHERE id = ?""",
                    (
                        problem_data["name"],
                        problem_text,
                        json.dumps(problem_data["data"]["costs"]),
                        json.dumps(problem_data["data"]["names_x"]),
                        json.dumps(problem_data["data"]["names_y"]),
                        problem_data["id"]
                    )
                )
            elif problem_type == "Транспортная задача":
                self.cursor.execute(
                    """UPDATE transport_problems 
                    SET name = ?, problem_text = ?, costs_json = ?, supply_json = ?, 
                    demand_json = ?, names_x_json = ?, names_y_json = ?
                    WHERE id = ?""",
                    (
                        problem_data["name"],
                        problem_text,
                        json.dumps(problem_data["data"]["costs"]),
                        json.dumps(problem_data["data"]["supply"]),
                        json.dumps(problem_data["data"]["demand"]),
                        json.dumps(problem_data["data"]["names_x"]),
                        json.dumps(problem_data["data"]["names_y"]),
                        problem_data["id"]
                    )
                )
            elif problem_type == "Многопродуктовая транспортная задача":
                self.cursor.execute(
                    """UPDATE multi_transport_problems 
                    SET name = ?, problem_text = ?, costs_json = ?, supply_json = ?, demand_json = ?
                    WHERE id = ?""",
                    (
                        problem_data["name"],
                        problem_text,
                        json.dumps(problem_data["data"]["costs"]),
                        json.dumps(problem_data["data"]["supply"]),
                        json.dumps(problem_data["data"]["demand"]),
                        problem_data["id"]
                    )
                )
            
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def delete_problem(self, problem_id: int, problem_type: str) -> bool:
        table_name = self._get_table_name(problem_type)
        if not table_name:
            return False

        try:
            self.cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (problem_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def get_all_problems(self, problem_type: str) -> List[Dict[str, Any]]:
        table_name = self._get_table_name(problem_type)
        if not table_name:
            return []

        try:
            self.cursor.execute(f"SELECT id, name, problem_text FROM {table_name}")
            problems = []
            for problem_id, name, problem_text in self.cursor.fetchall():
                problem = self.read_problem(problem_id, problem_type)
                if problem:
                    problems.append(problem)
            return problems
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()