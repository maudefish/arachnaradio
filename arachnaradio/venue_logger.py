import csv
from datetime import datetime
from pathlib import Path
import pandas as pd
from typing import List
from alias_resolver import resolve_venue_name


LOG_PATH = Path("data/logs/venue_mentions.csv")
MASTER_VENUE_PATH = Path("data/venues_master.csv")

# Load master venue data
venue_coords = pd.read_csv(MASTER_VENUE_PATH)

def get_coords_for_venue(venue_name: str):
    row = venue_coords[venue_coords["name"].str.lower() == venue_name.lower()]
    if not row.empty:
        return row.iloc[0]["lat"], row.iloc[0]["lon"]
    return None, None

def mentioned_venues(transcript: str, venue_list: List[str]) -> List[str]:
    transcript_lower = transcript.lower()
    matched = []
    for venue in venue_list:
        aliases = resolve_venue_name(venue)
        if any(alias.lower() in transcript_lower for alias in aliases):
            matched.append(venue)
    return matched
    
def log_venue_mention(filename: str, transcript: str, station: str, venues: List[str]):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    file_exists = LOG_PATH.exists()
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "station", "filename", "venue", "lat", "lon", "transcript"])
        
        # Only log each venue once per transcript
        logged = set()
        for venue in venues:
            if venue.lower() in logged:
                continue
            lat, lon = get_coords_for_venue(venue)
            writer.writerow([timestamp, station, filename, venue, lat, lon, transcript])
            logged.add(venue.lower())

    print(f"📍 Logged venue mention(s): {', '.join(set(venues))}")
