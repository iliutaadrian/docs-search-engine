import os
import sqlite3
import re
from config.config import DB_PATH

def init(documents):
    pass

def search(query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    terms = preprocess_query(query)
    fts_query = construct_fts_query(terms)
    
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

def preprocess_query(query):
    terms = re.findall(r'"[^"]*"|\S+', query)
    
    # Remove quotes from phrases and handle hyphenated words
    processed_terms = []
    for term in terms:
        if term.startswith('"') and term.endswith('"'):
            processed_terms.append(term.strip('"'))
        elif '-' in term:
            processed_terms.append(f'"{term}"')  # Treat hyphenated words as phrases
        else:
            processed_terms.append(term)
    
    return processed_terms

def construct_fts_query(terms):
    # Construct the FTS query using the NEAR operator for phrases and AND for single words
    fts_parts = []
    for term in terms:
        if ' ' in term:
            # For phrases, use the NEAR operator with a small distance
            words = term.split()
            fts_parts.append(' NEAR/2 '.join(words))
        else:
            fts_parts.append(term)
    
    return ' AND '.join(fts_parts)
