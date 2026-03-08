import gradio as gr
import faiss
import numpy as np
import pandas as pd
import torch
import time
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# ==============================
# 🔹 Load Models
# ==============================

embedding_model = SentenceTransformer(
    "sentence-transformers/paraphrase-MiniLM-L3-v2"
)

index = faiss.read_index("faiss_index.index")
metadata = pd.read_csv("Metadata.csv")

model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

device = torch.device("cpu")
model.to(device)
model.eval()

# ==============================
# 🔹 RAG Function
# ==============================

def ask_question(question, selected_paper):

    if not question or not selected_paper:
        yield "Please enter a question and select a paper.", ""

    paper_chunks = metadata[metadata["paper_name"] == selected_paper]

    if paper_chunks.empty:
        yield "Selected paper not found.", ""

    chunk_texts = paper_chunks["chunk"].tolist()

    query_embedding = embedding_model.encode([question])
    query_embedding = np.array(query_embedding).astype("float32")

    chunk_embeddings = embedding_model.encode(chunk_texts)
    chunk_embeddings = np.array(chunk_embeddings).astype("float32")

    query_norm = query_embedding / np.linalg.norm(query_embedding)
    chunk_norm = chunk_embeddings / np.linalg.norm(
        chunk_embeddings, axis=1, keepdims=True
    )

    similarities = np.dot(chunk_norm, query_norm.T).flatten()
    retrieval_strength = float(np.max(similarities))

    if retrieval_strength < 0.45:
        yield "⚠️ This question is out of context for the selected paper.", ""
        return

    top_indices = similarities.argsort()[-3:][::-1]
    retrieved_chunks = [chunk_texts[i] for i in top_indices]
    retrieved_context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an advanced research assistant.

Write a detailed academic explanation 
in ONE well-structured paragraph (minimum 250 words).

Use ONLY the provided context.

Question:
{question}

Context:
{retrieved_context}
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=350,
            min_new_tokens=220,
            temperature=0.6,
            top_p=0.9,
            repetition_penalty=1.15,
            length_penalty=1.1,
            do_sample=True
        )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # ==============================
    # 🔥 ADVANCED CONFIDENCE SYSTEM
    # ==============================

    def normalize(v):
        return v / np.linalg.norm(v)

    q = normalize(embedding_model.encode(question, convert_to_numpy=True))
    a = normalize(embedding_model.encode(generated_text, convert_to_numpy=True))
    c = normalize(embedding_model.encode(retrieved_context, convert_to_numpy=True))

    qa = float(np.dot(q, a))
    qc = float(np.dot(q, c))
    ac = float(np.dot(a, c))

    raw_confidence = (
        0.35 * qa +
        0.25 * qc +
        0.25 * ac +
        0.15 * retrieval_strength
    )

    # Smart scaling to boost strong relevance
    confidence = round(min(100, max(0, raw_confidence * 130)), 2)

    # ==============================
    # 🔥 Animated Confidence UI
    # ==============================

    for i in range(0, int(confidence) + 1, 3):

        if i < 50:
            color = "#ff4d4d"
        elif i < 75:
            color = "#ffa500"
        else:
            color = "#00c853"

        html = f"""
        <div style="width:100%; background:#222; border-radius:15px;">
            <div style="
                width:{i}%;
                background:{color};
                padding:10px;
                border-radius:15px;
                text-align:center;
                color:white;
                font-weight:bold;
                font-size:18px;
                transition: width 0.3s;">
                {i}%
            </div>
        </div>
        """

        yield generated_text, html
        time.sleep(0.015)

# ==============================
# 🔹 PREMIUM UI DESIGN
# ==============================

papers = metadata["paper_name"].unique().tolist()

with gr.Blocks(theme=gr.themes.Monochrome()) as demo:

    gr.Markdown("""
    <h1 style="text-align:center;">🔬 Hybrid RAG Research Assistant</h1>
    <h3 style="text-align:center;">AI-Powered Contextual Academic Intelligence System</h3>
    <hr>
    """)

    with gr.Row():
        question_input = gr.Textbox(
            label="🔎 Enter Research Question",
            lines=3,
            placeholder="Ask something relevant to your selected research paper..."
        )

    paper_dropdown = gr.Dropdown(
        papers,
        label="📚 Select Research Paper"
    )

    submit_btn = gr.Button("🚀 Generate Intelligent Summary", variant="primary")

    gr.Markdown("### 📄 Generated Academic Summary")
    output_text = gr.Textbox(lines=12)

    gr.Markdown("### 📊 Relevance Confidence Score")
    confidence_output = gr.HTML()

    submit_btn.click(
        ask_question,
        inputs=[question_input, paper_dropdown],
        outputs=[output_text, confidence_output]
    )

demo.launch()