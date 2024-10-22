import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from config.config import DATA_FOLDER
from search.syntactic_helper import find_snippet, highlight_terms

model = None
documents = None
faiss_index = None
model_name = "BAAI/bge-base-en-v1.5"
FAISS_INDEX_PATH = os.path.join(DATA_FOLDER, f"faiss_{model_name.replace('/', '-')}_index")

def init(docs):
    global model, documents, faiss_index
    documents = docs
    
    print(f"Initializing Sentence Transformer model ({model_name})...")
    model = SentenceTransformer(model_name)
    
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
        print(f"Creating new {model_name} FAISS index...")
        create_new_index()

def create_new_index():
    global faiss_index
    print(f"Generating embeddings for documents using {model_name}...")
    document_embeddings = model.encode([doc['content'] for doc in documents], show_progress_bar=True)
    
    dimension = document_embeddings.shape[1]
    faiss_index = faiss.IndexFlatIP(dimension)
    faiss_index.add(document_embeddings.astype('float32'))
    
    faiss.write_index(faiss_index, FAISS_INDEX_PATH)
    
    print(f"{model_name} vector search initialized with {len(documents)} documents.")

def search(query, k=5):
    if faiss_index is None:
        raise ValueError("Sentence Transformer vector store not initialized. Call init() first.")
    
    query_embedding = model.encode([query]).astype('float32')
    
    distances, indices = faiss_index.search(query_embedding, k*2)
    
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
        
        if doc['path'] not in unique_results or similarity_score > unique_results[doc['path']]['relevance_score']:
            unique_results[doc['path']] = result

    results = list(unique_results.values())
    results.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    results = results[:k]
    
    return results

