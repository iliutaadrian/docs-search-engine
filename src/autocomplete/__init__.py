import sqlite3
import os
import re
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from config.config import DATA_FOLDER
import numpy as np

AUTOCOMPLETE_DB_PATH = os.path.join(DATA_FOLDER, 'autocomplete.db')
MAX_PHRASE_LENGTH = 5
BATCH_SIZE = 1000
TOP_TFIDF_WORDS = 20


# Weights for the ranking formula
TFIDF_WEIGHT = 0.3
CLICK_COUNT_WEIGHT = 0.3
DOC_NAME_WEIGHT = 0.4


STOP_WORDS = set([
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t', 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
    'can\'t', 'cannot', 'could', 'couldn\'t',
    'aren', 'can', 'couldn', 'd', 'didn', 'doesn', 'don', 'hadn', 'hasn', 'haven', 'isn', 'let', 'll', 'm', 'mustn', 're', 's', 'shan', 'shouldn', 't', 've', 'wasn', 'weren', 'won', 'wouldn',
    'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t', 'down', 'during',
    'each',
    'few', 'for', 'from', 'further',
    'had', 'hadn\'t', 'has', 'hasn\'t', 'have', 'haven\'t', 'having', 'he', 'he\'d', 'he\'ll', 'he\'s', 'her', 'here', 'here\'s', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'how\'s',
    'i', 'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t', 'it', 'it\'s', 'its', 'itself',
    'let\'s', 'link',
    'me', 'more', 'most', 'mustn\'t', 'my', 'myself',
    'no', 'nor', 'not',
    'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
    'same', 'shan\'t', 'she', 'she\'d', 'she\'ll', 'she\'s', 'should', 'shouldn\'t', 'so', 'some', 'such',
    'than', 'that', 'that\'s', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'there\'s', 'these', 'they', 'they\'d', 'they\'ll', 'they\'re', 'they\'ve', 'this', 'those', 'through', 'to', 'too',
    'under', 'until', 'up', 'very',
    'was', 'wasn\'t', 'we', 'we\'d', 'we\'ll', 'we\'re', 'we\'ve', 'were', 'weren\'t', 'what', 'what\'s', 'when', 'when\'s', 'where', 'where\'s', 'which', 'while', 'who', 'who\'s', 'whom', 'why', 'why\'s', 'with', 'won\'t', 'would', 'wouldn\'t', 'www', 'http', 'https',
    'you', 'you\'d', 'you\'ll', 'you\'re', 'you\'ve', 'your', 'yours', 'yourself', 'yourselves'
])


def get_db_connection():
    conn = sqlite3.connect(AUTOCOMPLETE_DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_autocomplete(documents):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS autocomplete_items (
            id INTEGER PRIMARY KEY,
            phrase TEXT UNIQUE,
            tfidf_score REAL,
            click_count INTEGER DEFAULT 0,
            is_doc_name BOOLEAN DEFAULT 0
        );
        CREATE INDEX IF NOT EXISTS idx_autocomplete_items_phrase ON autocomplete_items(phrase);
    ''')
    
    conn.commit()
    conn.close()
    
    populate_autocomplete_from_documents(documents)


def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove links
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Replace all non-alphanumeric characters (except spaces) with spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Split into words
    words = text.split()
    
    # Filter and process words
    cleaned_words = []
    for word in words:

        # Remove prefix and suffix of special characters
        word = re.sub(r'^[^a-z0-9]+|[^a-z0-9]+$', '', word)
        
        # Keep words with 2 or more characters, not in STOP_WORDS, and not consisting only of digits
        if len(word) >= 2 and word not in STOP_WORDS and not word.isdigit():
            cleaned_words.append(word)
    
    return ' '.join(cleaned_words)

def consolidate_phrases(phrases):
    if not phrases:
        return []  # Return an empty list if there are no phrases

    phrase_dict = defaultdict(lambda: {'tfidf_score': 0})
    for phrase, tfidf in phrases:
        # Use the original phrase as the key, preserving word order
        phrase_dict[phrase]['tfidf_score'] = max(phrase_dict[phrase]['tfidf_score'], tfidf)
    
    # Convert the dictionary to a list of tuples
    consolidated = [(phrase, data['tfidf_score']) for phrase, data in phrase_dict.items()]
    
    return consolidated

def add_or_update_items(items, is_doc_name=False):
    if not items:
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    
    for item, tfidf_score in items:
        cursor.execute('''
            INSERT INTO autocomplete_items (phrase, tfidf_score, is_doc_name)
            VALUES (?, ?, ?)
            ON CONFLICT(phrase) DO UPDATE SET 
                tfidf_score = MAX(tfidf_score, ?),
                is_doc_name = ?
        ''', (item, tfidf_score, is_doc_name, tfidf_score, is_doc_name))
    
    conn.commit()
    conn.close()


def populate_autocomplete_from_documents(documents):
    phrases = []
    doc_names = []
    
    vectorizer = TfidfVectorizer(stop_words=list(STOP_WORDS), token_pattern=r'\b\w+\b')
    corpus = [clean_text(doc['content']) for doc in documents]
    
    tfidf_matrix = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names_out()

    for doc_index, doc in enumerate(documents):
        cleaned_content = clean_text(doc['content'])
        words = cleaned_content.split()
        
        for i in range(len(words)):
            for j in range(i + 1, min(i + MAX_PHRASE_LENGTH + 1, len(words) + 1)):
                phrase = ' '.join(words[i:j])
                phrase_words = [word for word in phrase.split() if word in vectorizer.vocabulary_]
                if phrase_words:
                    tfidf_scores = [tfidf_matrix[doc_index, vectorizer.vocabulary_[word]] for word in phrase_words]
                    tfidf_score = np.max(tfidf_scores)
                    phrases.append((phrase, tfidf_score))

        doc_name = doc['name']
        if doc_name:
            doc_names.append((doc_name, 1.0))  


    consolidated_phrases = consolidate_phrases(phrases)
    add_or_update_items(consolidated_phrases)

    add_or_update_items(doc_names, is_doc_name=True)
    
    quality_words = []
    for doc_index, doc in enumerate(documents):
        top_tfidf_features = tfidf_matrix[doc_index].tocoo()
        top_words = [feature_names[i] for i in top_tfidf_features.col[top_tfidf_features.data.argsort()[-TOP_TFIDF_WORDS:]]]
        for word in top_words:
            if word in vectorizer.vocabulary_:
                tfidf_score = tfidf_matrix[doc_index, vectorizer.vocabulary_[word]]
                quality_words.append((word, tfidf_score))

    if quality_words:
        consolidated_words = consolidate_phrases(quality_words)
        add_or_update_items(consolidated_words)
    else:
        print("No quality words found.")


def update_click_count(phrase):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE autocomplete_items
        SET click_count = click_count + 1
        WHERE phrase = ?
    ''', (phrase.lower(),))
    
    conn.commit()
    conn.close()

def get_autocomplete_suggestions(query, limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT phrase,
               (? * tfidf_score + 
                ? * (CAST(click_count AS REAL) / (SELECT MAX(click_count) FROM autocomplete_items)) + 
                ? * CAST(is_doc_name AS REAL)) AS combined_score
        FROM autocomplete_items
        WHERE phrase LIKE ? || '%'
        ORDER BY combined_score DESC, length(phrase) ASC
        LIMIT ?
    ''', (TFIDF_WEIGHT, CLICK_COUNT_WEIGHT, DOC_NAME_WEIGHT, query.lower(), limit))
    
    suggestions = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    return suggestions
