from python.LLMLearn.RAG_LLM_Learn import RAG_Reuseable_Def as rag_def
from pypdf import PdfReader
import os, json
import chromadb

# Find Document directory
doc_dir = os.path.join(os.getcwd(), "Documents")
print(doc_dir)

# Storing all the pdf files available in the Document directory
doc_list = [
    file for file in os.listdir(doc_dir)
    if file.lower().endswith(".pdf")
]

# Chunking the given text by paragraph
def chunk_by_size_overlap(texts, chunk_size=150, overlap=115):
    chunks = []
    for i in range(0, len(texts), overlap):
        chunks.append(texts[i:i+chunk_size])
    return chunks

# Extracting the text from the PDF and storing the chunks as source-wise
def extract_from_pdf(documents):
    all_chunks = []
    text = ""
    for document in documents:
        reader = PdfReader(os.path.join(doc_dir, document))
        extracted_text = "\n\n".join(page.extract_text() or " " for page in reader.pages)

        chunks = chunk_by_size_overlap(extracted_text)
        for chunk in chunks:
            all_chunks.append({
                    "text": chunk,
                    "source": document
                })
    
    return all_chunks

client = chromadb.PersistentClient(path="./choma_db")
chroma_db_name = "General_Knowledge"
collection = client.get_or_create_collection(name=chroma_db_name)
print("Total stored chunks:", collection.count())

# Embedding and and storing the chunks in local file chorma_db
def chroma_db_embedd_and_store_chunks(chunks):
    collection.upsert(
        ids = [f"chunk_{i}" for i in range(len(chunks))],
        documents = [chunk["text"] for chunk in chunks],
        metadatas=[{"source": chunk["source"]} for chunk in chunks]
    )
    print("Chunks are stored successfully in the chormadb")

# Searching related chunks and return the results
def search_chunks(query):
    results = collection.query(
        query_texts=query,
        n_results=2
    )

    return results

# Getting best results from the chroma db tools
def chromadb_top_context(results):
    top_context = []
    for query_index, documents in enumerate(results["documents"]):
        distances = results["distances"][query_index]
        for doc, dist in zip(documents, distances):
            print(f'{dist: .3f}: {doc}')
            top_context.append(doc)
    return top_context

if __name__ == "__main__":
    # Extract PDF text
    all_chunks = extract_from_pdf(doc_list)
    print(all_chunks)

    # Save embeddings and documents in ChromaDB
    chroma_db_embedd_and_store_chunks(all_chunks)