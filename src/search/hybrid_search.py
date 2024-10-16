from search.fulltext_search import init as init_fulltext, search as search_fulltext
from search.tfidf_search import init as init_tfidf, search as search_tfidf
from search.bm25_search import init as init_bm25, search as search_bm25
from search.openai_search import init as init_openai, search as search_openai
from search.bert_search import init as init_bert, search as search_bert
from search.sentence_transformers_search import init as init_sentence_transformers, search as search_sentence_transformers
from collections import defaultdict

def search(query, methods=['fulltext', 'openai', 'bert'], weights=None, combination_method='linear'):
    all_results = {}
    for method in methods:
        if method == 'fulltext':
            all_results[method] = search_fulltext(query)
        elif method == 'openai':
            all_results[method] = search_openai(query)
        elif method == 'bert':
            all_results[method] = search_bert(query)
        elif method == 'tfidf':
            all_results[method] = search_tfidf(query)
        elif method == 'bm25':
            all_results[method] = search_bm25(query)
        elif method == 'sentence_transformers':
            all_results[method] = search_sentence_transformers(query)

    if combination_method == 'rank_fusion':
        return rank_fusion(all_results)
    elif combination_method == 'cascade':
        return cascade_search(all_results, methods)
    elif combination_method == 'linear':
        return linear_combination(all_results, weights)
    else:
        raise ValueError(f"Unknown combination method: {combination_method}")


def linear_combination(results, weights=None):
    if weights is None:
        weights = {method: 1/len(results) for method in results}
    
    combined_scores = defaultdict(float)
    all_docs = {}
    
    for method, method_results in results.items():
        for rank, result in enumerate(method_results):
            doc_id = result['path']
            all_docs[doc_id] = result
            
            score = (len(method_results) - rank) * result['occurrence_count']
            combined_scores[doc_id] += score * weights[method]
    
    
    max_score = max(combined_scores.values()) if combined_scores else 1
    for doc_id in combined_scores:
        combined_scores[doc_id] /= max_score
    
    
    sorted_results = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    
    
    final_results = []
    for doc_id, combined_score in sorted_results:
        result = all_docs[doc_id].copy()
        result['occurrence_count'] = int(combined_score * 100)  
        final_results.append(result)
    
    return final_results

def rank_fusion(results, k=60):
    fused_scores = defaultdict(float)
    all_docs = {}
    
    for method, method_results in results.items():
        for rank, result in enumerate(method_results, start=1):
            doc_id = result['path']
            all_docs[doc_id] = result
            fused_scores[doc_id] += 1 / (rank + k)
    
    
    max_score = max(fused_scores.values()) if fused_scores else 1
    for doc_id in fused_scores:
        fused_scores[doc_id] /= max_score
    
    
    sorted_results = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    
    
    final_results = []
    for doc_id, fused_score in sorted_results:
        result = all_docs[doc_id].copy()
        result['occurrence_count'] = int(fused_score * 100)  
        final_results.append(result)
    
    return final_results

def cascade_search(results, methods, threshold=0.5):
    all_docs = {}
    final_results = []
    
    for method in methods:
        method_results = results[method]
        for result in method_results:
            doc_id = result['path']
            all_docs[doc_id] = result
            
            # Normalize the score based on occurrence_count
            # Assuming occurrence_count is in the range 0-100
            score = result['occurrence_count'] / 100.0
            
            if score >= threshold:
                if doc_id not in [r['path'] for r in final_results]:
                    final_results.append(result)
            
        if final_results:
            break  # Stop if we have results above the threshold
    
    # If no results meet the threshold, return top results from the last method
    if not final_results and method_results:
        final_results = method_results[:5]  # Return top 5 results
    
    # Sort the final results by occurrence_count
    final_results.sort(key=lambda x: x['occurrence_count'], reverse=True)
    
    return final_results
