"""
Phase 1: Data Preparation Pipeline
Main orchestrator for the RAG system Phase 1
"""
import os
import logging
from typing import List
from models import Book
from text_extractor import TextExtractor
from chunker import TextChunker
from embedder import EmbeddingGenerator
from vector_store import VectorStore
from config import BOOKS_DIRECTORY

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RAGPhase1Pipeline:
    """Main pipeline for Phase 1: Data Preparation"""
    
    def __init__(self):
        self.text_extractor = TextExtractor()
        self.chunker = TextChunker()
        self.embedder = EmbeddingGenerator()
        self.vector_store = VectorStore()
    
    def discover_books(self, books_dir: str = BOOKS_DIRECTORY) -> List[Book]:
        """Discover book files in the directory"""
        books = []
        supported_extensions = ['.pdf', '.txt']
        
        for filename in os.listdir(books_dir):
            file_path = os.path.join(books_dir, filename)
            if os.path.isfile(file_path):
                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext in supported_extensions:
                    # Extract title and author from filename (simple approach)
                    name_parts = os.path.splitext(filename)[0].split(' - ')
                    title = name_parts[0].strip()
                    author = name_parts[1].strip() if len(name_parts) > 1 else "Unknown Author"
                    
                    book = Book(
                        book_id="",  # Will be auto-generated
                        title=title,
                        author=author,
                        file_path=file_path
                    )
                    books.append(book)
        
        logger.info(f"Discovered {len(books)} books")
        return books
    
    def process_single_book(self, book: Book):
        """Process a single book through the entire pipeline"""
        logger.info(f"Processing book: {book.title}")
        
        # Step 1: Extract text from book
        pages_text = self.text_extractor.extract_text(book)
        if not pages_text:
            logger.warning(f"No text extracted from {book.title}")
            return
        
        # Step 2: Create chunks
        chunks = self.chunker.create_chunks_from_pages(book, pages_text)
        if not chunks:
            logger.warning(f"No chunks created for {book.title}")
            return
        
        # Step 3: Generate embeddings
        embeddings = self.embedder.generate_chunk_embeddings(chunks)
        
        # Step 4: Store in vector database
        self.vector_store.store_chunks(chunks, embeddings)
        
        logger.info(f"Successfully processed {book.title}: {len(chunks)} chunks stored")
    
    def run_pipeline(self):
        """Run the complete Phase 1 pipeline"""
        logger.info("Starting RAG Phase 1: Data Preparation Pipeline")
        
        # Discover books
        books = self.discover_books()
        if not books:
            logger.error("No books found to process")
            return
        
        # Process each book
        for book in books:
            try:
                self.process_single_book(book)
            except Exception as e:
                logger.error(f"Failed to process {book.title}: {e}")
                continue
        
        # Show final stats
        collection_info = self.vector_store.get_collection_info()
        if collection_info:
            logger.info(f"Pipeline complete! Collection stats: {collection_info}")

def main():
    """Main entry point"""
    pipeline = RAGPhase1Pipeline()
    pipeline.run_pipeline()

if __name__ == "__main__":
    main()