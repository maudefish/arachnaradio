import pandas as pd
from backend.services.transcript_logger import clean_transcript  # or redefine here

df = pd.read_csv("data/logs/all_transcripts.csv")

# Add 'stripped' column if missing
if "cleaned" not in df.columns:
    df["cleaned"] = df["transcript"].apply(clean_transcript)
    df.to_csv("data/logs/all_transcripts.csv", index=False)
    print("✅ Added 'cleaned' column to existing log.")
else:
    print("ℹ️ 'cleaned' column already exists.")
