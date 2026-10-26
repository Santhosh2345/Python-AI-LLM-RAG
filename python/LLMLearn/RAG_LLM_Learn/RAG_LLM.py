import RAG_Reuseable_Def as rag_def

#1. Store the sentence in the variable document
document = '''Bees collect pollen grains from flowers as they search for nectar. Pollen sticks to their fuzzy bodies and legs.

The pollen grain germinates and grows a tiny pollen tube down toward the ovule.

This allows fertilization to occur, helping the flower produce seeds and continue its life cycle.

When a bee visits another flower, some pollen grains rub off onto its sticky stigma, the female part of the flower.

'''
paragraphs = rag_def.chunk_by_paragraph(document)
query = ["How do bees help flowers reproduce?",
         "What is the role of pollen in fertilization?"]

#3. Print the paragraphs to confirm they are splited correctly
for i, paragraph in enumerate(paragraphs):
    print(f'Paragraph {i+1}: {paragraph}')

#4. Embed the paragraphs and the query using the embedding_text function
paragraph_embeddings = rag_def.embedding_text(paragraphs)

#5. Compute the cosine similarity between the query embedding and each paragraph embedding using the str_query_high_similarity function
high_similarity_indices = rag_def.query_high_similarity(query, paragraph_embeddings)
print(f'Query: {query}')
best_match_paragraphs = [paragraphs[i] for i in high_similarity_indices]
context = "\n\n".join(best_match_paragraphs)
rag_def.generate_answer(query, context)

