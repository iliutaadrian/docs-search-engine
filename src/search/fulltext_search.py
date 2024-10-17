import os
import sqlite3
import re
from config.config import DB_PATH

def init(documents):
    pass

def prepare_fts_query(query):
    clean_query = '" OR "'.join(query.split())
    return '"' + clean_query + '"'

def search(query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT 
            path, 
            highlight(documents, 0, '<mark>', '</mark>') AS highlighted_path,
            snippet(documents, 2, '<mark>', '</mark>', '...', 10) AS content_snippet,
            content,
            original_content,
            highlight(documents, 2, '<mark>', '</mark>') AS highlighted_content,
            length(original_content) AS content_length
        FROM documents 
        WHERE documents MATCH ?
        ORDER BY rank
    """, (prepare_fts_query(query),))
    
    results = c.fetchall()
    conn.close()
    
    final_results = []
    for result in results:
        path, highlighted_path, content_snippet, content, original_content, highlighted_content, content_length = result
        occurrence_count = highlighted_content.count('<mark>')
        final_results.append({
            "path": path,
            "highlighted_path": highlighted_path,
            "content_snippet": content_snippet,
            "content": content,
            "original_content": original_content,
            "highlighted_content": highlighted_content,
            "content_length": content_length,
            "occurrence_count": occurrence_count
        })
    
    final_results.sort(key=lambda x: x['occurrence_count'], reverse=True)
    return final_results
