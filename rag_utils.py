# Utility functions for Retrieval-Augmented Generation (RAG)

def split_text_into_chunks(
    text,
    source, 
    chunk_size=1000,
    chunk_overlap=200):
    # Splits a document into smaller overlapping text chunks for later embedding and retrieval

    chunks = []
    step = chunk_size - chunk_overlap

    for chunk_id, start in enumerate(range(0, len(text), step), start=1):  # Iterate over the text in increments of chunk_size - chunk_overlap
                                                    
        end = start + chunk_size                    # Calculate the end index for the current chunk
        
        chunk = text[start:end]                     # Extract the chunk from the text using slicing

        chunks.append({
            "text": chunk,
            "source": source,
            "chunk_id": chunk_id
        })                        # Append the chunk to the list of chunks

        # Stop if the current chunk already reaches the end of the document
        if end >= len(text):
            break

    return chunks

def create_embedding(text, client):
    # Creates a numerical embedding vector from text

    response = client.embeddings.create(
        model="text-embedding-3-small",         # Use openAI's text-embedding-3-small model for generating embeddings
        input=text
    )

    embedding = response.data[0].embedding

    return embedding

def generate_rag_answer(question, retrieved_chunks, client):

    # Function to generate an answer to a question based on retrieved chunks of text using a language model

    context = "\n\n".join(
        result["text"] for result in retrieved_chunks  # Create context for LLM by joining the retrieved chunks with double newlines
    )

    # Create a prompt for the LLM to answer the question based on the provided context
    prompt = f"""
    Answer the user's question using only the provided context.

    If the answer cannot be found in the context, say:
    "I cannot answer this question based on the provided documents."

    Context:
    {context}

    Question:
    {question}

    Answer: 
    """

    # Generate a response from the LLM using the constructed prompt
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text

def create_chunk_embeddings(chunks, client):
    # Function to create embeddings for all chunks of text

    for chunk in chunks:
        embedding = create_embedding(chunk["text"], client)     # Create an embedding for the current chunk of text
        chunk["embedding"] = embedding                          # Store the embedding in the chunk dictionary

    return chunks

def store_chunks_in_chroma(chunks, collection):
    # Function to store chunks into chromaDB

    for chunk in chunks:
        collection.upsert(      # Upsert either inserts or updates an ID
            ids=[
                f"{chunk['source']}_chunk_{chunk['chunk_id']}"
            ],
            documents=[
                chunk["text"]
            ],
            embeddings=[
                chunk["embedding"]
            ],
            metadatas=[
                {
                    "source": chunk["source"],
                    "chunk_id": chunk["chunk_id"]
                }
            ]
        )   

def retrieve_chunks_from_chroma(question, collection, client, top_k=3):
    # Function to retrieve chunks from ChromaDB

    question_embedding = create_embedding(question, client)     # Create an embedding for the user's question

    results = collection.query(
        query_embeddings=[question_embedding],                  # Search ChromaDB using the question embedding
        n_results=top_k                                         # Return the top-k most relevant chunks
    )

    retrieved_chunks = []                                       # Initialize an empty list to store the retrieved chunks

    documents = results["documents"][0]                         # Get the documents returned for the first query
    metadatas = results["metadatas"][0]                         # Get the metadata returned for the first query
    distances = results["distances"][0]                         # Get the distances returned for the first query

    for document, metadata, distance in zip(documents, metadatas, distances):

        retrieved_chunks.append({
            "text": document,                                   # Store the retrieved chunk text
            "source": metadata["source"],                       # Store the source document
            "chunk_id": metadata["chunk_id"],                   # Store the chunk ID
            "distance": distance                                # Store the ChromaDB distance
        })

    return retrieved_chunks

def index_pdf_in_chroma(pdf_path, collection, client):
    # Function for reading PDF files and sending them to chromaDB

    from pypdf import PdfReader
    
    pdf_reader = PdfReader(pdf_path)                # Read PDF file with given path
    document_text = ""

    for page in pdf_reader.pages:                   # Extract PDF contents
        page_text = page.extract_text()

        if page_text:
            document_text += page_text + "\n"

    chunks = split_text_into_chunks(                # Split PDF contents into chunks
        document_text,                              # Variable with saved PDF contents
        source=pdf_path.name,                       # Source path of PDF file
        chunk_size=1000,                            # Chunk size of 1000
        chunk_overlap=200                           # Overlapping size of 200 for better readability
    )

    chunks_with_embeddings = create_chunk_embeddings(chunks, client)    # Create embeddings for all chunks of text
    store_chunks_in_chroma(chunks_with_embeddings, collection)          # Insert or Update chunks in chromaDB

def index_folder_in_chroma(folder_path, collection, client):
    # Function to index whole PDF folder instead of single files

    pdf_count = 0

    for pdf_path in folder_path.glob("*.pdf"):

        index_pdf_in_chroma(pdf_path, collection, client)
        pdf_count += 1

    return pdf_count

def format_retrieved_sources(retrieved_chunks):
    # Function to format retrieved source information

    sources = []

    for chunk in retrieved_chunks:
        sources.append({
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"]
        })

    return sources

def index_uploaded_pdf_in_chroma(uploaded_file, collection, client):
    # Index a PDF uploaded through Streamlit

    from pypdf import PdfReader

    pdf_reader = PdfReader(uploaded_file)
    document_text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            document_text += page_text + "\n"

    chunks = split_text_into_chunks(
        document_text,
        source=uploaded_file.name,
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks_with_embeddings = create_chunk_embeddings(chunks, client)

    store_chunks_in_chroma(
        chunks_with_embeddings,
        collection
    )

# ---------------------------------------------------------------------------------------
# Legacy learning functions - manual vector retrieval implementation
# Kept for documentation purposes; not used by the production RAG pipeline
# ---------------------------------------------------------------------------------------

def cosine_similarity(vector_a, vector_b):
    # Calculates the cosine similarity between two embedding vectors
    # Only used during development for learning purposes, not used in the final product

    import numpy as np

    vector_a = np.array(vector_a)
    vector_b = np.array(vector_b)

    dot_product = np.dot(vector_a, vector_b)

    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)

    similarity = dot_product / (magnitude_a * magnitude_b)

    return similarity

def retrieve_chunks(question, chunks, client, top_k=3):
    
    # Function to retrieve the most relevant chunks of text based on a question using cosine similarity
    # Only used during development for learning purposes, not used in the final product

    question_embedding = create_embedding(question, client) # Create an embedding for the question
    results = []                                            # Initialize an empty list to store the similarity results

    for chunk in chunks:

        chunk_embedding = create_embedding(chunk["text"], client)               # Create an embedding for the current chunk of text
        similarity = cosine_similarity(question_embedding, chunk_embedding)     # Calculate the cosine similarity between the question embedding and the chunk embedding

        results.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "similarity": similarity
        })
    
    sorted_results = sorted(
        results,                                # Sort the results list
        key=lambda item: item["similarity"],    # Use the similarity score as the sorting key
        reverse=True                            # Sort in descending order
    )

    return sorted_results[:top_k]