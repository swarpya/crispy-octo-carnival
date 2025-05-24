"""
Data models for the RAG system
"""
from dataclasses import dataclass
from typing import List, Optional
import uuid

@dataclass
class Book:
    """Book metadata model"""
    book_id: str
    title: str
    author: str
    file_path: str
    total_pages: int = 0
    
    def __post_init__(self):
        if not self.book_id:
            self.book_id = f"BK_{str(uuid.uuid4())[:8]}"

@dataclass
class TextChunk:
    """Text chunk model with metadata"""
    chunk_id: str
    book_id: str
    title: str
    author: str
    page_number: int
    chunk_text: str
    chunk_index: int
    
    def __post_init__(self):
        if not self.chunk_id:
            self.chunk_id = f"CH_{str(uuid.uuid4())[:8]}"
    
    def to_metadata(self) -> dict:
        """Convert to metadata dict for vector storage"""
        return {
            "chunk_id": self.chunk_id,
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "page_number": self.page_number,
            "chunk_index": self.chunk_index,
            "text": self.chunk_text
        }