import os
import sqlite3
import markdown
from PyPDF2 import PdfReader
from config.config import DB_PATH, DOCS_FOLDER

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS documents USING fts5(path UNINDEXED, content)''')
    c.execute('''CREATE TABLE IF NOT EXISTS indexed_files (path TEXT PRIMARY KEY)''')
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

def is_file_indexed(conn, path):
    c = conn.cursor()
    c.execute("SELECT 1 FROM indexed_files WHERE path = ?", (path,))
    return c.fetchone() is not None

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
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

def index_documents():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    indexed_count = 0
    for root, _, files in os.walk(DOCS_FOLDER):
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

def get_all_documents():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT path, content FROM documents")
    documents = [{"path": path, "content": content} for path, content in c.fetchall()]
    conn.close()
    print(f"Fetched {len(documents)} documents from the database")
    return documents

def init_processor():
    init_db()
    index_documents()
    return get_all_documents()
