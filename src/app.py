from flask import Flask, request, jsonify, render_template

from document_processor import init_processor

from search.fulltext_search import init as init_fulltext, search as search_fulltext
from search.tfidf_search import init as init_tfidf, search as search_tfidf
from search.openai_search import init as init_openai, search as search_openai
from search.bert_search import init as init_bert, search as search_bert
from search.sentence_transformers_search import init as init_sentence_transformers, search as search_sentence_transformers

from config.config import DOCS_FOLDER

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    mode = request.args.get('mode', 'fulltext')

    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    if mode == 'fulltext':
        results = search_fulltext(query)
    elif mode == 'tfidf':
        results = search_tfidf(query)
    elif mode == 'openai':
        results = search_openai(query)
    elif mode == 'bert':
        results = search_bert(query)
    elif mode == 'sentence_transformers':
        results = search_sentence_transformers(query)
    elif mode == 'hybrid':
        fulltext_results = search_fulltext(query)
        vector_results = search_openai(query)  # You can change this to any other vector search method
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

    # init_fulltext(documents)
    # init_tfidf(documents)
    # init_openai(documents)
    init_bert(documents)
    # init_sentence_transformers(documents)
    
    app.run(debug=True, host='0.0.0.0')
