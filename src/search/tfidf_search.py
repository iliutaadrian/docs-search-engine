import os
import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
from config.config import DATA_FOLDER
import re


documents = None
tfidf_vectorizer = None
faiss_index = None
document_paths = None
document_names = None
FAISS_INDEX_PATH = os.path.join(DATA_FOLDER, "faiss_tfidf_index")

def init(docs):
    global documents, tfidf_vectorizer, faiss_index, document_paths, document_names
    documents = [doc['content'] for doc in docs]
    document_paths = [doc['path'] for doc in docs]
    document_names = [doc['name'] for doc in docs]
    
    # Combine document content with its name for TF-IDF vectorization
    combined_docs = [f"{name} {content}" for name, content in zip(document_names, documents)]
    
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
    
    query_vector = tfidf_vectorizer.transform([query]).toarray().astype('float32')
    
    # Perform the search
    scores, indices = faiss_index.search(query_vector, k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        full_content = documents[idx]
        content_length = len(full_content)
        content_snippet = full_content[:100] + "..." if len(full_content) > 100 else full_content
        highlighted_content = highlight_terms(full_content, query)
        highlighted_name = highlight_terms(document_names[idx], query)
        
        relevance_score = float(scores[0][i])
        
        results.append({
            "path": document_paths[idx],
            "highlighted_name": highlighted_name,
            "content_snippet": content_snippet,
            "content_length": content_length,
            "full_content": full_content,
            "highlighted_content": highlighted_content,
            "relevance_score": relevance_score,
        })
    
    return results

def highlight_terms(text, query):
    highlighted = text
    for term in query.split():
        # Create a regular expression pattern for case-insensitive matching
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        
        # Use the pattern to replace all occurrences with the highlighted version
        highlighted = pattern.sub(lambda m: f"<mark>{m.group()}</mark>", highlighted)
    
    return highlighted
