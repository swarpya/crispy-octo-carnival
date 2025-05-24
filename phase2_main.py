"""
Phase 2: Query Processing and Search Interface
Main interface for querying the RAG system
"""
import logging
from typing import Optional
from query_processor import QueryProcessor, QueryResult, SearchResult
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RAGPhase2Interface:
    """Interactive interface for querying the RAG system"""
    
    def __init__(self):
        self.query_processor = QueryProcessor()
        self.running = True
        logger.info("RAG Phase 2 Interface initialized")
    
    def display_welcome(self):
        """Display welcome message and instructions"""
        print("\n" + "="*80)
        print("🔍 RAG System - Phase 2: Query Interface")
        print("="*80)
        print("Welcome to the RAG (Retrieval-Augmented Generation) Query System!")
        print("\nAvailable commands:")
        print("  • Just type your question to search across all books")
        print("  • 'stats' - Show collection statistics")
        print("  • 'book:<title>' - Search within a specific book")
        print("  • 'author:<name>' - Search within books by an author")
        print("  • 'help' - Show this help message")
        print("  • 'quit' or 'exit' - Exit the system")
        print("\nExample queries:")
        print("  • What is quantum mechanics?")
        print("  • book:Quantum Physics - What are photons?")
        print("  • author:Dr. Sarah Chen - energy levels")
        print("-"*80)
    
    def display_help(self):
        """Display detailed help information"""
        print("\n📖 RAG System Help")
        print("-"*50)
        print("BASIC SEARCH:")
        print("  Just type your question: 'What is machine learning?'")
        print("\nFILTERED SEARCH:")
        print("  book:<title> <query>     - Search within specific book")
        print("  author:<name> <query>    - Search by author")
        print("\nSYSTEM COMMANDS:")
        print("  stats    - Show database statistics")
        print("  help     - Show this help")
        print("  quit     - Exit system")
        print("\nSEARCH TIPS:")
        print("  • Use specific terms for better results")
        print("  • Ask complete questions rather than single words")
        print("  • Results are ranked by relevance score")
        print("  • Each result shows book title, page number, and excerpt")
    
    def display_stats(self):
        """Display collection statistics"""
        print("\n📊 Collection Statistics")
        print("-"*50)
        
        stats = self.query_processor.get_book_statistics()
        if stats:
            print(f"Total text chunks: {stats.get('total_chunks', 0):,}")
            print(f"Unique books: {stats.get('unique_books', 0)}")
            print(f"Unique authors: {stats.get('unique_authors', 0)}")
            print(f"Collection status: {stats.get('collection_status', 'Unknown')}")
            print(f"Vector count: {stats.get('vector_count', 0):,}")
        else:
            print("Unable to retrieve statistics.")
    
    def display_results(self, query_result: QueryResult):
        """Display search results in a formatted way"""
        if not query_result.results:
            print(f"\n❌ No results found for: '{query_result.query}'")
            print("Try rephrasing your query or using different keywords.")
            return
        
        print(f"\n🔍 Results for: '{query_result.query}'")
        print(f"Found {query_result.total_results} results in {query_result.processing_time:.3f}s")
        print("="*80)
        
        for i, result in enumerate(query_result.results, 1):
            print(f"\n📄 Result {i} - Relevance: {result.relevance_score:.3f}")
            print(f"📖 {result.title} by {result.author} (Page {result.page_number})")
            print("-"*60)
            
            # Display text with some formatting
            text = result.text
            if len(text) > 400:
                text = text[:400] + "..."
            
            # Add some basic text formatting
            lines = text.split('. ')
            for line in lines:
                if line.strip():
                    print(f"   {line.strip()}.")
            print()
        
        # Show context summary
        print("="*80)
        print("💡 Quick Context Summary:")
        context = query_result.get_context_text(500)
        if context:
            lines = context.split('\n')[:3]  # First few lines
            for line in lines:
                if line.strip():
                    print(f"   {line.strip()}")
    
    def parse_special_commands(self, user_input: str) -> Optional[QueryResult]:
        """Parse and handle special commands"""
        user_input = user_input.strip()
        
        # Book-specific search
        if user_input.startswith('book:'):
            parts = user_input[5:].split(' - ', 1)
            if len(parts) == 2:
                book_title = parts[0].strip()
                query = parts[1].strip()
                print(f"\n🔍 Searching in book: '{book_title}'")
                results = self.query_processor.search_by_book(book_title, query)
                return QueryResult(
                    query=f"In '{book_title}': {query}",
                    results=results,
                    total_results=len(results),
                    processing_time=0.0
                )
            else:
                print("❌ Format: book:<title> - <query>")
                return None
        
        # Author-specific search
        elif user_input.startswith('author:'):
            parts = user_input[7:].split(' - ', 1)
            if len(parts) == 2:
                author = parts[0].strip()
                query = parts[1].strip()
                print(f"\n🔍 Searching books by: '{author}'")
                results = self.query_processor.search_by_author(author, query)
                return QueryResult(
                    query=f"By {author}: {query}",
                    results=results,
                    total_results=len(results),
                    processing_time=0.0
                )
            else:
                print("❌ Format: author:<name> - <query>")
                return None
        
        return None
    
    def process_user_input(self, user_input: str):
        """Process user input and return appropriate response"""
        user_input = user_input.strip().lower()
        
        # Handle system commands
        if user_input in ['quit', 'exit', 'q']:
            self.running = False
            print("\n👋 Thank you for using the RAG System!")
            return
        
        elif user_input == 'help':
            self.display_help()
            return
        
        elif user_input == 'stats':
            self.display_stats()
            return
        
        # Handle empty input
        if not user_input:
            print("Please enter a query or command. Type 'help' for assistance.")
            return
        
        # Handle special commands
        special_result = self.parse_special_commands(user_input)
        if special_result:
            self.display_results(special_result)
            return
        
        # Regular search query
        try:
            print(f"\n🔍 Searching for: '{user_input}'")
            query_result = self.query_processor.process_query(user_input)
            self.display_results(query_result)
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            print(f"❌ Error processing your query: {e}")
            print("Please try again or rephrase your question.")
    
    def run_interactive_mode(self):
        """Run the interactive query interface"""
        self.display_welcome()
        
        try:
            while self.running:
                print("\n" + "-"*80)
                user_input = input("🤔 Your question: ").strip()
                
                if user_input:
                    self.process_user_input(user_input)
                else:
                    print("Please enter a query. Type 'help' for assistance.")
                    
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
        except Exception as e:
            logger.error(f"Unexpected error in interactive mode: {e}")
            print(f"❌ An unexpected error occurred: {e}")
    
    def run_batch_queries(self, queries: list):
        """Run a batch of predefined queries for testing"""
        print("\n🧪 Running batch queries...")
        
        for i, query in enumerate(queries, 1):
            print(f"\n{'='*80}")
            print(f"Batch Query {i}/{len(queries)}")
            print(f"{'='*80}")
            
            try:
                query_result = self.query_processor.process_query(query)
                self.display_results(query_result)
            except Exception as e:
                print(f"❌ Error processing query '{query}': {e}")
        
        print(f"\n✅ Completed {len(queries)} batch queries")

def main():
    """Main entry point for Phase 2"""
    try:
        interface = RAGPhase2Interface()
        
        # Check if we have any data
        stats = interface.query_processor.get_book_statistics()
        if not stats or stats.get('total_chunks', 0) == 0:
            print("⚠️  No data found in the system!")
            print("Please run Phase 1 first to process some books:")
            print("   python phase1_main.py")
            return
        
        # Run interactive mode
        interface.run_interactive_mode()
        
    except Exception as e:
        logger.error(f"Failed to start Phase 2 interface: {e}")
        print(f"❌ Failed to start the system: {e}")
        print("Make sure Qdrant is running and Phase 1 has been completed.")

if __name__ == "__main__":
    main()