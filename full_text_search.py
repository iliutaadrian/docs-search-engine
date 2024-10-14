import os
import sqlite3
import markdown
from PyPDF2 import PdfReader
from config import DB_PATH

def init_fulltext_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS documents USING fts5(path UNINDEXED, content)''')
    c.execute('''CREATE TABLE IF NOT EXISTS indexed_files (path TEXT PRIMARY KEY)''')
    conn.commit()
    conn.close()
    print(f"Fulltext database initialized at {DB_PATH}")

def is_file_indexed(conn, path):
    c = conn.cursor()
    c.execute("SELECT 1 FROM indexed_files WHERE path = ?", (path,))
    return c.fetchone() is not None

def index_documents(folder_path):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    indexed_count = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.md') or file.endswith('.pdf'):
                file_path = os.path.join(root, file)
                if not is_file_indexed(conn, file_path):
                    print(f"Indexing file: {file_path}")
                    content = extract_content(file_path)
                    c.execute("INSERT INTO documents (path, content) VALUES (?, ?)", (file_path, content))
                    c.execute("INSERT INTO indexed_files (path) VALUES (?)", (file_path,))
                    indexed_count += 1
                else:
                    print(f"Skipping already indexed file: {file_path}")
    conn.commit()
    conn.close()
    print(f"Indexed {indexed_count} new documents")

def extract_content(file_path):
    print(f"Extracting content from: {file_path}")
    if file_path.endswith('.md'):
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            html_content = markdown.markdown(md_content)
            return html_content
    elif file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            return ' '.join(page.extract_text() for page in reader.pages)

def fulltext_search(query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    terms = query.split()
    
    fts_query = ' OR '.join(terms)
    
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
