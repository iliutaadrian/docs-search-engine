import os
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.config import DATA_FOLDER

# Initialize the BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Global variables
embeddings = []
documents = []
INDEX_PATH = os.path.join(DATA_FOLDER, "bert_index.npz")

def init(docs):
    global embeddings, documents
    
    if os.path.exists(INDEX_PATH):
        print("Loading existing BERT embeddings index...")
        try:
            data = np.load(INDEX_PATH, allow_pickle=True)
            embeddings = data['embeddings'].tolist()
            documents = data['documents'].tolist()
            print("Successfully loaded index with {} BERT embedding vectors.".format(len(embeddings)))
        except Exception as e:
            print("Error loading existing BERT embeddings index: {}".format(e))
            print("Creating new BERT embeddings index...")
            create_new_index(docs)
    else:
        print("Creating new BERT embeddings index...")
        create_new_index(docs)

def create_new_index(docs):
    global embeddings, documents
    
    print("Processing documents for BERT embeddings...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    all_splits = []
    all_metadatas = []
    for doc in docs:
        splits = text_splitter.split_text(doc['content'])
        all_splits.extend(splits)
        all_metadatas.extend([{"path": doc['path']}] * len(splits))
    
    print("Generating BERT embeddings for {} document chunks...".format(len(all_splits)))
    embeddings = model.encode(all_splits)
    documents = [{"content": split, "metadata": metadata} for split, metadata in zip(all_splits, all_metadatas)]
    
    print("Saving BERT embeddings index...")
    np.savez(INDEX_PATH, embeddings=embeddings, documents=documents)
    
    print("BERT embeddings vector search initialized with {} chunks from {} documents using all-MiniLM-L6-v2 model.".format(len(all_splits), len(docs)))

def search(query, k=5):
    global embeddings, documents
    
    if not embeddings or not documents:
        raise ValueError("BERT embeddings vector store not initialized. Call init() first.")
    
    query_embedding = model.encode([query])[0]
    
    similarities = np.dot(embeddings, query_embedding) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
    )
    top_k_indices = np.argsort(similarities)[-k:][::-1]
    
    results = [(documents[i], similarities[i]) for i in top_k_indices]
    
    processed_results = []
    for doc, score in results:
        full_content = doc['content']
        content_length = len(full_content)
        content_snippet = full_content[:100] + "..." if len(full_content) > 100 else full_content
        highlighted_content = full_content
        for term in query.split():
            highlighted_content = highlighted_content.replace(term, "<b>{}</b>".format(term))
        occurrence_count = sum(full_content.lower().count(term.lower()) for term in query.split())
        
        processed_results.append({
            "path": doc['metadata']["path"],
            "name": os.path.basename(doc['metadata']["path"]),
            "content_snippet": content_snippet,
            "content_length": content_length,
            "full_content": full_content,
            "highlighted_content": highlighted_content,
            "occurrence_count": occurrence_count,
            "similarity_score": score
        })
    
    print("Returned {} processed results from BERT embeddings search.".format(len(processed_results)))
    return processed_results
