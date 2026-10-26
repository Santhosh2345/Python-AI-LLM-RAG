import os, json
from sentence_transformers import SentenceTransformer, util
from google import genai
from google.genai import types

genai_model="gemini-3.5-flash-lite"
model = SentenceTransformer('all-MiniLM-L6-V2')
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

usage = None

# This function generates an answer to a query based on the provided context using the GenAI model.
def generate_answer(query, context):
    question = "\n".join(
        f"{i}. {question}"
        for i, question in enumerate(query, start=1)
    )
    prompt = f"""
    Answer the question using only the context provided.
    If the answer is not available in the context, say so.

    Context:
    {context}

    Question:
    {question}
    """

    chat = client.chats.create(
                model=genai_model,
                config=types.GenerateContentConfig(
                    max_output_tokens=100,
                    automatic_function_calling=(
                        types.AutomaticFunctionCallingConfig(
                        disable=False
                        )
                    )
                )
            )
    
    print("GenAI response: ")
            
    for chunk in chat.send_message_stream(prompt):
        if chunk.text:
            print(chunk.text, end="", flush=True)

    if chunk.usage_metadata:
        usage = chunk.usage_metadata

    print()  # Move to the next line after streaming

    if usage:
        print("Prompt tokens:", usage.prompt_token_count)
        print("Response tokens:", usage.candidates_token_count)
        print("Total tokens:", usage.total_token_count)

# Split the document into paragraphs
def chunk_by_paragraph(texts):
    return [text.strip() for text in texts.split('\n\n') if text.strip()]

# Split the document into sentences and store in a list fixed length of 20 sentences per chunk
def chunk_by_sentence(texts, chunk_size=20):
    chunk = []
    for i in range(0, len(texts), chunk_size):
        chunk.append(texts[i:i+chunk_size])
    print(f'Chunked sentences: {chunk}')
    return chunk

# Split the document into sentences and store in a list fixed length of 20 sentences per chunk with a overlap of 10 characters stored in a list
def chunk_by_sentence(texts, chunk_size=20, step=10):
    chunk = []
    for i in range(0, len(texts), step):
        chunk.append((texts[i:i+chunk_size]))
    print(f'Chunked sentences: {chunk}')
    return chunk

# Embedding the text using SentenceTransformer model
def embedding_text(text):
    return model.encode(text)

# Compute the cosine similarity between the query embedding and each paragraph embedding
def query_high_similarity(queries, paragraph_embeddings):
    top_indices = []
    for query in queries:
        query_embedding = model.encode(query)
        similarity_scores = util.cos_sim(query_embedding, paragraph_embeddings)[0]
        top_indices.append(similarity_scores.argmax().item())
    print(f'Top indices of high similarity: {top_indices}')
    return top_indices
        