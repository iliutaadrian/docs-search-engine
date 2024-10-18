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
            click_count INTEGER DEFAULT 0
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
    
   # Split into words, keeping special characters within words
    words = re.findall(r'\S+', text)
    
    # Filter words
    cleaned_words = []
    for word in words:
        # Remove numbers
        word = re.sub(r'\d', '', word)
        
        # Remove prefix and suffix of special characters
        word = re.sub(r'^[^a-z]+|[^a-z]+$', '', word)
        
        # Keep words with 2 or more characters, or single alphanumeric characters
        if len(word) >= 2 or (len(word) == 1 and word.isalnum()):
            # Keep dots, hyphens, underscores, and forward slashes
            word = ''.join(char for char in word if char.isalnum() or char in '.-_/#')
            if word:
                cleaned_words.append(word)
    
    # Remove stop words
    cleaned_words = [word for word in cleaned_words if word not in STOP_WORDS]
    
    return ' '.join(cleaned_words)

def is_quality_phrase(phrase):
    words = phrase.split()
    if len(words) > MAX_PHRASE_LENGTH or len(words) < 1:
        return False

    # Check if all words are unique
    if len(set(words)) != len(words):
        return False
    
    return True


def consolidate_phrases(phrases):
    if not phrases:
        return []  # Return an empty list if there are no phrases

    phrase_dict = defaultdict(lambda: {'tfidf_score': 0})
    for phrase, tfidf in phrases:
        base_phrase = ' '.join(sorted(phrase.split()))
        phrase_dict[base_phrase]['tfidf_score'] = max(phrase_dict[base_phrase]['tfidf_score'], tfidf)
    
    # Convert the dictionary to a list of tuples
    consolidated = [(phrase, data['tfidf_score']) for phrase, data in phrase_dict.items()]
    
    return consolidated
    

def add_or_update_items(items):
    if not items:
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    
    for item, tfidf_score in items:
        cursor.execute('''
            INSERT INTO autocomplete_items (phrase, tfidf_score)
            VALUES (?, ?)
            ON CONFLICT(phrase) DO UPDATE SET 
                tfidf_score = MAX(tfidf_score, ?)
        ''', (item, tfidf_score, tfidf_score))
    
    conn.commit()
    conn.close()

def populate_autocomplete_from_documents(documents):
    phrases = []
    
    vectorizer = TfidfVectorizer(stop_words=list(STOP_WORDS), token_pattern=r'\b\w+\b')
    corpus = [clean_text(doc['content']) for doc in documents]
    
    tfidf_matrix = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names_out()

    for doc_index, doc in enumerate(documents):
        cleaned_content = clean_text(doc['content'])
        words = cleaned_content.split()
        
        print(f"Document {doc_index + 1} - Number of words after cleaning: {len(words)}")
        print(f"Document {doc_index + 1} - First 10 words: {words[:20]}")
        
        for i in range(len(words)):
            for j in range(i + 1, min(i + MAX_PHRASE_LENGTH + 1, len(words) + 1)):
                phrase = ' '.join(words[i:j])
                if is_quality_phrase(phrase):
                    phrase_words = [word for word in phrase.split() if word in vectorizer.vocabulary_]
                    if phrase_words:
                        tfidf_scores = [tfidf_matrix[doc_index, vectorizer.vocabulary_[word]] for word in phrase_words]
                        tfidf_score = np.max(tfidf_scores)
                        phrases.append((phrase, tfidf_score))
                    else:
                        continue
                        print(f"Phrase '{phrase}' contains no words in the vocabulary. Skipping.")
    
    print(f"Total number of phrases found: {len(phrases)}")
    print(f"Sample phrases (first 5): {phrases[:5]}")

    consolidated_phrases = consolidate_phrases(phrases)
    print(f"Number of consolidated phrases: {len(consolidated_phrases)}")
    print(f"Sample consolidated phrases (first 5): {consolidated_phrases[:5]}")

    add_or_update_items(consolidated_phrases)
    
    quality_words = []
    for doc_index, doc in enumerate(documents):
        top_tfidf_features = tfidf_matrix[doc_index].tocoo()
        top_words = [feature_names[i] for i in top_tfidf_features.col[top_tfidf_features.data.argsort()[-TOP_TFIDF_WORDS:]]]
        for word in top_words:
            if is_quality_phrase(word) and word in vectorizer.vocabulary_:
                tfidf_score = tfidf_matrix[doc_index, vectorizer.vocabulary_[word]]
                quality_words.append((word, tfidf_score))
    
    print(f"Total number of quality words: {len(quality_words)}")
    print(f"Sample quality words (first 5): {quality_words[:5]}")

    if quality_words:
        consolidated_words = consolidate_phrases(quality_words)
        print(f"Number of consolidated quality words: {len(consolidated_words)}")
        print(f"Sample consolidated quality words (first 5): {consolidated_words[:5]}")
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
        SELECT phrase, (tfidf_score * 0.3 + (CAST(click_count AS REAL) / (SELECT MAX(click_count) FROM autocomplete_items)) * 0.7) AS combined_score
        FROM autocomplete_items
        WHERE phrase LIKE ? || '%'
        ORDER BY combined_score DESC, length(phrase) ASC
        LIMIT ?
    ''', (query.lower(), limit))
    
    suggestions = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    return suggestions
