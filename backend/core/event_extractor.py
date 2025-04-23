from pathlib import Path
from datetime import datetime
from typing import List, Dict
import csv
import re
import json

# --- Configuration ---
PARSED_EVENTS_PATH = Path("data/logs/parsed_events.csv")

def extract_timestamp_from_filename(filename: str) -> str:
    match = re.search(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}", Path(filename).name)
    if match:
        dt = datetime.strptime(match.group(), "%Y-%m-%d_%H-%M-%S")
        return dt.strftime("%Y-%m-%dT%H:%M:%S")

def normalize_event_fields(event: dict) -> dict:
    """
    Ensure that all values in the event are strings, flattening lists.
    """
    normalized = {}
    for key, value in event.items():
        if isinstance(value, list):
            normalized[key] = ", ".join(str(v) for v in value)
        else:
            normalized[key] = str(value)
    return normalized

def extract_rows_from_summary(summary: str, station: str, filename: str) -> List[Dict]:
    # print("🔍 Raw LLM Summary:\n", summary)

    # 1. Clean illegal trailing commas
    cleaned = re.sub(r",(\s*[\}\]])", r"\1", summary.strip())

    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, list):
            normalized = []
            for item in parsed:
                # Ensure dict, flatten all values
                if isinstance(item, dict):
                    item.setdefault("timestamp", extract_timestamp_from_filename(filename))
                    item.setdefault("station", station)
                    item.setdefault("filename", filename)
                    flat = normalize_event_fields(item)
                    normalized.append(flat)
            return normalized
        else:
            print("⚠️ Unexpected format (not a list)")
            return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed after cleaning: {e}")
        return []

def append_events_to_csv(events: List[Dict]) -> None:
    PARSED_EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = PARSED_EVENTS_PATH.exists()

    with open(PARSED_EVENTS_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "artist", "venue", "date", "station", "filename"
        ])
        if not file_exists:
            writer.writeheader()
        for event in events:
            writer.writerow(event)


# EXAMPLE USAGE:
# summary_text = llm_output
# filename = "data/audio_clip.mp3"
# station = "KALX"
# events = extract_rows_from_summary(summary_text, station, filename)
# append_events_to_csv(events)

