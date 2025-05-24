"""
Text extraction module for different file formats
"""
import os
from typing import List, Tuple
import PyPDF2
import logging
from models import Book

logger = logging.getLogger(__name__)

class TextExtractor:
    """Handles text extraction from various file formats"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.txt']
    
    def extract_from_pdf(self, file_path: str) -> List[Tuple[int, str]]:
        """Extract text from PDF file, returns list of (page_num, text) tuples"""
        pages_text = []
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text.strip():  # Only add non-empty pages
                        pages_text.append((page_num, text))
        except Exception as e:
            logger.error(f"Error extracting PDF {file_path}: {e}")
        return pages_text
    
    def extract_from_txt(self, file_path: str) -> List[Tuple[int, str]]:
        """Extract text from TXT file, simulate pages by splitting"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # Simple page simulation: split by double newlines or every 2000 chars
                pages = content.split('\n\n\n')  # Assumes triple newline as page break
                if len(pages) == 1:
                    # If no page breaks, split by character count
                    pages = [content[i:i+2000] for i in range(0, len(content), 2000)]
                
                return [(i+1, page.strip()) for i, page in enumerate(pages) if page.strip()]
        except Exception as e:
            logger.error(f"Error extracting TXT {file_path}: {e}")
            return []
    
    def extract_text(self, book: Book) -> List[Tuple[int, str]]:
        """Extract text from book file based on format"""
        file_ext = os.path.splitext(book.file_path)[1].lower()
        
        if file_ext == '.pdf':
            pages_text = self.extract_from_pdf(book.file_path)
        elif file_ext == '.txt':
            pages_text = self.extract_from_txt(book.file_path)
        else:
            logger.warning(f"Unsupported format: {file_ext}")
            return []
        
        # Update book's total pages
        book.total_pages = len(pages_text)
        logger.info(f"Extracted {len(pages_text)} pages from {book.title}")
        return pages_text