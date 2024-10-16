Docu-Seek: Effortless Local Document Search
Docu-Seek is a lightweight, powerful document search engine designed for local use. Built with Python and SQLite, it offers fast and efficient full-text search capabilities for your personal or organizational document collection.
Key Features:

Seamless indexing of PDF and Markdown files
Full-text search using SQLite's FTS5 extension
Flask-based web interface for easy querying
Detailed search results with content snippets and previews
Grouped results for better organization and readabilit


Search Methods
Syntactic Search Methods

Full-Text Search (FTS)
Quick word-based search using an index. Good for exact matches.
Learn more

BM25
Ranks documents by relevance to a search query.
Learn more

TF-IDF
Finds important words in documents for similarity matching.
Learn more
Semantic Search Methods

OpenAI Embeddings
Uses AI to understand context and meaning in searches.
Learn more

BERT Embeddings
Captures context-dependent meanings in text.
Learn more

Sentence Transformers
Compares semantic similarity between sentences.
Learn more
Hybrid and Advanced Methods

Hybrid Search
Combines word-based and meaning-based search methods.
Learn more

Reciprocal Rank Fusion
Merges results from multiple search methods.
Learn more

AI-Assisted Search
Uses AI to analyze and summarize search results.
Learn more
Ranking and Personalization Methods

Page Ranking
Ranks results based on popularity and user behavior.
Learn more


docker compose build && docker compose up 
