from python.LLMLearn.RAG_LLM_Learn import RAG_Reuseable_Def as rag_def
import python.LLMLearn.RAG_Chromadb.ingest_documents as chroma_db

def main():
    while True:
        query = []
        user_query = input("\nAsk me a question (or type exit): ").lower()

        if user_query == "exit":
            break

        query.append(user_query)

        # Passing query and finding the best match
        results = chroma_db.search_chunks(query)
        context = chroma_db.chromadb_top_context(results)

        # Calling resuable function called feed the top result contexts and query to the GEMINI AI
        # And getting response from the provided content through GEMINI AI
        rag_def.generate_answer(query, context)

if __name__ == "__main__":
    main()