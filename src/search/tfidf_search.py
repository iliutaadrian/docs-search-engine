import os
import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
from config.config import DATA_FOLDER
import re

from search.syntactic_helper import clear_text, find_snippet, highlight_terms

documents = None
tfidf_vectorizer = None
faiss_index = None
document_paths = None
document_names = None
FAISS_INDEX_PATH = os.path.join(DATA_FOLDER, "faiss_tfidf_index")

def init(docs):
    global documents, tfidf_vectorizer, faiss_index, document_paths, document_names
    documents = docs 
    document_paths = [doc['path'] for doc in docs]
    document_names = [doc['name'] for doc in docs]
    
    # Combine document content with its name for TF-IDF vectorization
    combined_docs = [f"{doc['name']} {doc['content']}" for doc in docs]
    
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(combined_docs)
    
    # Convert sparse matrix to dense numpy array
    dense_matrix = tfidf_matrix.toarray().astype('float32')
    
    # Create and train the FAISS index
    dimension = dense_matrix.shape[1]
    faiss_index = faiss.IndexFlatIP(dimension)  # Inner Product Index
    faiss_index.add(dense_matrix)
    
    # Save the FAISS index
    faiss.write_index(faiss_index, FAISS_INDEX_PATH)
    
    print(f"TF-IDF FAISS search initialized with {len(documents)} documents.")

def search(query, k=5):
    if faiss_index is None or tfidf_vectorizer is None:
        raise ValueError("TF-IDF FAISS search not initialized. Call init() first.")
    
    query = clear_text(query)
    query_vector = tfidf_vectorizer.transform([query]).toarray().astype('float32')
    
    # Perform the search
    scores, indices = faiss_index.search(query_vector, k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        doc = documents[idx]
        content = doc['content']
        original_content = doc['original_content']
        content_length = len(original_content)
        
        # Find the content snippet where the term appears
        content_snippet = find_snippet(content, query)
        
        highlighted_content = highlight_terms(original_content, query)
        highlighted_name = highlight_terms(doc['name'], query)
        
        relevance_score = float(scores[0][i])
        
        results.append({
            "path": doc['path'],
            "highlighted_name": highlighted_name,
            "content_snippet": content_snippet,
            "content": content,
            "original_content": original_content,
            "highlighted_content": highlighted_content,
            "content_length": content_length,
            "relevance_score": relevance_score,
        })
    
    return results
