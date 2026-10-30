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

# Embedding and getting results for query
def chroma_db_embedd_and_store_chunks(chunks, query):
    client = chromadb.Client()
    collection = client.create_collection(name="General_Knowledge")
    collection.add(
        ids = [f"chunk_{i}" for i in range(len(chunks))],
        documents = [chunk["text"] for chunk in chunks],
        metadatas=[{"source": chunk["source"]} for chunk in chunks]
    )

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

# Storing all chunks
all_chunks = extract_from_pdf(doc_list)
print(all_chunks)
query = ["What is python?", "give any advice for financial management"]

# Passing query and chunks to embedd and find the best match
results = chroma_db_embedd_and_store_chunks(all_chunks, query)
context = chromadb_top_context(results)

# Calling resuable function called feed the top result contexts and query to the GEMINI AI
# And getting response from the provided content through GEMINI AI
rag_def.generate_answer(query, context)