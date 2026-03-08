ResearchAnalyzer – AI Research Paper Assistant

"Python" (https://img.shields.io/badge/Python-3.10-blue)
"Gradio" (https://img.shields.io/badge/UI-Gradio-orange)
"FAISS" (https://img.shields.io/badge/VectorDB-FAISS-green)
"Transformers" (https://img.shields.io/badge/HuggingFace-Transformers-yellow)
"License" (https://img.shields.io/badge/License-MIT-lightgrey)

An AI-powered Research Paper Assistant that allows users to chat with academic papers and generate structured summaries using a Retrieval-Augmented Generation (RAG) pipeline.

---

Live Application

Try the deployed app on Hugging Face Spaces:

https://huggingface.co/spaces/chinaksh/ResearchAnalyzer

---



Research Paper Summarizer

docs/summarizer.png

"Summarizer" (docs/summarizer.png)

---

Features

- Chat with research papers
- Upload custom research PDFs
- Semantic search retrieval
- Automatic research paper summarization
- Confidence score for answers
- Conversation memory
- Split interface for chat and summarizer

---

Technologies Used

Gradio

Interactive UI framework used to build the web interface.

Sentence Transformers

Used to convert document chunks into embeddings.

Model used:

sentence-transformers/all-MiniLM-L6-v2

---

FAISS

Vector similarity search engine used to retrieve relevant document chunks.

---

FLAN-T5

Language model used to generate contextual answers and summaries.

Model used:

google/flan-t5-base

---

PyMuPDF

Used for extracting text from PDF research papers.

---

System Architecture

User Query
     ↓
Text Embedding
     ↓
Vector Search (FAISS)
     ↓
Relevant Paper Chunks
     ↓
Language Model (FLAN-T5)
     ↓
Generated Answer

---

RAG Workflow

User Question
      ↓
Sentence Transformer Embedding
      ↓
FAISS Vector Database
      ↓
Top Relevant Chunks
      ↓
FLAN-T5 Language Model
      ↓
Final Generated Answer

---

Project Structure

ResearchAnalyzer/

app.py
requirements.txt
README.md

metadata.csv
faiss_index.index

pdfs/
   Research paper -1.pdf
   Research paper -2.pdf


documentation/
   Agile_Template.xlsx
   Defect_Tracker.xlsx
   Unit_Test_Plan.xlsx

---

File Description

app.py

Main application script responsible for:

- Loading embedding models
- Loading FAISS index
- Handling chat interactions
- Processing PDF uploads
- Performing document retrieval
- Generating answers and summaries
- Running the Gradio interface

---

metadata.csv

Stores extracted text chunks and their associated research papers.

Example:

paper_name,chunk
paper1,"text chunk"
paper1,"another chunk"

---

faiss_index.index

Vector database containing embeddings used for similarity search.

---

requirements.txt

Python dependencies used in the project.

Example:

gradio
faiss-cpu
numpy
pandas
torch
sentence-transformers
transformers
pymupdf

---    hybrid_rag_pipeline.py: runs locally with all features

Installation

Clone the repository

git clone https://github.com/yourusername/ResearchAnalyzer.git

Navigate to the project directory

cd ResearchAnalyzer

Install dependencies

pip install -r requirements.txt

Run the application

python app.py

---

Deployment

The application is deployed using Hugging Face Spaces.

Deployment link:

https://huggingface.co/spaces/chinaksh/ResearchAnalyzer

Steps:

1. Create a new Hugging Face Space
2. Select SDK = Gradio
3. Upload project files
4. Hugging Face automatically builds and runs the application

---

Future Improvements

- Integrated PDF viewer
- Citation highlighting
- Multi-paper querying
- Improved summarization models
- Research topic clustering

---

Author

Chinmay Naksh

B.Tech – Artificial Intelligence and Machine Learning

---

License

MIT License
