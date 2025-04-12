# arachnaradio/venue_logger.py

import csv
from datetime import datetime
from pathlib import Path
import pandas as pd
from typing import List


LOG_PATH = Path("data/logs/venue_mentions.csv")
COORDS_PATH = Path("data/venue_locations.csv")

# Load venue coordinates once
venue_coords = pd.read_csv(COORDS_PATH)

def get_coords_for_venue(venue_name: str):
    row = venue_coords[venue_coords["venue"].str.lower() == venue_name.lower()]
    if not row.empty:
        return row.iloc[0]["lat"], row.iloc[0]["lon"]
    return None, None

def mentioned_venues(transcript: str, venue_list: List[str]) -> List[str]:
    return [venue for venue in venue_list if venue.lower() in transcript.lower()]

def log_venue_mention(filename: str, transcript: str, station: str, venues: List[str]):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    file_exists = LOG_PATH.exists()
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "station", "filename", "venue", "lat", "lon", "transcript"])
        for venue in venues:
            lat, lon = get_coords_for_venue(venue)
            writer.writerow([timestamp, station, filename, venue, lat, lon, transcript])

    print(f"📍 Logged venue mention(s): {', '.join(venues)}")
