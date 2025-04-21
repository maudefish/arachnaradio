import pandas as pd
import re
from pathlib import Path

# === CONFIG ===
CSV_PATH = Path("data/logs/venue_mentions.csv")
OUTPUT_PATH = Path("data/logs/venue_mentions_enriched.csv")

# === SIMPLE PARSING HELPERS ===

def extract_artist(transcript: str) -> str:
    """
    Extract likely artist names using basic patterns like:
    - 'performing with <artist>'
    - 'playing with <artist>'
    - 'featuring <artist>'
    """
    patterns = [
        r"performing with ([A-Z][\w\s&'-]+)",
        r"playing with ([A-Z][\w\s&'-]+)",
        r"featuring ([A-Z][\w\s&'-]+)",
        r"performing at [\w\s]+ with ([A-Z][\w\s&'-]+)",
        r"set from ([A-Z][\w\s&'-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, transcript, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return "Unknown Artist"

def extract_date(transcript: str) -> str:
    """
    Extract likely date phrases like:
    - 'on Friday, April 18th'
    - 'Saturday April 20'
    """
    match = re.search(
        r"(on\s+)?(?P<weekday>Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)[,\s]+(?P<month>\w+)\s+(?P<day>\d{1,2})(?:st|nd|rd|th)?",
        transcript,
        flags=re.IGNORECASE
    )
    if match:
        weekday = match.group("weekday")
        month = match.group("month")
        day = match.group("day")
        return f"{weekday}, {month} {day}"
    return "Unknown Date"

# === MAIN FUNCTION ===
def enrich_venue_mentions():
    if not CSV_PATH.exists():
        print(f"❌ File not found: {CSV_PATH}")
        return

    df = pd.read_csv(CSV_PATH)

    if "transcript" not in df.columns:
        print("❌ Missing 'transcript' column.")
        return

    print("🔍 Parsing transcripts...")

    df["artist"] = df["transcript"].apply(extract_artist)
    df["event_date"] = df["transcript"].apply(extract_date)

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Enriched file saved to: {OUTPUT_PATH}")

# === RUN ===
if __name__ == "__main__":
    enrich_venue_mentions()
