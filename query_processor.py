"""
Query processing module for Phase 2 of RAG system
"""
from typing import List, Dict, Any, Optional
import numpy as np
from dataclasses import dataclass
from embedder import EmbeddingGenerator
from vector_store import VectorStore
from config import EMBEDDING_MODEL
import logging

logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    """Search result with metadata and relevance score"""
    chunk_id: str
    book_id: str
    title: str
    author: str
    page_number: int
    chunk_index: int
    text: str
    relevance_score: float
    
    def __str__(self):
        return f"[{self.title} by {self.author}, p.{self.page_number}] Score: {self.relevance_score:.3f}\n{self.text[:200]}..."

@dataclass
class QueryResult:
    """Complete query result with context and metadata"""
    query: str
    results: List[SearchResult]
    total_results: int
    processing_time: float
    
    def get_context_text(self, max_chars: int = 2000) -> str:
        """Get concatenated context text from top results"""
        context = []
        char_count = 0
        
        for result in self.results:
            if char_count + len(result.text) > max_chars:
                break
            context.append(f"[{result.title}, p.{result.page_number}]: {result.text}")
            char_count += len(result.text)
        
        return "\n\n".join(context)

class QueryProcessor:
    """Handles query processing and vector search"""
    
    def __init__(self, embedding_model: str = EMBEDDING_MODEL):
        self.embedder = EmbeddingGenerator(embedding_model)
        self.vector_store = VectorStore()
        logger.info("QueryProcessor initialized")
    
    def preprocess_query(self, query: str) -> str:
        """Clean and preprocess the query"""
        # Basic preprocessing
        query = query.strip()
        
        # Remove excessive whitespace
        query = " ".join(query.split())
        
        # Add question context if query is very short
        if len(query.split()) < 3 and not query.endswith('?'):
            query = f"What is {query}?"
        
        return query
    
    def search_similar_chunks(self, query: str, top_k: int = 10, score_threshold: float = 0.5) -> List[SearchResult]:
        """Search for similar text chunks using vector similarity"""
        try:
            # Generate embedding for the query
            query_embedding = self.embedder.generate_embedding(query)
            
            # Search in Qdrant
            search_results = self.vector_store.client.search(
                collection_name=self.vector_store.collection_name,
                query_vector=query_embedding.tolist(),
                limit=top_k,
                score_threshold=score_threshold
            )
            
            # Convert to SearchResult objects
            results = []
            for result in search_results:
                payload = result.payload
                search_result = SearchResult(
                    chunk_id=payload.get('chunk_id', ''),
                    book_id=payload.get('book_id', ''),
                    title=payload.get('title', ''),
                    author=payload.get('author', ''),
                    page_number=payload.get('page_number', 0),
                    chunk_index=payload.get('chunk_index', 0),
                    text=payload.get('text', ''),
                    relevance_score=result.score
                )
                results.append(search_result)
            
            logger.info(f"Found {len(results)} relevant chunks for query")
            return results
            
        except Exception as e:
            logger.error(f"Error searching for similar chunks: {e}")
            return []
    
    def process_query(self, query: str, top_k: int = 10, score_threshold: float = 0.5) -> QueryResult:
        """Process a complete query and return structured results"""
        import time
        start_time = time.time()
        
        # Preprocess query
        processed_query = self.preprocess_query(query)
        logger.info(f"Processing query: '{processed_query}'")
        
        # Search for similar chunks
        search_results = self.search_similar_chunks(processed_query, top_k, score_threshold)
        
        processing_time = time.time() - start_time
        
        # Create query result
        query_result = QueryResult(
            query=processed_query,
            results=search_results,
            total_results=len(search_results),
            processing_time=processing_time
        )
        
        logger.info(f"Query processed in {processing_time:.3f}s, found {len(search_results)} results")
        return query_result
    
    def get_book_statistics(self) -> Dict[str, Any]:
        """Get statistics about the book collection"""
        try:
            collection_info = self.vector_store.get_collection_info()
            if not collection_info:
                return {}
            
            # Count unique books and authors
            scroll_result = self.vector_store.client.scroll(
                collection_name=self.vector_store.collection_name,
                limit=1000,
                with_payload=True
            )
            
            books = set()
            authors = set()
            total_chunks = 0
            
            for point in scroll_result[0]:
                payload = point.payload
                books.add(f"{payload.get('title', '')} by {payload.get('author', '')}")
                authors.add(payload.get('author', ''))
                total_chunks += 1
            
            return {
                "total_chunks": total_chunks,
                "unique_books": len(books),
                "unique_authors": len(authors),
                "collection_status": collection_info.status,
                "vector_count": collection_info.vectors_count if hasattr(collection_info, 'vectors_count') else total_chunks
            }
            
        except Exception as e:
            logger.error(f"Error getting book statistics: {e}")
            return {}
    
    def search_by_book(self, book_title: str, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search within a specific book"""
        try:
            # Generate embedding for the query
            query_embedding = self.embedder.generate_embedding(query)
            
            # Search with book filter
            search_results = self.vector_store.client.search(
                collection_name=self.vector_store.collection_name,
                query_vector=query_embedding.tolist(),
                query_filter={
                    "must": [
                        {"key": "title", "match": {"value": book_title}}
                    ]
                },
                limit=top_k
            )
            
            # Convert to SearchResult objects
            results = []
            for result in search_results:
                payload = result.payload
                search_result = SearchResult(
                    chunk_id=payload.get('chunk_id', ''),
                    book_id=payload.get('book_id', ''),
                    title=payload.get('title', ''),
                    author=payload.get('author', ''),
                    page_number=payload.get('page_number', 0),
                    chunk_index=payload.get('chunk_index', 0),
                    text=payload.get('text', ''),
                    relevance_score=result.score
                )
                results.append(search_result)
            
            logger.info(f"Found {len(results)} results in book '{book_title}'")
            return results
            
        except Exception as e:
            logger.error(f"Error searching in book '{book_title}': {e}")
            return []
    
    def search_by_author(self, author: str, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search within books by a specific author"""
        try:
            # Generate embedding for the query
            query_embedding = self.embedder.generate_embedding(query)
            
            # Search with author filter
            search_results = self.vector_store.client.search(
                collection_name=self.vector_store.collection_name,
                query_vector=query_embedding.tolist(),
                query_filter={
                    "must": [
                        {"key": "author", "match": {"value": author}}
                    ]
                },
                limit=top_k
            )
            
            # Convert to SearchResult objects
            results = []
            for result in search_results:
                payload = result.payload
                search_result = SearchResult(
                    chunk_id=payload.get('chunk_id', ''),
                    book_id=payload.get('book_id', ''),
                    title=payload.get('title', ''),
                    author=payload.get('author', ''),
                    page_number=payload.get('page_number', 0),
                    chunk_index=payload.get('chunk_index', 0),
                    text=payload.get('text', ''),
                    relevance_score=result.score
                )
                results.append(search_result)
            
            logger.info(f"Found {len(results)} results by author '{author}'")
            return results
            
        except Exception as e:
            logger.error(f"Error searching by author '{author}': {e}")
            return []