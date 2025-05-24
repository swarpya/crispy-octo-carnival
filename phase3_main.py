"""
Phase 3: RAG System with LLM Response Generation
Complete RAG pipeline with intelligent response generation
"""
import logging
from query_processor import QueryProcessor
from response_generator import ResponseGenerator
import sys
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RAGPhase3System:
    """Complete RAG system with LLM-powered responses"""
    
    def __init__(self):
        self.query_processor = QueryProcessor()
        self.response_generator = ResponseGenerator()
        self.running = True
        logger.info("RAG Phase 3 System initialized")
    
    def display_welcome(self):
        """Display enhanced welcome message"""
        print("\n" + "="*80)
        print("🧠 RAG System - Phase 3: Intelligent Response Generation")
        print("="*80)
        print("Welcome to the complete RAG system with AI-powered responses!")
        print("\nFeatures:")
        print("  🔍 Smart semantic search across your book collection")
        print("  🤖 AI-generated comprehensive answers")
        print("  📚 Source citations and evidence-based responses")
        print("  ⚡ Real-time streaming responses")
        print("\nCommands:")
        print("  • Ask any question to get AI-powered answers")
        print("  • 'stream' mode for real-time response generation")
        print("  • 'sources' - Show search results without AI response")
        print("  • 'stats' - Collection statistics")
        print("  • 'help' - Show detailed help")
        print("  • 'quit' - Exit system")
        print("-"*80)
    
    def process_query_with_ai(self, query: str, stream_mode: bool = False):
        """Process query and generate AI response"""
        print(f"\n🔍 Searching for: '{query}'")
        
        # Get search results
        query_result = self.query_processor.process_query(query)
        
        if not query_result.results:
            print(f"\n❌ No relevant information found for: '{query}'")
            print("Try rephrasing your question or using different keywords.")
            return
        
        print(f"📊 Found {len(query_result.results)} relevant sources")
        print("🤖 Generating AI response...\n")
        
        if stream_mode:
            # Streaming response
            print("💭 AI Response:")
            print("-" * 60)
            for chunk in self.response_generator.generate_streaming_response(query_result):
                print(chunk, end="", flush=True)
            print("\n")
        else:
            # Complete response
            response = self.response_generator.generate_response(query_result)
            print("💭 AI Response:")
            print("-" * 60)
            print(response)
        
        # Show sources
        print("\n📚 Sources:")
        print("-" * 60)
        for i, result in enumerate(query_result.results[:3], 1):
            print(f"{i}. {result.title} by {result.author} (Page {result.page_number})")
            print(f"   Relevance: {result.relevance_score:.3f}")
    
    def show_sources_only(self, query: str):
        """Show search results without AI response"""
        query_result = self.query_processor.process_query(query)
        
        if not query_result.results:
            print(f"\n❌ No results found for: '{query}'")
            return
        
        print(f"\n📊 Search Results for: '{query}'")
        print(f"Found {len(query_result.results)} sources in {query_result.processing_time:.3f}s")
        print("="*80)
        
        for i, result in enumerate(query_result.results, 1):
            print(f"\n📄 Source {i} - Relevance: {result.relevance_score:.3f}")
            print(f"📖 {result.title} by {result.author} (Page {result.page_number})")
            print(f"📝 {result.text[:300]}..." if len(result.text) > 300 else result.text)
    
    def show_stats(self):
        """Display system statistics"""
        print("\n📊 System Statistics")
        print("-"*50)
        
        stats = self.query_processor.get_book_statistics()
        if stats:
            print(f"📚 Total text chunks: {stats.get('total_chunks', 0):,}")
            print(f"📖 Unique books: {stats.get('unique_books', 0)}")
            print(f"✍️  Unique authors: {stats.get('unique_authors', 0)}")
            print(f"🔄 Collection status: {stats.get('collection_status', 'Unknown')}")
            print(f"🧮 Vector embeddings: {stats.get('vector_count', 0):,}")
        else:
            print("Unable to retrieve statistics.")
    
    def process_input(self, user_input: str):
        """Process user input with enhanced commands"""
        user_input = user_input.strip()
        
        # System commands
        if user_input.lower() in ['quit', 'exit', 'q']:
            self.running = False
            print("\n👋 Thanks for using the RAG System!")
            return
        
        if user_input.lower() == 'help':
            self.show_help()
            return
        
        if user_input.lower() == 'stats':
            self.show_stats()
            return
        
        # Check for special prefixes
        if user_input.lower().startswith('stream '):
            query = user_input[7:].strip()
            self.process_query_with_ai(query, stream_mode=True)
            return
        
        if user_input.lower().startswith('sources '):
            query = user_input[8:].strip()
            self.show_sources_only(query)
            return
        
        # Regular AI-powered query
        if user_input:
            self.process_query_with_ai(user_input, stream_mode=False)
        else:
            print("Please enter a question. Type 'help' for assistance.")
    
    def show_help(self):
        """Show detailed help"""
        print("\n📖 RAG System Phase 3 - Help")
        print("-"*50)
        print("QUERY MODES:")
        print("  <question>              - Get AI-powered answer")
        print("  stream <question>       - Get streaming AI response")
        print("  sources <question>      - Show search results only")
        print("\nSYSTEM COMMANDS:")
        print("  stats                   - Show system statistics")
        print("  help                    - Show this help")
        print("  quit                    - Exit system")
        print("\nEXAMPLE QUERIES:")
        print("  What is quantum mechanics?")
        print("  stream How do neural networks work?")
        print("  sources artificial intelligence history")
        print("\nTIPS:")
        print("  • Ask complete questions for better AI responses")
        print("  • Use 'stream' for real-time response generation")
        print("  • Use 'sources' to see raw search results")
    
    def run(self):
        """Run the interactive system"""
        self.display_welcome()
        
        # Check system readiness
        stats = self.query_processor.get_book_statistics()
        if not stats or stats.get('total_chunks', 0) == 0:
            print("⚠️  No data found! Please run Phase 1 first:")
            print("   python phase1_main.py")
            return
        
        try:
            while self.running:
                print("\n" + "-"*80)
                user_input = input("🤔 Your question: ").strip()
                if user_input:
                    self.process_input(user_input)
                    
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
        except Exception as e:
            logger.error(f"System error: {e}")
            print(f"❌ System error: {e}")

def main():
    """Main entry point"""
    try:
        system = RAGPhase3System()
        system.run()
    except Exception as e:
        logger.error(f"Failed to start Phase 3: {e}")
        print(f"❌ Failed to start system: {e}")
        print("Ensure Qdrant is running and Phase 1 is completed.")

if __name__ == "__main__":
    main()