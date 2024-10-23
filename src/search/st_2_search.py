import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config.config import DATA_FOLDER
from search.syntactic_helper import find_snippet, highlight_terms

# Model configuration
MODEL_NAME = "all-mpnet-base-v2"

# Initialize the sentence transformer model
model = SentenceTransformer(MODEL_NAME)

documents = None
faiss_index = None
document_chunks = None
FAISS_INDEX_PATH = os.path.join(DATA_FOLDER, f"faiss_{MODEL_NAME.replace('/', '-')}_index")

def init(docs):
    global documents, faiss_index, document_chunks
    documents = docs
    
    if os.path.exists(FAISS_INDEX_PATH):
        try:
            faiss_index = faiss.read_index(FAISS_INDEX_PATH)
            document_chunks = create_document_chunks(documents)
            print(f"Loaded existing FAISS index with {faiss_index.ntotal} vectors")
        except Exception:
            faiss_index, document_chunks = create_new_index(documents)
    else:
        faiss_index, document_chunks = create_new_index(documents)
    
    print(f"{MODEL_NAME} embeddings FAISS search initialized with {len(documents)} documents.")

def create_document_chunks(docs):
    langchain_docs = [
        Document(page_content=doc['content'], metadata={"path": doc['path'], "name": doc['name']})
        for doc in docs
    ]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=20,
        length_function=len,
    )
    
    return text_splitter.split_documents(langchain_docs)

def create_new_index(docs):
    chunks = create_document_chunks(docs)
    
    # Create embeddings for all chunks
    embeddings = model.encode([chunk.page_content for chunk in chunks], 
                            show_progress_bar=True, 
                            convert_to_numpy=True)
    
    # Normalize embeddings
    faiss.normalize_L2(embeddings)
    
    # Create and train the FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings.astype('float32'))
    
    # Save the FAISS index
    faiss.write_index(index, FAISS_INDEX_PATH)
    
    return index, chunks

def search(query, k=5):
    if faiss_index is None:
        raise ValueError(f"{MODEL_NAME} FAISS index not initialized. Call init() first.")
    
    # Encode and normalize the query
    query_embedding = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_embedding)
    
    # Search the index
    distances, indices = faiss_index.search(query_embedding.astype('float32'), k=k)
    
    results = []
    
    for i, idx in enumerate(indices[0]):
        chunk = document_chunks[idx]
        doc_path = chunk.metadata["path"]
        global_doc = next((d for d in documents if d['path'] == doc_path), None)
        
        if global_doc:
            content = global_doc['content']
            original_content = global_doc['original_content']
            content_length = len(original_content)
            
            content_snippet = find_snippet(chunk.page_content, query)
            highlighted_content = highlight_terms(original_content, query)
            highlighted_name = highlight_terms(global_doc['name'], query)
            
            # Convert distance to similarity score
            similarity_score = float(distances[0][i])  # Already normalized by FAISS
            
            result = {
                "path": global_doc['path'],
                "highlighted_name": highlighted_name,
                "content_snippet": content_snippet,
                "content": content,
                "original_content": original_content,
                "highlighted_content": highlighted_content,
                "content_length": content_length,
                "relevance_score": similarity_score,
                "chunk": chunk.page_content
            }
            
            results.append(result)
    
    results.sort(key=lambda x: x['relevance_score'], reverse=True)
    return results
