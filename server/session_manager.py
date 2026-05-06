import sqlite3
from datetime import datetime
import os

class SessionManager:
    """
    Manages the 'Neural Ledger' - a local database for tracking 
    BCI performance, session metadata, and model versions.
    """
    def __init__(self, db_path="/root/Coding/projects/project-cerebrum/docs/research/neural_ledger.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Sessions Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                task_type TEXT,
                trial_count INTEGER,
                data_path TEXT
            )
        ''')
        
        # Models Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                accuracy REAL,
                weights_path TEXT,
                parent_session_id INTEGER,
                FOREIGN KEY(parent_session_id) REFERENCES sessions(id)
            )
        ''')
        conn.commit()
        conn.close()

    def log_session(self, task_type, trial_count, data_path):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('INSERT INTO sessions (timestamp, task_type, trial_count, data_path) VALUES (?, ?, ?, ?)',
                       (timestamp, task_type, trial_count, data_path))
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        print(f"[Ledger] Session {session_id} logged.")
        return session_id

    def log_model(self, accuracy, weights_path, session_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('INSERT INTO models (timestamp, accuracy, weights_path, parent_session_id) VALUES (?, ?, ?, ?)',
                       (timestamp, accuracy, weights_path, session_id))
        conn.commit()
        conn.close()
        print(f"[Ledger] Model with {accuracy*100:.2f}% accuracy logged.")

if __name__ == "__main__":
    # Test Ledger
    sm = SessionManager()
    print("Neural Ledger initialized and ready.")
