import RAG_Reuseable_Def as rag_def

#1. Store the sentence in the variable document
document = '''Bees collect pollen grains from flowers as they search for nectar. Pollen sticks to their fuzzy bodies and legs.

When a bee visits another flower, some pollen grains rub off onto its sticky stigma, the female part of the flower. 

    The pollen grain germinates and grows a tiny pollen tube down toward the ovule. This allows fertilization to occur, helping the flower produce seeds and continue its life cycle.

'''
paragraphs = rag_def.chunk_by_paragraph(document)
query = "How do bees help flowers reproduce?"

#3. Print the paragraphs to confirm they are splited correctly
for i, paragraph in enumerate(paragraphs):
    print(f'Paragraph {i+1}: {paragraph}')

#4. Embed the paragraphs and the query using the embedding_text function
paragraph_embeddings = rag_def.embedding_text(paragraphs)
query_embedding = rag_def.embedding_text([query])

#5. Compute the cosine similarity between the query embedding and each paragraph embedding using the str_query_high_similarity function
high_similarity_index = rag_def.str_query_high_similarity(query_embedding, paragraph_embeddings)
print(f'Query: {query}')
print(f'Best match paragraph: {paragraphs[high_similarity_index]}')