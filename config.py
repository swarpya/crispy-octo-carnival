"""
Configuration settings for the RAG system
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

# Create directories if they don't exist
os.makedirs(BOOKS_DIRECTORY, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)