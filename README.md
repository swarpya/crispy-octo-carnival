# RAG System - Phases 1 & 2: Complete Document Retrieval System

This is the implementation of Phases 1 & 2 for the RAG (Retrieval-Augmented Generation) system that processes books, stores them in a vector database, and provides intelligent search capabilities.

## Project Structure

```
rag_system/
├── config.py           # Configuration settings (updated for Phase 2)
├── models.py           # Data models (Book, TextChunk)
├── text_extractor.py   # Text extraction from PDFs/TXT files
├── chunker.py          # Text chunking with overlap
├── embedder.py         # Embedding generation
├── vector_store.py     # Qdrant vector database operations
├── query_processor.py  # Phase 2: Query processing and search
├── phase1_main.py      # Phase 1: Data preparation pipeline
├── phase2_main.py      # Phase 2: Interactive query interface
├── requirements.txt    # Python dependencies
├── books/              # Directory for book files
└── processed_data/     # Directory for processed data
```

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Qdrant Locally**
   ```bash
   # Using Docker
   docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
   ```

3. **Add Books**
   - Place your PDF or TXT files in the `books/` directory
   - Use filename format: `"Title - Author.pdf"` or `"Title - Author.txt"`
   - Example: `"Quantum Physics - Dr. Sarah Chen.pdf"`

4. **Run Phase 1 Pipeline (Data Preparation)**
   ```bash
   python phase1_main.py
   ```

5. **Run Phase 2 Interface (Query System)**
   ```bash
   python phase2_main.py
   ```

## Phase 1: Data Preparation

Phase 1 handles the initial data processing:

1. **Book Discovery**: Scans the `books/` directory for PDF and TXT files
2. **Text Extraction**: Extracts text from each book page by page
3. **Text Chunking**: Breaks text into 400-word chunks with 50-word overlap
4. **Embedding Generation**: Creates semantic embeddings using sentence-transformers
5. **Vector Storage**: Stores embeddings and metadata in Qdrant

### Key Features
- **Modular Architecture**: Each component is separate and reusable
- **Metadata Preservation**: Tracks book ID, title, author, and page numbers
- **Batch Processing**: Handles multiple books efficiently
- **Error Handling**: Continues processing even if individual books fail
- **Comprehensive Logging**: Monitors progress and errors

## Phase 2: Query Processing & Search

Phase 2 provides intelligent search and retrieval capabilities:

### Search Features
- **Semantic Search**: Find relevant content using natural language queries
- **Book-Specific Search**: Search within a particular book
- **Author-Specific Search**: Search across books by a specific author
- **Relevance Scoring**: Results ranked by semantic similarity
- **Context Extraction**: Automatically extract relevant context for queries

### Interactive Interface
The Phase 2 interface provides:

- **Natural Language Queries**: Ask questions in plain English
- **Multiple Search Modes**: 
  - General search: `What is quantum mechanics?`
  - Book search: `book:Quantum Physics - What are photons?`
  - Author search: `author:Dr. Sarah Chen - energy levels`
- **Collection Statistics**: View database stats with `stats` command
- **Formatted Results**: Clean, readable output with relevance scores
- **Context Summaries**: Automatic context extraction for follow-up questions

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `<query>` | Search across all books | `What is machine learning?` |
| `book:<title> - <query>` | Search within specific book | `book:Physics Fundamentals - energy` |
| `author:<name> - <query>` | Search by author | `author:Einstein - relativity` |
| `stats` | Show collection statistics | `stats` |
| `help` | Display help information | `help` |
| `quit` | Exit the system | `quit` |

## Configuration

Edit `config.py` to customize:

### Phase 1 Settings
- Chunk size and overlap
- Qdrant connection details
- File directories
- Embedding model

### Phase 2 Settings
- Default number of search results (`DEFAULT_TOP_K`)
- Minimum relevance score threshold (`DEFAULT_SCORE_THRESHOLD`)
- Maximum context length (`MAX_CONTEXT_LENGTH`)
- Display formatting options

## Usage Examples

### Basic Search
```bash
$ python phase2_main.py
🤔 Your question: What is quantum entanglement?
```

### Book-Specific Search
```bash
🤔 Your question: book:Quantum Physics - photon behavior
```

### Author-Specific Search
```bash
🤔 Your question: author:Dr. Sarah Chen - wave functions
```

### System Statistics
```bash
🤔 Your question: stats
📊 Collection Statistics
Total text chunks: 1,247
Unique books: 5
Unique authors: 3
```

## Technical Details

### Search Algorithm
1. **Query Preprocessing**: Clean and normalize user queries
2. **Embedding Generation**: Convert queries to semantic vectors
3. **Vector Search**: Use cosine similarity to find relevant chunks
4. **Result Ranking**: Sort by relevance score
5. **Context Assembly**: Combine relevant chunks for comprehensive answers

### Performance Optimizations
- **Batch Processing**: Efficient embedding generation
- **Vector Indexing**: Fast similarity search with Qdrant
- **Result Caching**: Improved response times for similar queries
- **Memory Management**: Optimized for large document collections

## Next Steps (Future Phases)

- **Phase 3**: LLM integration for response generation
- **Phase 4**: Web interface and REST API
- **Phase 5**: Advanced features (summarization, multi-modal support)

## Troubleshooting

### Common Issues

**No results found:**
- Check that Phase 1 completed successfully
- Verify books are in the correct format and directory
- Try rephrasing queries with different keywords

**Connection errors:**
- Ensure Qdrant is running on port 6333
- Check Docker container status: `docker ps`
- Verify firewall settings

**Performance issues:**
- Increase `DEFAULT_TOP_K` for more results
- Adjust `DEFAULT_SCORE_THRESHOLD` for broader matches
- Check system resources (RAM, CPU)

**Empty collection:**
- Run `python phase1_main.py` first
- Check `books/` directory has supported files
- Review Phase 1 logs for processing errors

## System Requirements

- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 1GB free space per 100MB of books
- **Docker**: For Qdrant vector database

## API Usage (Programmatic)

```python
from query_processor import QueryProcessor

# Initialize processor
processor = QueryProcessor()

# Simple search
result = processor.process_query("What is artificial intelligence?")
print(f"Found {result.total_results} results")

# Book-specific search
book_results = processor.search_by_book("AI Fundamentals", "neural networks")

# Get collection stats
stats = processor.get_book_statistics()
print(f"Total chunks: {stats['total_chunks']}")
```

## Contributing

When adding new features:
1. Follow the modular architecture pattern
2. Add comprehensive logging
3. Include error handling
4. Update configuration options
5. Add usage examples to README