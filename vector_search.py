# vector_search.py

import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = None
documents = None
document_vectors = None

def init_vector_search(docs):
    global vectorizer, documents, document_vectors
    documents = docs
    
    if not documents:
        print("Warning: No documents provided for vector search initialization.")
        return

    # Check if there's any non-empty content
    non_empty_docs = [doc for doc in documents if doc['content'].strip()]
    if not non_empty_docs:
        print("Warning: All documents are empty or contain only whitespace.")
        return

    vectorizer = TfidfVectorizer(stop_words='english', min_df=1, max_df=0.9)
    
    try:
        document_vectors = vectorizer.fit_transform([doc['content'] for doc in non_empty_docs])
        print("Vector search initialized with {} documents.".format(len(non_empty_docs)))
    except ValueError as e:
        print("Error initializing vector search: {}".format(str(e)))
        print("This might be due to all words being considered stop words or other preprocessing issues.")
        vectorizer = None
        document_vectors = None

def search_vector(query, k=5):
    if vectorizer is None or document_vectors is None:
        print("Vector search is not properly initialized. Returning empty results.")
        return []

    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, document_vectors).flatten()
    top_k_indices = similarities.argsort()[-k:][::-1]

    results = []
    for idx in top_k_indices:
        doc = documents[idx]
        full_content = doc['content']
        content_length = len(full_content)
        
        # Create a simple content snippet (first 100 characters)
        content_snippet = full_content[:100] + "..." if len(full_content) > 100 else full_content
        
        # Create a simple highlighted content (bold the query terms)
        highlighted_content = full_content
        for term in query.split():
            highlighted_content = highlighted_content.replace(term, "<b>{}</b>".format(term))
        
        # Count occurrences (case-insensitive)
        occurrence_count = sum(full_content.lower().count(term.lower()) for term in query.split())

        results.append({
            "path": doc["path"],
            "name": os.path.basename(doc["path"]),
            "content_snippet": content_snippet,
            "content_length": content_length,
            "full_content": full_content,
            "highlighted_content": highlighted_content,
            "occurrence_count": occurrence_count,
            "similarity_score": float(similarities[idx])
        })

    results.sort(key=lambda x: x['similarity_score'], reverse=True)
    return results
