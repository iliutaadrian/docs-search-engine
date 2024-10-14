from flask import Flask, request, jsonify, render_template
from full_text_search import init_fulltext_db, index_documents, fulltext_search
from config import DOCS_FOLDER

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    mode = request.args.get('mode', 'fulltext')

    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    if mode == 'fulltext':
        results = fulltext_search(query)
        return jsonify(results)
    elif mode in ['semantic', 'vector', 'hybrid']:
        return jsonify({"error": f"{mode.capitalize()} search not implemented"}), 501
    else:
        return jsonify({"error": "Invalid search mode"}), 400

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # full text search
    init_fulltext_db()
    index_documents(DOCS_FOLDER)


    app.run(debug=True, host='0.0.0.0')
