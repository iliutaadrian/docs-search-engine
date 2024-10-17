from search.fulltext_search import init as init_fulltext, search as search_fulltext
from search.tfidf_search import init as init_tfidf, search as search_tfidf
from search.bm25_search import init as init_bm25, search as search_bm25
from search.openai_search import init as init_openai, search as search_openai
from search.bert_search import init as init_bert, search as search_bert
from search.sentence_transformers_search import init as init_sentence_transformers, search as search_sentence_transformers
from search.hybrid_search import search as hybrid_search

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

