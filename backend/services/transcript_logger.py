from pyprojroot import here
import csv
from datetime import datetime
from pathlib import Path
import os
from backend.utils.time_utils import extract_timestamp

TRANSCRIPT_LOG_PATH = here("data/logs/all_transcripts.csv")

def log_transcript(filename: str, transcript: str, station: str = "KALX",
                   contains_music=False, contains_venue=False,
                   contains_artist=False, llm_summary_ready=False):
    TRANSCRIPT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    timestamp = extract_timestamp(filename)

    file_exists = TRANSCRIPT_LOG_PATH.exists()
    is_empty = os.path.getsize(TRANSCRIPT_LOG_PATH) == 0 if file_exists else True

    with open(TRANSCRIPT_LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if is_empty:
            writer.writerow([
                "timestamp", "station", "filename", "transcript",
                "contains_music", "contains_venue", "contains_artist", "llm_summary_ready"
            ])
        writer.writerow([
            timestamp, station, filename, transcript,
            contains_music, contains_venue, contains_artist, llm_summary_ready
        ])
