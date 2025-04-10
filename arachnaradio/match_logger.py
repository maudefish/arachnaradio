import csv
import os
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("data/logs")
LOG_FILE = LOG_DIR / "song_matches.csv"

# Create logs directory and header if needed
def ensure_log_file():
    if not LOG_DIR.exists():
        LOG_DIR.mkdir(parents=True)
    if not LOG_FILE.exists():
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "station", "filename",
                "title", "artist", "album",
                "score", "label", "play_offset_ms",
                "acrid", "genres"
            ])

def log_match(filepath: str, match: dict, station: str = "Unknown"):
    ensure_log_file()

    genres = ";".join(match.get("genres", [])) if match.get("genres") else ""

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            station,
            filepath,
            match.get("title"),
            match.get("artist"),
            match.get("album"),
            match.get("score"),
            match.get("label"),
            match.get("play_offset_ms"),
            match.get("acrid"),
            genres
        ])
