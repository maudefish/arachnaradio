import csv
from pathlib import Path
from datetime import datetime

MISS_LOG_PATH = Path("data/logs/fuzzy_misses.csv")

def log_fuzzy_misses(unmatched: list, station: str, timestamp: str):
    """Append fuzzy match misses to a CSV for later review."""
    
    # Ensure CSV file exists with header
    if not MISS_LOG_PATH.exists():
        with MISS_LOG_PATH.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "station", "raw_phrase", 
                "normalized_phrase", "suggested_match", 
                "score", "geopy_match", "geopy_coords", 
                "matched_existing", "note"
            ])

    # Append entries
    with MISS_LOG_PATH.open("a", newline="") as f:
        writer = csv.writer(f)
        for suggested, phrase in unmatched:
            norm = phrase.lower().strip()
            writer.writerow([
                timestamp,
                station,
                phrase,
                norm,
                suggested,
                "",         # score (optional to calculate here)
                "",         # geopy_match
                "",         # geopy_coords
                "False",    # matched_existing
                "",         # note (for manual review)
            ])
