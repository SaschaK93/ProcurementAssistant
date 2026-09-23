# Test the RAG functions
from openai import OpenAI
import os
from dotenv import load_dotenv
from rag_utils import generate_rag_answer, retrieve_chunks_from_chroma, index_folder_in_chroma, format_retrieved_sources
from pathlib import Path
import chromadb

# Get the directory where this Python file is located
base_dir = Path(__file__).parent

# Set the ChromaDB path relative to this Python file
chroma_db_path = base_dir / "chroma_db"

# Initialize ChromaDB client for persistent storage
chroma_client = chromadb.PersistentClient(
    path=str(chroma_db_path)
)

# Create folder path to index quotations
folder_path = base_dir / "quotation_samples"

# Create or get a collection in ChromaDB to store the document chunks and their embeddings
collection = chroma_client.get_or_create_collection(name="procurement_documents")

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

pdf_count = index_folder_in_chroma(folder_path,collection,client)
print(f"PDFs indexed: {pdf_count}")
print(f"Chunks stored in Chroma: {collection.count()}")

question = "Which supplier offers the shorter delivery time?"

retrieved_chunks = retrieve_chunks_from_chroma(
    question,
    collection,
    client,
    top_k=3
)

generated_answer = generate_rag_answer(
    question,
    retrieved_chunks,
    client
)

print(f"\nQuestion: {question}")

print("\nAnswer:")
print(generated_answer)

sources = format_retrieved_sources(retrieved_chunks)
print(f"Sources: {sources}")