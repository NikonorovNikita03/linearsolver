import sqlite3
import json

class ProblemDatabase:
    def __init__(self, db_name='data.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                name TEXT,
                data TEXT
            )
        ''')
        self.conn.commit()

    def add_item(self, item_type, name, data):
        data_str = json.dumps(data)
        self.cursor.execute('''
            INSERT INTO data_items (type, name, data)
            VALUES (?, ?, ?)
        ''', (item_type, name, data_str))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_item(self, item_id):
        self.cursor.execute('SELECT * FROM data_items WHERE id = ?', (item_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'type': row[1],
                'name': row[2],
                'data': json.loads(row[3])
            }
        return None

    def update_item(self, item_id, item_type=None, name=None, data=None):
        updates = []
        params = []
        
        if item_type is not None:
            updates.append("type = ?")
            params.append(item_type)
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if data is not None:
            updates.append("data = ?")
            params.append(json.dumps(data))
            
        if not updates:
            return False
            
        params.append(item_id)
        query = f"UPDATE data_items SET {', '.join(updates)} WHERE id = ?"
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_item(self, item_id):
        self.cursor.execute('DELETE FROM data_items WHERE id = ?', (item_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_all_items(self):
        self.cursor.execute('SELECT * FROM data_items')
        return [
            {
                'id': row[0],
                'type': row[1],
                'name': row[2],
                'data': json.loads(row[3])
            } for row in self.cursor.fetchall()
        ]

    def __del__(self):
        self.conn.close()