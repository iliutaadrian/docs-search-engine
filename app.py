import os
import sqlite3
from flask import Flask, request, jsonify, render_template
import markdown
from PyPDF2 import PdfReader
from collections import defaultdict


app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('documents.db')
    c = conn.cursor()
    c.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS documents USING fts5(path, content)''')
    conn.commit()
    conn.close()

def index_documents(folder_path):
    conn = sqlite3.connect('documents.db')
    c = conn.cursor()

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.md') or file.endswith('.pdf'):
                file_path = os.path.join(root, file)
                content = extract_content(file_path)
                c.execute("INSERT INTO documents (path, content) VALUES (?, ?)", (file_path, content))

    conn.commit()
    conn.close()

def extract_content(file_path):
    if file_path.endswith('.md'):
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            html_content = markdown.markdown(md_content)
            return html_content
    elif file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            return ' '.join(page.extract_text() for page in reader.pages)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    conn = sqlite3.connect('documents.db')
    c = conn.cursor()

    # Modified query to return more content and a unique identifier
    c.execute("""
        SELECT 
            path, 
            snippet(documents, 0, '<b>', '</b>', '...', 50) AS name_snippet,
            snippet(documents, 1, '<b>', '</b>', '...', 200) AS content_snippet,
            length(content) AS content_length,
            substr(content, 1, 500) AS content_preview
        FROM documents 
        WHERE documents MATCH ? 
        ORDER BY rank
    """, (query,))
    
    results = c.fetchall()
    conn.close()
    
    # Group results by file path
    grouped_results = defaultdict(list)
    for result in results:
        path, name_snippet, content_snippet, content_length, content_preview = result
        grouped_results[path].append({
            "path": path,
            "name": os.path.basename(path),
            "name_snippet": name_snippet,
            "content_snippet": content_snippet,
            "content_length": content_length,
            "content_preview": content_preview
        })
    
    # Prepare the final result
    final_results = []
    for path, group in grouped_results.items():
        final_results.append({
            "path": path,
            "name": os.path.basename(path),
            "occurrences": len(group),
            "details": group
        })
    
    return jsonify(final_results)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    index_documents('../docs')  
    app.run(debug=True)
