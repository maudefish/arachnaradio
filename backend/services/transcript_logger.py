from pyprojroot import here
import csv
import re
from datetime import datetime
from pathlib import Path
import os
from backend.utils.time_utils import extract_timestamp

TRANSCRIPT_LOG_PATH = here("data/logs/all_transcripts.csv")


def clean_transcript(transcript) -> str:
    if not isinstance(transcript, str):
        return ""

    # Remove Whisper-style timestamps
    text = re.sub(r"\[\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\]", "", transcript)
    # Remove [MUSIC], [APPLAUSE], etc.
    # text = re.sub(r"\[(MUSIC|APPLAUSE|LAUGHTER|NOISE|SILENCE)\]", "", text, flags=re.IGNORECASE)
    # Normalize whitespace
    return re.sub(r"\s+", " ", text).strip()


def log_transcript(
    filename: str,
    transcript: str,
    cleaned: str,
    station: str = "KALX",
    contains_music: bool = False,
    contains_venue: bool = False,
    contains_artist: bool = False,
    llm_summary_ready: bool = False
):
    TRANSCRIPT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = extract_timestamp(filename)

    fieldnames = [
        "timestamp", "station", "filename", "transcript", "cleaned",
        "contains_music", "contains_venue", "contains_artist", "llm_summary_ready"
    ]

    file_exists = TRANSCRIPT_LOG_PATH.exists()
    is_empty = os.path.getsize(TRANSCRIPT_LOG_PATH) == 0 if file_exists else True

    with open(TRANSCRIPT_LOG_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if is_empty:
            writer.writeheader()

        writer.writerow({
            "timestamp": timestamp,
            "station": station,
            "filename": filename,
            "transcript": transcript,
            "cleaned": cleaned,
            "contains_music": contains_music,
            "contains_venue": contains_venue,
            "contains_artist": contains_artist,
            "llm_summary_ready": llm_summary_ready
        })