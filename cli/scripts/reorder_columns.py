import pandas as pd

desired_order = [
    "timestamp", "station", "filename", "transcript", "cleaned",
    "contains_music", "contains_venue", "contains_artist", "llm_summary_ready"
]

df = pd.read_csv("data/logs/all_transcripts.csv")

# Reorder if all desired columns are present
if all(col in df.columns for col in desired_order):
    df = df[desired_order]
    df.to_csv("data/logs/all_transcripts.csv", index=False)
    print("✅ Columns reordered.")
else:
    print("⚠️ Not all desired columns found. Skipping reorder.")
