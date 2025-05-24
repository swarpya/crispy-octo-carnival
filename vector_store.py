"""
Vector storage module using Qdrant
"""
from typing import List
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from models import TextChunk
from config import QDRANT_HOST, QDRANT_PORT, COLLECTION_NAME
import logging
import uuid

logger = logging.getLogger(__name__)

class VectorStore:
    """Handles vector storage operations with Qdrant"""
    
    def __init__(self):
        self.client = None
        self.collection_name = COLLECTION_NAME
        self._connect()
    
    def _connect(self):
        """Connect to Qdrant instance"""
        try:
            # Try connecting with URL format first
            self.client = QdrantClient(url=f"http://{QDRANT_HOST}:{QDRANT_PORT}")
            logger.info(f"Connected to Qdrant at http://{QDRANT_HOST}:{QDRANT_PORT}")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            # Try alternative connection method
            try:
                self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, prefer_grpc=False)
                logger.info(f"Connected to Qdrant using alternative method")
            except Exception as e2:
                logger.error(f"Alternative connection also failed: {e2}")
                raise
    
    def create_collection(self, vector_size: int):
        """Create collection if it doesn't exist"""
        try:
            # Check if collection exists
            try:
                collection_info = self.client.get_collection(self.collection_name)
                logger.info(f"Collection {self.collection_name} already exists")
                return
            except:
                # Collection doesn't exist, create it
                pass
            
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            logger.info(f"Created collection: {self.collection_name}")
            
        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            raise
    
    def store_chunks(self, chunks: List[TextChunk], embeddings: List[np.ndarray]):
        """Store text chunks with their embeddings"""
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks and embeddings must match")
        
        # Create collection with appropriate vector size
        if embeddings:
            vector_size = len(embeddings[0])
            self.create_collection(vector_size)
        
        # Prepare points for upload
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # Use UUID for point ID to avoid conflicts
            point_id = str(uuid.uuid4())
            
            point = PointStruct(
                id=point_id,
                vector=embedding.tolist(),
                payload=chunk.to_metadata()
            )
            points.append(point)
        
        # Upload points in smaller batches to avoid issues
        batch_size = 50
        total_batches = (len(points) - 1) // batch_size + 1
        
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            try:
                result = self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )
                batch_num = i // batch_size + 1
                logger.info(f"Uploaded batch {batch_num}/{total_batches} ({len(batch)} points)")
                
            except Exception as e:
                logger.error(f"Failed to upload batch {batch_num}: {e}")
                raise
        
        logger.info(f"Successfully stored {len(chunks)} chunks in Qdrant")
    
    def get_collection_info(self):
        """Get information about the collection"""
        try:
            info = self.client.get_collection(self.collection_name)
            return info
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return None