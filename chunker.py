"""
Text chunking module for breaking text into manageable pieces
"""
from typing import List, Tuple
import re
from models import TextChunk, Book
from config import CHUNK_SIZE, CHUNK_OVERLAP
import logging

logger = logging.getLogger(__name__)

class TextChunker:
    """Handles text chunking with overlap and metadata preservation"""
    
    def __init__(self, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
        return text.strip()
    
    def split_text_into_chunks(self, text: str) -> List[str]:
        """Split text into overlapping chunks"""
        clean_text = self.clean_text(text)
        words = clean_text.split()
        
        if len(words) <= self.chunk_size:
            return [clean_text]
        
        chunks = []
        start = 0
        
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk_words = words[start:end]
            chunk_text = ' '.join(chunk_words)
            chunks.append(chunk_text)
            
            # Move start position with overlap
            if end >= len(words):
                break
            start = end - self.overlap
        
        return chunks
    
    def create_chunks_from_pages(self, book: Book, pages_text: List[Tuple[int, str]]) -> List[TextChunk]:
        """Create TextChunk objects from book pages"""
        all_chunks = []
        chunk_counter = 0
        
        for page_num, page_text in pages_text:
            page_chunks = self.split_text_into_chunks(page_text)
            
            for chunk_text in page_chunks:
                if len(chunk_text.strip()) < 50:  # Skip very short chunks
                    continue
                
                chunk = TextChunk(
                    chunk_id="",  # Will be auto-generated
                    book_id=book.book_id,
                    title=book.title,
                    author=book.author,
                    page_number=page_num,
                    chunk_text=chunk_text,
                    chunk_index=chunk_counter
                )
                all_chunks.append(chunk)
                chunk_counter += 1
        
        logger.info(f"Created {len(all_chunks)} chunks for book: {book.title}")
        return all_chunks