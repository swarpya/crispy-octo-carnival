"""
Response generation module using Groq LLM for Phase 3
"""
from typing import List, Optional
from groq import Groq
from query_processor import SearchResult, QueryResult
from config import GROQ_MODEL, GROQ_TEMPERATURE, GROQ_MAX_TOKENS
import logging

logger = logging.getLogger(__name__)

class ResponseGenerator:
    """Generates natural language responses using Groq LLM"""
    
    def __init__(self):
        self.client = Groq()
        logger.info("ResponseGenerator initialized with Groq")
    
    def _build_context_prompt(self, query: str, search_results: List[SearchResult]) -> str:
        """Build context prompt from search results"""
        if not search_results:
            return f"Question: {query}\n\nNo relevant information found. Please provide a general response."
        
        context_parts = []
        for i, result in enumerate(search_results[:5], 1):  # Top 5 results
            context_parts.append(
                f"Source {i} [{result.title} by {result.author}, p.{result.page_number}]:\n{result.text}\n"
            )
        
        context = "\n".join(context_parts)
        return f"""Based on the following information, answer the question comprehensively:

CONTEXT:
{context}

QUESTION: {query}

Please provide a detailed answer based on the provided context. If the context doesn't fully answer the question, acknowledge what information is available and what might be missing. Always cite your sources using the format [Source X]."""
    
    def generate_response(self, query_result: QueryResult) -> str:
        """Generate response using Groq LLM"""
        try:
            prompt = self._build_context_prompt(query_result.query, query_result.results)
            
            stream = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a knowledgeable research assistant. Provide accurate, well-structured answers based on the given context. Always cite sources and be clear about the scope of your knowledge."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=GROQ_MODEL,
                temperature=GROQ_TEMPERATURE,
                max_completion_tokens=GROQ_MAX_TOKENS,
                top_p=1,
                stream=True,
            )
            
            response_text = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    response_text += chunk.choices[0].delta.content
            
            logger.info(f"Generated response of {len(response_text)} characters")
            return response_text.strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I apologize, but I encountered an error generating a response. However, I found {len(query_result.results)} relevant sources that might help answer your question about: {query_result.query}"
    
    def generate_streaming_response(self, query_result: QueryResult):
        """Generate streaming response for real-time display"""
        try:
            prompt = self._build_context_prompt(query_result.query, query_result.results)
            
            stream = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a knowledgeable research assistant. Provide accurate, well-structured answers based on the given context. Always cite sources and be clear about the scope of your knowledge."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=GROQ_MODEL,
                temperature=GROQ_TEMPERATURE,
                max_completion_tokens=GROQ_MAX_TOKENS,
                top_p=1,
                stream=True,
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
            
        except Exception as e:
            logger.error(f"Error in streaming response: {e}")
            yield f"Error generating response: {e}"