import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the documents folder
DOCS_FOLDER = '/docs'

# Path to the SQLite database
DB_PATH = os.path.join(BASE_DIR, 'data', 'documents.db')

# Ensure the data directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
