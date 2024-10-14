from flask import Flask, request, jsonify, render_template
from document_processor import init_processor
from fulltext_search import search_fulltext
from vector_search import init_vector_search, search_vector
from config import DOCS_FOLDER

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    mode = request.args.get('mode', 'fulltext')

    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    if mode == 'fulltext':
        results = search_fulltext(query)
    elif mode == 'vector':
        results = search_vector(query)
    elif mode == 'hybrid':
        fulltext_results = search_fulltext(query)
        vector_results = search_vector(query)
        results = combine_results(fulltext_results, vector_results)
    else:
        return jsonify({"error": "Invalid search mode"}), 400
    
    return jsonify(results)

def combine_results(fulltext_results, vector_results):
    combined = fulltext_results + vector_results
    combined.sort(key=lambda x: x.get('occurrence_count', 0) + x.get('similarity_score', 0), reverse=True)
    return combined[:10] 


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    documents = init_processor()

    init_vector_search(documents)

    app.run(debug=True, host='0.0.0.0')
