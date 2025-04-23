import csv
from datetime import datetime
from pathlib import Path
from typing import List

MENTION_LOG = Path("data/logs/artist_mentions.csv")

def ensure_log_file():
    if not MENTION_LOG.parent.exists():
        MENTION_LOG.parent.mkdir(parents=True)
    if not MENTION_LOG.exists():
        with open(MENTION_LOG, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "station", "filename", "transcript", "mentioned_artists"])

def log_mention(filename: str, transcript: str, station: str, matches: List[str]):
    ensure_log_file()
    with open(MENTION_LOG, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            station,
            filename,
            transcript,
            ";".join(matches)
        ])

def mentioned_artists(transcript: str, artist_list: List[str]) -> List[str]:
    transcript_lower = transcript.lower()
    return [artist for artist in artist_list if artist.lower() in transcript_lower]