import sqlite3
import os
from flask import request, jsonify
from config.config import DATA_FOLDER

AUTOCOMPLETE_DB_PATH = os.path.join(DATA_FOLDER, 'autocomplete.db')

def get_db_connection():
    conn = sqlite3.connect(AUTOCOMPLETE_DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")  # Use Write-Ahead Logging for better concurrency
    return conn

def init_autocomplete(documents):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create table with UNIQUE constraint on phrase
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY,
            phrase TEXT UNIQUE,
            frequency INTEGER
        )
    ''')
    
    # Create index on phrase column for faster lookups
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_prompts_phrase ON prompts(phrase)')
    
    conn.commit()
    conn.close()
    
    populate_autocomplete_from_documents(documents)

def add_or_update_prompt(phrases):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Use executemany for batch inserts
    cursor.executemany('''
        INSERT INTO prompts (phrase, frequency)
        VALUES (?, 1)
        ON CONFLICT(phrase) DO UPDATE SET frequency = frequency + 1
    ''', [(phrase,) for phrase in phrases])
    
    conn.commit()
    conn.close()

def get_autocomplete_suggestions(query, limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Use LIKE with an index for faster prefix matching
    cursor.execute('''
        SELECT phrase
        FROM prompts
        WHERE phrase LIKE ? || '%'
        ORDER BY frequency DESC, length(phrase) ASC
        LIMIT ?
    ''', (query.lower(), limit))
    
    results = cursor.fetchall()
    conn.close()
    
    return [result[0] for result in results]

def populate_autocomplete_from_documents(documents):
    batch_size = 1000
    phrases = []
    
    for doc in documents:
        words = doc['content'].lower().split()
        for i in range(len(words)):
            for j in range(i + 1, min(i + 6, len(words) + 1)):
                phrase = ' '.join(words[i:j])
                phrases.append(phrase)
                
                if len(phrases) >= batch_size:
                    add_or_update_prompt(phrases)
                    phrases = []
    
    if phrases:
        add_or_update_prompt(phrases)
