import os, json
from sentence_transformers import SentenceTransformer, util

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
    model = SentenceTransformer('all-MiniLM-L6-V2')
    return model.encode(text)

# Compute the cosine similarity between the query embedding and each paragraph embedding
def str_query_high_similarity(query_embedding, paragraph_embeddings):
    for query_embedded in query_embedding:
        similarity_scores = util.cos_sim(query_embedded, paragraph_embeddings)[0]
        similarity_high = similarity_scores.argmax()  # Get the index of the paragraph with the highest similarity score
        return similarity_high