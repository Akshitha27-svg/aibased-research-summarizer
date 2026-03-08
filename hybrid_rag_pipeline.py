import faiss
import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# =====================================
# 1️⃣ Load Embedding Model
# =====================================
print("Loading embedding model...")
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# =====================================
# 2️⃣ Load FAISS Index
# =====================================
print("Loading FAISS index...")
index = faiss.read_index("faiss_index.index")

# =====================================
# 3️⃣ Load Metadata
# =====================================
print("Loading metadata...")
metadata = pd.read_csv("metadata.csv")

# =====================================
# 4️⃣ Load LLM
# =====================================
print("Loading LLM...")
model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

print("\nHybrid RAG System Ready 🚀")

# =====================================
# 5️⃣ Query Loop
# =====================================
while True:
    query = input("\nEnter your research question (or type 'exit'): ")

    if query.lower() == "exit":
        break

    # =====================================
    # 🔹 Generate Query Embedding
    # =====================================
    print("\nGenerating query embedding...")
    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    # =====================================
    # 🔹 Search FAISS
    # =====================================
    print("Searching FAISS...")
    k = 8
    distances, indices = index.search(query_embedding, k)

    retrieved_chunks = []
    source_papers = set()

    for idx in indices[0]:
        row = metadata.iloc[idx]
        retrieved_chunks.append(row["chunk"])
        source_papers.add(row["paper_name"])

    retrieved_context = "\n\n".join(retrieved_chunks)

    # =====================================
    # 🔹 Strong Academic Prompt
    # =====================================
    prompt = f"""
You are a senior academic researcher.

Using ONLY the provided research context,
write a comprehensive and detailed academic explanation
in ONE large paragraph (minimum 250 words).

The paragraph must:
- Explain the research objective clearly
- Describe techniques or methodology
- Discuss findings or results
- Explain real-world implications
- Be analytical and in-depth

Do NOT write a short answer.
Do NOT summarize in one sentence.
Write a full academic paragraph.

Research Question:
{query}

Context:
{retrieved_context}
"""

    print("Generating summary using LLM...\n")

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    ).to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=600,
            min_new_tokens=250,   # 🔥 force long output
            temperature=0.8,
            do_sample=True,
            top_p=0.95,
            repetition_penalty=1.2
        )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # =====================================
    # 🔟 Evaluation Metrics
    # =====================================

    # ---- Retrieval Evaluation ----
    avg_distance = float(np.mean(distances))

    # ---- Query-Answer Relevance ----
    query_emb = embedding_model.encode(query, convert_to_numpy=True)
    answer_emb = embedding_model.encode(generated_text, convert_to_numpy=True)

    query_emb = query_emb / np.linalg.norm(query_emb)
    answer_emb = answer_emb / np.linalg.norm(answer_emb)

    qa_similarity = np.dot(query_emb, answer_emb)
    qa_confidence = round(float(qa_similarity) * 100, 2)

    # ---- Grounding Score (Answer vs Retrieved Chunks) ----
    chunk_embeddings = embedding_model.encode(retrieved_chunks, convert_to_numpy=True)

    # Normalize
    chunk_embeddings = chunk_embeddings / np.linalg.norm(chunk_embeddings, axis=1, keepdims=True)
    answer_emb_norm = answer_emb

    grounding_scores = np.dot(chunk_embeddings, answer_emb_norm)
    grounding_confidence = round(float(np.mean(grounding_scores)) * 100, 2)

    # =====================================
    # 📊 Display Results
    # =====================================
    print("\n==============================")
    print("FINAL GENERATED SUMMARY")
    print("==============================\n")
    print(generated_text)

    print("\nSources Used:")
    for paper in source_papers:
        print("-", paper)

    print("\n==============================")
    print("EVALUATION METRICS")
    print("==============================")

    print("\nRetrieval Evaluation:")
    print("Average Similarity Distance:", avg_distance)

    print("\nGeneration Evaluation:")
    print("Character Length:", len(generated_text))
    print("Word Count:", len(generated_text.split()))

    print("\nEnd-to-End Query Relevance Score:",
          qa_confidence, "%")

    print("Grounding Confidence Score:",
          grounding_confidence, "%")
