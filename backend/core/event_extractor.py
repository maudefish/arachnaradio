from pathlib import Path
from datetime import datetime
from typing import List, Dict
import csv
import re
import json
from backend.core.alias_resolver import resolve_canonical_name

# --- Configuration ---
PARSED_EVENTS_PATH = Path("data/logs/parsed_events.csv")

def normalize_event_fields(event: dict) -> dict:
    normalized = event.copy()
    print(f"\nnormalized:{normalized}\n")

    if "venue" in normalized and isinstance(normalized["venue"], str):
        original = normalized["venue"]
        canonical = resolve_canonical_name(original)
        normalized["venue_original"] = original
        normalized["venue"] = canonical

    return normalized


def extract_timestamp_from_filename(filename: str) -> str:
    match = re.search(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}", Path(filename).name)
    if match:
        dt = datetime.strptime(match.group(), "%Y-%m-%d_%H-%M-%S")
        return dt.strftime("%Y-%m-%dT%H:%M:%S")

def flatten_event_fields(event: dict) -> dict:
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
    cleaned = re.sub(r",(\s*[\}\]])", r"\1", summary.strip())

    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, list):
            normalized = []
            for item in parsed:
                if isinstance(item, dict):
                    item.setdefault("timestamp", extract_timestamp_from_filename(filename))
                    item.setdefault("station", station)
                    item.setdefault("filename", filename)

                    # Canonicalize venue BEFORE flattening
                    # item = normalize_event_fields(item)

                    flat = flatten_event_fields(item)
                    normalized.append(flat)
            return normalized
        else:
            print("⚠️ Unexpected format (not a list)")
            return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed after cleaning: {e}")
        return []
    return []

def append_events_to_csv(events: List[Dict], path: Path = PARSED_EVENTS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = path.exists()

    fieldnames = [
        "timestamp", "artist", "venue", "venue_original", "date", "station", "filename"
    ]

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        for event in events:
            # Ensure all required keys are present
            row = {field: str(event.get(field, "")) for field in fieldnames}
            writer.writerow(row)



