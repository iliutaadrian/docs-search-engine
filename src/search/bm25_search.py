import os
import numpy as np
import faiss
import re
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import CountVectorizer
from config.config import DATA_FOLDER

documents = None
bm25 = None
faiss_index = None
document_paths = None
document_names = None
FAISS_INDEX_PATH = os.path.join(DATA_FOLDER, "faiss_bm25_index")

def init(docs):
    global documents, bm25, faiss_index, document_paths, document_names

    documents = [doc['content'] for doc in docs]
    document_paths = [doc['path'] for doc in docs]
    document_names = [doc['name'] for doc in docs]
    
    # Combine document content with its name for BM25 calculation
    combined_docs = [f"{name} {content}" for name, content in zip(document_names, documents)]
    
    # Tokenize the documents
    tokenized_docs = [doc.split() for doc in combined_docs]
    
    # Create BM25 object
    bm25 = BM25Okapi(tokenized_docs)
    
    # Calculate BM25 scores for all documents
    bm25_scores = np.array([bm25.get_scores(doc) for doc in tokenized_docs])
    
    # Create and train the FAISS index
    dimension = bm25_scores.shape[1]
    faiss_index = faiss.IndexFlatIP(dimension)  # Inner Product Index
    faiss_index.add(bm25_scores.astype('float32'))
    
    # Save the FAISS index
    faiss.write_index(faiss_index, FAISS_INDEX_PATH)
    
    print(f"BM25 FAISS search initialized with {len(documents)} documents.")


def search(query, k=5):
    if faiss_index is None or bm25 is None:
        raise ValueError("BM25 FAISS search not initialized. Call init() first.")
    
    # Tokenize the query
    tokenized_query = query.split()
    
    # Calculate BM25 scores for the query
    query_scores = bm25.get_scores(tokenized_query)
    
    # Perform the search
    scores, indices = faiss_index.search(query_scores.reshape(1, -1).astype('float32'), k)
    
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
