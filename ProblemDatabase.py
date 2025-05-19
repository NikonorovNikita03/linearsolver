import sqlite3
import json

class ProblemDatabase():
    def __init__(self, db_path: str = "optimization_problems.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Create the necessary tables in the database."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY,
            type TEXT NOT NULL,
            name TEXT NOT NULL,
            size_x INTEGER,
            size_y INTEGER,
            UNIQUE(type, name)
        )
        """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transport_problems (
            problem_id INTEGER PRIMARY KEY,
            costs TEXT NOT NULL,
            supply TEXT NOT NULL,
            demand TEXT NOT NULL,
            FOREIGN KEY (problem_id) REFERENCES problems (id)
        )
        """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignment_problems (
            problem_id INTEGER PRIMARY KEY,
            costs TEXT NOT NULL,
            FOREIGN KEY (problem_id) REFERENCES problems (id)
        )
        """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS multi_product_transport_problems (
            problem_id INTEGER PRIMARY KEY,
            costs TEXT NOT NULL,
            supply TEXT NOT NULL,
            demand TEXT NOT NULL,
            FOREIGN KEY (problem_id) REFERENCES problems (id)
        )
        """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS linear_programming_problems (
            problem_id INTEGER PRIMARY KEY,
            problem_type TEXT NOT NULL,
            costs TEXT NOT NULL,
            constraints TEXT NOT NULL,
            signs TEXT NOT NULL,
            function TEXT NOT NULL,
            FOREIGN KEY (problem_id) REFERENCES problems (id)
        )
        """)
        
        self.conn.commit()