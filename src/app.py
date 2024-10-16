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

# Global variable to store all document titles for typeahead
all_titles = []

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    mode = request.args.get('mode', 'fulltext')
    options = json.loads(request.args.get('options', '[]'))

    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    search_function = get_search_function(mode)
    results = search_function(query)

    if 'popularity_rank' in options:
        results = apply_popularity_ranking(results)
    
    if 'ai_assist' in options:
        ai_response = generate_ai_response(query, results[:3])
        results = {
            "ai_response": ai_response.get('full_content', 'No response possible'),
            "search_results": results[:10]
        }
    
    return jsonify(results)

@app.route('/typeahead', methods=['GET'])
def typeahead():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])

    suggestions = [title for title in all_titles if query in title.lower()]
    return jsonify(suggestions[:10])  # Limit to 10 suggestions

@app.route('/')
def index():
    return render_template('index.html')

def get_search_function(mode):
    if mode == 'fulltext':
        return search_fulltext
    elif mode == 'tfidf':
        return search_tfidf
    elif mode == 'bm25':
        return search_bm25
    elif mode == 'openai':
        return search_openai
    elif mode == 'bert':
        return search_bert
    elif mode == 'sentence_transformers':
        return search_sentence_transformers
    elif mode in ['linear', 'rrf', 'cascade']:
        return lambda query: hybrid_search(query, methods=['fulltext', 'tfidf'], combination_method=mode)
    else:
        return search_fulltext  # Default to fulltext search

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
