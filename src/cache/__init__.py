from config.config import DATA_FOLDER
from typing import List, Dict, Optional
import json
import os
import os
import sqlite3

CACHE_DB_PATH = os.path.join(DATA_FOLDER, 'cache.db')

def init_cache_module():
    create_table()

def get_db_connection():
    return sqlite3.connect(CACHE_DB_PATH)

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cache (
            query TEXT PRIMARY KEY,
            search_results TEXT,
            ai_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def store_results(query: str, search_results: List[Dict], ai_response: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO cache (query, search_results, ai_response)
        VALUES (?, ?, ?)
    ''', (query, json.dumps(search_results), ai_response))
    conn.commit()
    conn.close()

def get_results(query: str) -> Optional[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT search_results, ai_response FROM cache WHERE query = ?', (query,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'search_results': json.loads(result[0]),
            'ai_response': result[1]
        }
    return None

def clear_cache():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cache')
    conn.commit()
    conn.close()

