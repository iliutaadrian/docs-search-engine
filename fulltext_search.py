import os
import sqlite3
from typing import List, Dict
from config import DB_PATH

def search_fulltext(query: str) -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    terms = query.split()
    fts_query = ' AND '.join(terms)
    
    c.execute("""
        SELECT 
            path, 
            snippet(documents, 0, '<b>', '</b>', '...', 50) AS name_snippet,
            snippet(documents, 1, '<b>', '</b>', '...', 100) AS content_snippet,
            content,
            length(content) AS content_length,
            highlight(documents, 1, '<mark>', '</mark>') AS highlighted_content
        FROM documents 
        WHERE documents MATCH ?
        ORDER BY rank
    """, (fts_query,))
    
    results = c.fetchall()
    conn.close()
    
    final_results = []
    for result in results:
        path, name_snippet, content_snippet, full_content, content_length, highlighted_content = result
        occurrence_count = highlighted_content.count('<mark>')
        final_results.append({
            "path": path,
            "name": os.path.basename(path),
            "content_snippet": content_snippet,
            "content_length": content_length,
            "full_content": full_content,
            "highlighted_content": highlighted_content,
            "occurrence_count": occurrence_count
        })
    
    final_results.sort(key=lambda x: x['occurrence_count'], reverse=True)
    return final_results
