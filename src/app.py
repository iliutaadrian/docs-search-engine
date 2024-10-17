from flask import Flask, request, jsonify, render_template
from document_processor import init_processor
from search.fulltext_search import init as init_fulltext, search as search_fulltext
from search.tfidf_search import init as init_tfidf, search as search_tfidf
from search.bm25_search import init as init_bm25, search as search_bm25
from search.openai_search import init as init_openai, search as search_openai
from search.bert_search import init as init_bert, search as search_bert
from search.sentence_transformers_search import init as init_sentence_transformers, search as search_sentence_transformers
from search.hybrid_search import search as hybrid_search
from llm import init_llm, generate_ai_response
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
    
    return jsonify(response)

def perform_search(query, aggregation_method, syntactic_methods, semantic_methods):
    all_methods = syntactic_methods + semantic_methods
    
    if aggregation_method == 'single' and len(all_methods) == 1:
        search_function = get_search_function(all_methods[0])
        return search_function(query)
    elif aggregation_method in ['linear', 'rank_fusion', 'cascade']:
        return hybrid_search(query, methods=all_methods, combination_method=aggregation_method)
    else:
        # Default to fulltext search if no valid method is specified
        return search_fulltext(query)

def get_search_function(method):
    search_functions = {
        'fulltext': search_fulltext,
        'tfidf': search_tfidf,
        'bm25': search_bm25,
        'openai': search_openai,
        'bert': search_bert,
        'sentence_transformers': search_sentence_transformers
    }
    return search_functions.get(method.lower(), search_fulltext)

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

    init_fulltext(documents)
    init_tfidf(documents)
    init_bm25(documents)
    init_openai(documents)

    init_bert(documents)
    init_sentence_transformers(documents)
    init_llm()
    init_typeahead(documents)
    
    app.run(debug=True, host='0.0.0.0')
