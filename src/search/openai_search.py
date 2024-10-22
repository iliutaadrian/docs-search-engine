import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config.config import DATA_FOLDER
from search.syntactic_helper import find_snippet, highlight_terms

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
documents = None
vector_store = None
FAISS_INDEX_PATH = os.path.join(DATA_FOLDER, "faiss_openai_index")

def init(docs):
    global documents, vector_store
    documents = docs
    
    if os.path.exists(FAISS_INDEX_PATH):
        try:
            vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        except Exception:
            vector_store = create_new_index(documents)
    else:
        vector_store = create_new_index(documents)
    
    print(f"OpenAI embeddings FAISS search initialized with {len(documents)} documents.")

def create_new_index(docs):
    langchain_docs = [
        Document(page_content=doc['content'], metadata={"path": doc['path'], "name": doc['name']})
        for doc in docs
    ]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    split_docs = text_splitter.split_documents(langchain_docs)
    
    vs = FAISS.from_documents(split_docs, embeddings)
    
    vs.save_local(FAISS_INDEX_PATH)
    
    return vs

def search(query, k=5):
    if vector_store is None:
        raise ValueError("OpenAI embeddings vector store not initialized. Call init() first.")
    
    semantic_results = vector_store.similarity_search_with_score(query, k=k*2)
    print(semantic_results)
    
    unique_results = {}
    for doc, score in semantic_results:
        global_doc = next((d for d in documents if d['path'] == doc.metadata["path"]), None)
        
        if global_doc:
            content = global_doc['content']
            original_content = global_doc['original_content']
            content_length = len(original_content)
            
            content_snippet = find_snippet(content, query)
            
            highlighted_content = highlight_terms(original_content, query)
            highlighted_name = highlight_terms(global_doc['name'], query)
            
            relevance_score = 1 - score              

            result = {
                "path": global_doc['path'],
                "highlighted_name": highlighted_name,
                "content_snippet": content_snippet,
                "content": content,
                "original_content": original_content,
                "highlighted_content": highlighted_content,
                "content_length": content_length,
                "relevance_score": relevance_score,
            }
            
            if global_doc['path'] not in unique_results or relevance_score > unique_results[global_doc['path']]['relevance_score']:
                unique_results[global_doc['path']] = result

    results = list(unique_results.values())
    results.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    return results[:k]
