import os
import fitz  # PyMuPDF
import faiss
import numpy as np
import pandas as pd
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# =====================================
# SETTINGS
# =====================================
PDF_FOLDER = "pdfs"  # your folder name
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# =====================================
# Load Embedding Model
# =====================================
print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

documents = []
metadata_rows = []

# =====================================
# Function: Extract Text from PDF
# =====================================
def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# =====================================
# Function: Chunk Text
# =====================================
def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# =====================================
# Process PDFs
# =====================================
print("Processing PDFs...")

for filename in tqdm(os.listdir(PDF_FOLDER)):
    if filename.endswith(".pdf"):
        path = os.path.join(PDF_FOLDER, filename)
        text = extract_text_from_pdf(path)

        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

        for chunk in chunks:
            documents.append(chunk)
            metadata_rows.append({
                "paper_name": filename,
                "chunk": chunk
            })

print(f"Total chunks created: {len(documents)}")

# =====================================
# Create Embeddings
# =====================================
print("Generating embeddings...")
embeddings = model.encode(documents, show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

# =====================================
# Build FAISS Index
# =====================================
print("Building FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "faiss_index.index")
print("FAISS index saved.")

# =====================================
# Save Metadata
# =====================================
metadata_df = pd.DataFrame(metadata_rows)
metadata_df.to_csv("metadata.csv", index=False)
print("metadata.csv saved.")

print("✅ Index building complete!")
