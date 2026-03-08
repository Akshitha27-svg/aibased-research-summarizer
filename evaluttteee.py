import pandas as pd
import numpy as np

chunks = pd.read_csv("chunks.csv")

print("Total Papers:", chunks['Paper_ID'].nunique())
print("Total Chunks:", len(chunks))
print("Average Chunk Length:", chunks['chunk_text'].apply(len).mean())
