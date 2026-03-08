import os
import pandas as pd
from pypdf import PdfReader

# Folder containing PDFs
PDF_FOLDER = "research_papers"

# Chunk settings
CHUNK_SIZE = 300
OVERLAP = 50

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
    
    return chunks

all_chunks = []

for filename in os.listdir(PDF_FOLDER):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(PDF_FOLDER, filename)
        print(f"Processing: {filename}")
        
        text = extract_text_from_pdf(pdf_path)
        
        if text.strip():
            chunks = chunk_text(text, CHUNK_SIZE, OVERLAP)
            
            for chunk in chunks:
                all_chunks.append({
                    "paper_name": filename,
                    "chunk": chunk
                })

chunks_df = pd.DataFrame(all_chunks)
chunks_df.to_csv("chunks.csv", index=False)

print("\nChunking completed successfully!")
print(f"Total chunks created: {len(all_chunks)}")
