import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from config.config import DATA_FOLDER
from search.syntactic_helper import find_snippet, highlight_terms

model = None
documents = None
faiss_index = None
FAISS_INDEX_PATH = os.path.join(DATA_FOLDER, "faiss_sentence_transformer_index")

def init(docs):
    global model, documents, faiss_index
    documents = docs
    
    print("Initializing Sentence Transformer model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    if os.path.exists(FAISS_INDEX_PATH):
        print("Loading existing Sentence Transformer FAISS index...")
        try:
            faiss_index = faiss.read_index(FAISS_INDEX_PATH)
            print(f"Successfully loaded FAISS index with {faiss_index.ntotal} vectors.")
        except Exception as e:
            print(f"Error loading existing Sentence Transformer index: {e}")
            print("Creating new Sentence Transformer FAISS index...")
            create_new_index()
    else:
        print("Creating new Sentence Transformer FAISS index...")
        create_new_index()

def create_new_index():
    global faiss_index
    print("Generating embeddings for documents using Sentence Transformer...")
    document_embeddings = model.encode([doc['content'] for doc in documents], show_progress_bar=True)
    
    print("Creating FAISS index for fast similarity search...")
    dimension = document_embeddings.shape[1]
    faiss_index = faiss.IndexFlatIP(dimension)
    faiss_index.add(document_embeddings.astype('float32'))
    
    print("Saving Sentence Transformer FAISS index...")
    faiss.write_index(faiss_index, FAISS_INDEX_PATH)
    
    print(f"Sentence Transformer vector search initialized with {len(documents)} documents.")

def search(query, k=5):
    if faiss_index is None:
        raise ValueError("Sentence Transformer vector store not initialized. Call init() first.")
    
    print(f"Performing similarity search with Sentence Transformer for query: '{query}'")
    query_embedding = model.encode([query]).astype('float32')
    
    print(f"Searching for top {k*2} similar documents...")  # Search for more results initially
    distances, indices = faiss_index.search(query_embedding, k*2)
    
    print(f"Processing top {k*2} results from Sentence Transformer similarity search...")
    unique_results = {}
    for i, idx in enumerate(indices[0]):
        doc = documents[idx]
        content = doc['content']
        original_content = doc['original_content']
        content_length = len(original_content)
        
        # Find the content snippet where the term appears
        content_snippet = find_snippet(content, query)
        
        highlighted_content = highlight_terms(original_content, query)
        highlighted_name = highlight_terms(doc['name'], query)
        
        similarity_score = float(distances[0][i])
        
        result = {
            "path": doc['path'],
            "highlighted_name": highlighted_name,
            "content_snippet": content_snippet,
            "content": content,
            "original_content": original_content,
            "highlighted_content": highlighted_content,
            "content_length": content_length,
            "relevance_score": similarity_score,
        }
        
        # Keep only the most relevant result for each unique file path
        if doc['path'] not in unique_results or similarity_score > unique_results[doc['path']]['relevance_score']:
            unique_results[doc['path']] = result

    # Convert the dictionary to a list and sort by relevance score
    results = list(unique_results.values())
    results.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    # Trim to the requested number of results
    results = results[:k]
    
    return results
