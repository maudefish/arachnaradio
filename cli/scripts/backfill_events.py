import pandas as pd
from pathlib import Path
from llm_helper import generate_event_summary
from event_extractor import extract_rows_from_summary, append_events_to_csv

# Paths
MENTIONS_PATH = Path("data/logs/venue_mentions.csv")

# Load the existing mentions
df = pd.read_csv(MENTIONS_PATH)

# Track new parsed event rows
all_events = []

for i, row in df.iterrows():
    transcript = row.get("transcript", "")
    filename = row.get("filename", "unknown.mp3")
    station = row.get("station", "Unknown Station")

    if not transcript.strip():
        continue

    print(f"🧠 Parsing row {i+1}/{len(df)}: {filename}")

    # Run LLM summarization
    summary = generate_event_summary(transcript, station)

    # Extract structured info
    parsed = extract_rows_from_summary(summary, station, filename)

    if parsed:
        all_events.extend(parsed)
    else:
        print(f"⚠️ No events extracted from summary: {summary}")

# Append to parsed CSV
if all_events:
    append_events_to_csv(all_events)
    print(f"✅ Added {len(all_events)} new event rows to parsed_events.csv")
else:
    print("🚫 No new events parsed.")
