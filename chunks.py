import pandas as pd
import numpy as np

# Load metadata
metadata = pd.read_csv("Metadata.csv")

# Extract chunks
chunks = metadata["chunk"].tolist()

# Save chunks for FAISS alignment
np.save("chunk_texts.npy", chunks)

print("✅ chunk_texts.npy created successfully!")