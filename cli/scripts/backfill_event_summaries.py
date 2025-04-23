import pandas as pd
from pathlib import Path
from llm_helper import generate_event_summary

# Path to the CSV
MENTIONS_PATH = Path("data/logs/venue_mentions.csv")

# Load CSV
if not MENTIONS_PATH.exists():
    print("❌ venue_mentions.csv not found.")
    exit()

df = pd.read_csv(MENTIONS_PATH)

# Add summary column if it doesn't exist
if "summary" not in df.columns:
    df["summary"] = ""

# Iterate and backfill
updated = False
for idx, row in df.iterrows():
    if pd.isna(row["summary"]) or row["summary"].strip() == "":
        transcript = row.get("transcript", "")
        station = row.get("station", "Unknown Station")
        summary = generate_event_summary(transcript, station)
        df.at[idx, "summary"] = summary
        updated = True
        print(f"✅ Row {idx} updated")

# Save back if changes made
if updated:
    df.to_csv(MENTIONS_PATH, index=False)
    print("✅ Backfilled missing summaries.")
else:
    print("🎉 All rows already have summaries.")
