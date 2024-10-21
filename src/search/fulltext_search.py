import os
import sqlite3
import re
from config.config import DB_PATH

def init(documents):
    pass

def prepare_fts_query(query):
    clean_query = '" AND "'.join(query.split())
    return '"' + clean_query + '"'

def search(query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT 
            path, 
            highlight(documents, 1, '<mark>', '</mark>') AS highlighted_name,
            snippet(documents, 2, '<mark>', '</mark>', '...', 10) AS content_snippet,
            content,
            original_content,
            highlight(documents, 2, '<mark>', '</mark>') AS highlighted_content,
            length(original_content) AS content_length
        FROM documents 
        WHERE documents MATCH ?
    """, (prepare_fts_query(query),))
    
    results = c.fetchall()
    conn.close()
    
    final_results = []
    for result in results:
        path, highlighted_name, content_snippet, content, original_content, highlighted_content, content_length = result
        occurrence_count = highlighted_content.count('<mark>')
        final_results.append({
            "path": path,
            "highlighted_name": highlighted_name,
            "content_snippet": content_snippet,
            "content": content,
            "original_content": original_content,
            "highlighted_content": highlighted_content,
            "content_length": content_length,
            "relevance_score": occurrence_count
        })
    
    final_results.sort(key=lambda x: x['relevance_score'], reverse=True)
    return final_results
