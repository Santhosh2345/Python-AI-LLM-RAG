from python.LLMLearn.RAG_Chromadb import ingest_documents as ingestDoc
from python.LLMLearn.RAG_LLM_Learn import RAG_Reuseable_Def as rag_def
import os
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# # Chromdb was created in the ingest_documents.py file
# client = chromadb.PersistentClient(path="./chroma_db")
# collection = client.get_or_create_collection(ingestDoc.chroma_db_name)

# Load the chromadb to LlamaIndex
vector_store = ChromaVectorStore(
    chroma_collection=ingestDoc.collection
)

# Configure Gemini
Settings.llm = GoogleGenAI(
    model=rag_def.genai_model,
    api_key=os.environ["GEMINI_API_KEY"]
)

# Configure the same embedding model used by ChromaDB's default
# embedding function
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create an index interface over existing vectors
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store
)

query_engine = index.as_query_engine(
    similarity_top_k=3
)

def ask_question(question: str):
    response = query_engine.query(question)
    return response

while True:
    question = input("\nAsk a question (or type exit): ")

    if question.lower() == "exit":
        break

    response = ask_question(question)
    print(f'\nAnwer: \n{response}')