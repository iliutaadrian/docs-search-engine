from flask import Flask, request, jsonify, render_template

from search import init_search_module
from search.search_module import perform_search

from cache import init_cache_module, store_results, get_results

from llm.llm_module import init_llm, generate_ai_response
from document_processor import init_processor
from config.config import DOCS_FOLDER
import json

app = Flask(__name__)

all_titles = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    aggregation_method = request.args.get('aggregationMethod', 'single')
    syntactic_methods = json.loads(request.args.get('syntacticMethods', '[]'))
    semantic_methods = json.loads(request.args.get('semanticMethods', '[]'))
    options = json.loads(request.args.get('options', '[]'))

    if not query:
        return jsonify({"error": "No query provided"}), 400

    search_methods = syntactic_methods + semantic_methods

    if 'caching' in options:
        cached_results = get_results(query, aggregation_method, search_methods, options)
        if cached_results:
            return jsonify(cached_results)

    results = perform_search(query, aggregation_method, syntactic_methods, semantic_methods)
    
    if 'popularity_rank' in options:
        results = apply_popularity_ranking(results)
    
    ai_response = None
    if 'ai_assist' in options:
        ai_response = generate_ai_response(query, results[:3])
    
    response = {
        "search_results": results[:10],
        "ai_response": ai_response.get('full_content', '') if ai_response else None
    }

    if 'caching' in options:
        store_results(query, aggregation_method, search_methods, options, results, response.get('ai_response'))
    
    return jsonify(response)

@app.route('/typeahead', methods=['GET'])
def typeahead():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    suggestions = [title for title in all_titles if query in title.lower()]
    return jsonify(suggestions[:10])  # Limit to 10 suggestions

def apply_popularity_ranking(results):
    # This is a placeholder function. In a real-world scenario, you would implement
    # actual popularity ranking based on user behavior, document views, etc.
    return sorted(results, key=lambda x: x.get('popularity', 0), reverse=True)

def init_typeahead(documents):
    global all_titles
    all_titles = [doc['path'].split('/')[-1] for doc in documents]

if __name__ == '__main__':
    documents = init_processor()

    init_search_module(documents)
    
    init_cache_module()

    init_llm()
    init_typeahead(documents)
    
    app.run(debug=True, host='0.0.0.0')
