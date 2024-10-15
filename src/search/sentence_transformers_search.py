import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from config.config import DATA_FOLDER

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
    
    print(f"Searching for top {k} similar documents...")
    distances, indices = faiss_index.search(query_embedding, k)
    
    print(f"Processing top {k} results from Sentence Transformer similarity search...")
    results = []
    for i, idx in enumerate(indices[0]):
        doc = documents[idx]
        full_content = doc['content']
        content_length = len(full_content)
        content_snippet = full_content[:100] + "..." if len(full_content) > 100 else full_content
        highlighted_content = full_content
        for term in query.split():
            highlighted_content = highlighted_content.replace(term, f"<b>{term}</b>")
        occurrence_count = sum(full_content.lower().count(term.lower()) for term in query.split())
        
        results.append({
            "path": doc["path"],
            "name": os.path.basename(doc["path"]),
            "content_snippet": content_snippet,
            "content_length": content_length,
            "full_content": full_content,
            "highlighted_content": highlighted_content,
            "occurrence_count": occurrence_count,
            "similarity_score": float(distances[0][i])  # FAISS returns similarity, not distance for IP index
        })
    
    print(f"Returned {len(results)} processed results from Sentence Transformer search.")
    return results
