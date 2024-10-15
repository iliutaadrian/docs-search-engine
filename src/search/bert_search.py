import os
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config.config import DATA_FOLDER
from transformers import BertTokenizer, BertModel
import torch
import numpy as np

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
model.eval()

documents = None
vector_store = None
FAISS_INDEX_PATH = os.path.join(DATA_FOLDER, "faiss_bert_index")

def embed_text(text):
    inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

def init(docs):
    global documents, vector_store
    documents = docs
    
    if os.path.exists(FAISS_INDEX_PATH):
        print("Loading existing FAISS index...")
        try:
            vector_store = FAISS.load_local(FAISS_INDEX_PATH, embed_text, allow_dangerous_deserialization=True)
            print(f"Loaded vector store with {vector_store.index.ntotal} vectors.")
        except Exception as e:
            print(f"Error loading existing index: {e}")
            print("Creating new FAISS index...")
            vector_store = create_new_index(documents)
    else:
        print("Creating new FAISS index...")
        vector_store = create_new_index(documents)

def create_new_index(docs):
    langchain_docs = [
        Document(page_content=doc['content'], metadata={"path": doc['path']})
        for doc in docs
    ]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    split_docs = text_splitter.split_documents(langchain_docs)
    
    # Create embeddings
    texts = [doc.page_content for doc in split_docs]
    embeddings = [embed_text(text) for text in texts]
    
    # Create vector store
    vs = FAISS.from_embeddings(embeddings, texts, embed_text)
    
    # Save the index
    vs.save_local(FAISS_INDEX_PATH)
    
    print(f"Vector search initialized with {len(split_docs)} chunks from {len(docs)} documents using BERT model.")
    return vs

def search(query, k=5):
    if vector_store is None:
        raise ValueError("Vector store not initialized. Call init() first.")
    
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
    
    return processed_results
