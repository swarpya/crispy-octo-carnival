"""
Embedding generation module using sentence-transformers
"""
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from models import TextChunk
from config import EMBEDDING_MODEL
import logging

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Generates embeddings for text chunks"""
    
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model"""
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded embedding model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to load model {self.model_name}: {e}")
            raise
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a single text"""
        if not self.model:
            raise ValueError("Model not loaded")
        
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for a batch of texts"""
        if not self.model:
            raise ValueError("Model not loaded")
        
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        return [embedding for embedding in embeddings]
    
    def generate_chunk_embeddings(self, chunks: List[TextChunk]) -> List[np.ndarray]:
        """Generate embeddings for TextChunk objects"""
        texts = [chunk.chunk_text for chunk in chunks]
        logger.info(f"Generating embeddings for {len(texts)} chunks...")
        
        embeddings = self.generate_embeddings_batch(texts)
        logger.info(f"Generated {len(embeddings)} embeddings")
        
        return embeddings