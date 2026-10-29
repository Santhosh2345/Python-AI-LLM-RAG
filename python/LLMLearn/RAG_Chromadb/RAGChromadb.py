from pypdf import PdfReader
import os, json

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
    
context = extract_from_pdf(doc_list)
print(context)