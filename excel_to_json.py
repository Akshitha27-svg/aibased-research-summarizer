import pandas as pd
import json
import os

print("📂 Current folder:", os.getcwd())

# ===== FILE NAMES (must match exactly) =====
CITATIONS_FILE = "Citations.xlsx"
REFERENCES_FILE = "Research_References.xlsx"

# ===== Load Excel safely =====
try:
    citations_df = pd.read_excel(CITATIONS_FILE, engine="openpyxl")
    print("✅ Loaded Citations.xlsx")
except Exception as e:
    print("❌ Error loading Citations.xlsx:", e)
    exit()

try:
    references_df = pd.read_excel(REFERENCES_FILE, engine="openpyxl")
    print("✅ Loaded Research_References.xlsx")
except Exception as e:
    print("❌ Error loading Research_References.xlsx:", e)
    exit()

# ===== Convert to JSON =====
citations_data = citations_df.to_dict(orient="records")
references_data = references_df.to_dict(orient="records")

# ===== Save JSON files =====
with open("citations.json", "w", encoding="utf-8") as f:
    json.dump(citations_data, f, indent=4)

with open("references.json", "w", encoding="utf-8") as f:
    json.dump(references_data, f, indent=4)

print("🎉 SUCCESS")
print("➡ citations.json created")
print("➡ references.json created")
