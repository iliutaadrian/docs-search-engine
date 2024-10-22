

<h2 align="center">
DOCU-SEEK
</h2>

<p align="center">
    <em>Unlocking Knowledge, One Query at a Time</em>
</p>

<p align="center">
	<img src="https://img.shields.io/github/license/iliutaadrian/docu-seek?style=flat&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/iliutaadrian/docu-seek?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/iliutaadrian/docu-seek?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/iliutaadrian/docu-seek?style=flat&color=0080ff" alt="repo-language-count">
</p>

<p align="center">
	<img src="https://img.shields.io/badge/JavaScript-F7DF1E.svg?style=flat&logo=JavaScript&logoColor=black" alt="JavaScript">
	<img src="https://img.shields.io/badge/scikitlearn-F7931E.svg?style=flat&logo=scikit-learn&logoColor=white" alt="scikitlearn">
	<img src="https://img.shields.io/badge/HTML5-E34F26.svg?style=flat&logo=HTML5&logoColor=white" alt="HTML5">
	<img src="https://img.shields.io/badge/YAML-CB171E.svg?style=flat&logo=YAML&logoColor=white" alt="YAML">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<br>
	<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white" alt="Docker">
	<img src="https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white" alt="NumPy">
	<img src="https://img.shields.io/badge/Flask-000000.svg?style=flat&logo=Flask&logoColor=white" alt="Flask">
	<img src="https://img.shields.io/badge/Markdown-000000.svg?style=flat&logo=Markdown&logoColor=white" alt="Markdown">
</p>

## 📍 Overview

Docu-Seek is a document search platform designed for efficient use for personal or organizational document collections. Make it easy to visualise the different types of results for multiple types of search algorithms.

![Screenshot 2024-10-16 at 07 59 37](https://github.com/user-attachments/assets/09856b39-6014-426d-8927-777974e89398)

![Screenshot 2024-10-16 at 08 00 57](https://github.com/user-attachments/assets/7551d5eb-3ad6-4b86-8b82-1548d1b0dc58)

## 👾 Key Features

- Seamless indexing of PDF, Markdown, TXT files
- Multiple search methods: Full-text, Vector-based, and AI-assisted

## 🔍 Search Methods

### Syntactic Search Methods
- **Full-Text Search (FTS)**: Quick word-based search using an index. Good for exact matches.
- **BM25**: Ranks documents by relevance to a search query.
- **TF-IDF**: Finds important words in documents for similarity matching.

### Semantic Search Methods
- **OpenAI Embeddings**: Uses AI to understand context and meaning in searches.
- **baai Embeddings**: Captures context-dependent meanings in text.
- **Sentence Transformers**: Compares semantic similarity between sentences.

### Hybrid and Advanced Methods
- **Hybrid Search**: Combines word-based and meaning-based search methods.
- **Reciprocal Rank Fusion**: Merges results from multiple search methods.
- **AI-Assisted Search**: Uses AI to analyze and summarize search results.

### Ranking and Personalization Methods
- **Page Ranking**: Ranks results based on popularity and user behavior.


## 📂 Repository Structure

```sh
└── docu-seek/
    ├── Dockerfile
    ├── README.md
    ├── docker-compose.yml
    ├── docs
    │   ├── cybersecurity.md
    │   ├── gpt-4.pdf
    │   ├── ml_overview.md
    │   └── web_dev.md
    ├── requirements.txt
    ├── src
    │   ├── app.py
    │   ├── config
    │   │   └── config.py
    │   ├── document_processor.py
    │   ├── llm.py
    │   ├── search
    │   │   ├── baai_search.py
    │   │   ├── fulltext_search.py
    │   │   ├── openai_search.py
    │   │   ├── sentence_transformers_search.py
    │   │   └── tfidf_search.py
    │   └── templates
    │       └── index.html
    └── test
        └── k6_search_load_test.js
```

---

## 🧩 Modules

<details closed><summary>.</summary>

| File | Summary |
| --- | --- |
| [requirements.txt](https://github.com/iliutaadrian/docu-seek/blob/main/requirements.txt) | Enables the execution of the project by specifying required Python libraries. Necessary dependencies encompass Flask for web services, PyPDF2 for PDF processing, and additional tools for various functionalities like language processing and search capabilities. |
| [docker-compose.yml](https://github.com/iliutaadrian/docu-seek/blob/main/docker-compose.yml) | Orchestrates a web service using Flask with hot-reload for development. Maps local directories for live updates. Exposes the service on port 5017. Builds and runs the app with a specific command. |
| [Dockerfile](https://github.com/iliutaadrian/docu-seek/blob/main/Dockerfile) | Builds a containerized Flask application using Python, enabling seamless deployment and execution of the parent repositorys document search functionality. Integrated with required dependencies, the Dockerfile sets up the environment for hosting and running the app. |

</details>

<details closed><summary>src</summary>

| File | Summary |
| --- | --- |
| [document_processor.py](https://github.com/iliutaadrian/docu-seek/blob/main/src/document_processor.py) | Initializes a database, indexes and extracts content from documents (Markdown, PDF), fetches all indexed documents for processing in the Docu-Seek repository. |
| [llm.py](https://github.com/iliutaadrian/docu-seek/blob/main/src/llm.py) | Initializes and generates AI responses using GPT-3.5 Turbo based on search results. Formats AI responses for user queries with related context. Supports contextual understanding and question answering within the Docu-Seek projects architecture. |
| [app.py](https://github.com/iliutaadrian/docu-seek/blob/main/src/app.py) | Implements a Flask API for searching and retrieving documents with various modes (full-text, vector-based) and AI responses. Initiates different search engines and AI models. Handles search requests and renders HTML. |

</details>

<details closed><summary>src.templates</summary>

| File | Summary |
| --- | --- |
| [index.html](https://github.com/iliutaadrian/docu-seek/blob/main/src/templates/index.html) | The `index.html` file in the `src/templates` directory is a crucial part of the Docu Seek repository. It serves as the primary interface for the Docu Seek application, providing a user-friendly web portal for searching and accessing documents. The HTML file includes essential structure and styling elements, ensuring a visually pleasing and responsive layout for users interacting with the Docu Seek platform.---By crafting a well-structured and visually appealing web interface, this file plays a significant role in enhancing the overall user experience of the Docu Seek application. It serves as the gateway for users to interact with the search functionalities and access the wealth of documents available within the repository. |

</details>

<details closed><summary>src.config</summary>

| File | Summary |
| --- | --- |
| [config.py](https://github.com/iliutaadrian/docu-seek/blob/main/src/config/config.py) | Determines project root paths and data storage locations for Document Seeker in docu-seek repo, ensuring seamless file handling and organization. |

</details>

<details closed><summary>src.search</summary>

| File | Summary |
| --- | --- |
| [sentence_transformers_search.py](https://github.com/iliutaadrian/docu-seek/blob/main/src/search/sentence_transformers_search.py) | Initialize, create, and search with Sentence Transformer for fast similarity lookups on documents using a FAISS index. Process results for top document matches, highlighting query terms. Dynamically generate embeddings for each document, optimizing search efficiency in the parent repositorys architecture. |
| [fulltext_search.py](https://github.com/iliutaadrian/docu-seek/blob/main/src/search/fulltext_search.py) | Enables full-text search functionalities integrating SQLite with FTS5 extension. Parses and processes user queries for optimal search results, returning relevant document snippets with highlighted matches. Sorting results by occurrence count enhances search precision within the repositorys architecture. |
| [baai_search.py](https://github.com/iliutaadrian/docu-seek/blob/main/src/search/baai_search.py) | Indexes documents, calculates similarities, and highlights search query terms using baai embeddings. Implements search function for top results based on similarity score. |
| [tfidf_search.py](https://github.com/iliutaadrian/docu-seek/blob/main/src/search/tfidf_search.py) | Initializes and loads a TF-IDF FAISS search index to enable document search based on queries. Searches for relevant documents, highlighting query terms in results. Supports customization such as result snippet length and occurrence count. |
| [openai_search.py](https://github.com/iliutaadrian/docu-seek/blob/main/src/search/openai_search.py) | Initializes and searches an OpenAI embeddings vector store. Processes documents, splits them for embeddings, and performs similarity search with score, returning processed results for text highlighting. |

</details>

<details closed><summary>test</summary>

| File | Summary |
| --- | --- |
| [k6_search_load_test.js](https://github.com/iliutaadrian/docu-seek/blob/main/test/k6_search_load_test.js) | Load test script simulates high user load by sending random search queries to the search endpoint using different modes. Validates response status code, non-empty body, and logs search performance metrics. |

</details>

---


## 🚀 Getting Started

### 🔖 Prerequisites

- Python: version 3.7 or higher
- Docker (optional, for containerized deployment)

### 📦 Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/iliutaadrian/docu-seek
   cd docu-seek
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up the environment:
   - Copy `.env.example` to `.env` and fill in the required variables.

### 🤖 Usage

1. Run the application:
   ```sh
   python src/app.py
   ```

2. Or use Docker:
   ```sh
   docker compose build && docker compose up
   ```

3. Access the web interface at `http://localhost:5017`



## 🧪 Testing

Run the test suite using:

```sh
pytest
```

For load testing, use the k6 script:

```sh
k6 run test/k6_search_load_test.js
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).
 
