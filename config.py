"""
Configuration settings for the RAG system - Updated for Phase 3
"""
import os

# Qdrant Configuration
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "book_library"

# Embedding Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # sentence-transformers model
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50

# File Paths
BOOKS_DIRECTORY = "books/"
PROCESSED_DATA_DIR = "processed_data/"

# Phase 2: Query Processing Configuration
DEFAULT_TOP_K = 10  # Default number of results to return
DEFAULT_SCORE_THRESHOLD = 0.5  # Minimum relevance score
MAX_CONTEXT_LENGTH = 2000  # Maximum characters for context
QUERY_TIMEOUT = 30  # Query timeout in seconds

# Phase 3: LLM Configuration
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
GROQ_TEMPERATURE = 0.5
GROQ_MAX_TOKENS = 1024

# Display Configuration
MAX_RESULT_TEXT_LENGTH = 400  # Max characters to display per result
RESULTS_PER_PAGE = 5  # Results to display per page in interactive mode

# Create directories if they don't exist
os.makedirs(BOOKS_DIRECTORY, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)