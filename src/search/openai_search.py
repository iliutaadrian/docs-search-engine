import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config.config import DATA_FOLDER

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
documents = None
vector_store = None
FAISS_INDEX_PATH = os.path.join(DATA_FOLDER, "faiss_openai_index")

def init(docs):
    global documents, vector_store
    documents = docs
    
    if os.path.exists(FAISS_INDEX_PATH):
        print("Loading existing OpenAI embeddings FAISS index...")
        try:
            vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
            print(f"Successfully loaded vector store with {vector_store.index.ntotal} OpenAI embedding vectors.")
        except Exception as e:
            print(f"Error loading existing OpenAI embeddings index: {e}")
            print("Creating new OpenAI embeddings FAISS index...")
            vector_store = create_new_index(documents)
    else:
        print("Creating new OpenAI embeddings FAISS index...")
        vector_store = create_new_index(documents)

def create_new_index(docs):
    print("Processing documents for OpenAI embeddings...")
    langchain_docs = [
        Document(page_content=doc['content'], metadata={"path": doc['path']})
        for doc in docs
    ]
    
    print("Splitting documents into chunks for more granular embeddings...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    split_docs = text_splitter.split_documents(langchain_docs)
    
    print(f"Generating OpenAI embeddings for {len(split_docs)} document chunks...")
    vs = FAISS.from_documents(split_docs, embeddings)
    
    print("Saving OpenAI embeddings FAISS index...")
    vs.save_local(FAISS_INDEX_PATH)
    
    print(f"OpenAI embeddings vector search initialized with {len(split_docs)} chunks from {len(docs)} documents using text-embedding-3-large model.")
    return vs

def search(query, k=5):
    if vector_store is None:
        raise ValueError("OpenAI embeddings vector store not initialized. Call init() first.")
    
    results = vector_store.similarity_search_with_score(query, k=k)
    
    processed_results = []
    for doc, score in results:
        full_content = doc.page_content
        content_length = len(full_content)
        content_snippet = full_content[:100] + "..." if len(full_content) > 100 else full_content
        highlighted_content = full_content
        for term in query.split():
            highlighted_content = highlighted_content.replace(term, f"<b>{term}</b>")
        occurrence_count = sum(full_content.lower().count(term.lower()) for term in query.split())
        
        processed_results.append({
            "path": doc.metadata["path"],
            "name": os.path.basename(doc.metadata["path"]),
            "content_snippet": content_snippet,
            "content_length": content_length,
            "full_content": full_content,
            "highlighted_content": highlighted_content,
            "occurrence_count": occurrence_count,
            "similarity_score": 1 - score  # FAISS returns distance, so we convert it to similarity
        })
    
    print(f"Returned {len(processed_results)} processed results from OpenAI embeddings search.")
    return processed_results
