from pyprojroot import here
import csv
from datetime import datetime
from pathlib import Path
import pandas as pd
from typing import List, Tuple, Union
from backend.core.alias_resolver import resolve_canonical_name, normalize_name, get_aliases_from_yaml
from backend.core.llm_helper import generate_event_summary
from backend.data_io.writers import write_venue_log_row

PROJECT_ROOT = here()
LOG_PATH = here("data/logs/venue_mentions.csv")
MASTER_VENUE_PATH = here("data/masters/venues_geotagged.csv")

# Load master venue data
venue_coords = pd.read_csv(MASTER_VENUE_PATH)

def get_coords_for_venue(venue_name: str):
    row = venue_coords[venue_coords["name"].str.lower() == venue_name.lower()]
    if not row.empty:
        return row.iloc[0]["lat"], row.iloc[0]["lon"]
    return None, None

# def check_for_mentioned_venues(transcript: str, venue_list: List[str], return_aliases: bool = True) -> List[Tuple[str, str]]:
#     transcript_lower = transcript.lower()
#     matched = []

#     for venue in venue_list:
#         if venue.lower() in transcript_lower:
#             matched.append((venue, venue))  # both canonical and matched name are the same
#             # you can still use the same (venue, alias) format
#             # in case you reintroduce aliases later
#     return matched
def check_for_mentioned_venues(
                    transcript: str,
                    known_venues: List[str],
                    alias_data: dict,
                    return_aliases: bool = True
                ) -> List[Tuple[str, str]]:    
    transcript_clean = normalize_name(transcript)
    # print(f"\n\nDEBUG: transcript_clean output:\n\n {transcript_clean}")
    # print(f"\n\nDEBUG: alias_data output:\n\n {alias_data}")

    matched = []

    for canonical in known_venues:
        # resolved = resolve_canonical_name(canonical, alias_data, verbose=True)
        # print(f"\nDEBUG: canonical: {canonical}, resolved: {resolved} ")

        match_candidates = {normalize_name(canonical)} # These are just the normalized canonical names alone

        # # 👇 This should be the YAML key, so use `resolved`, not `normalize_name(...)`
        aliases = get_aliases_from_yaml(canonical, alias_data)

        match_candidates.update(normalize_name(a) for a in aliases) # This creates a larger candidate list from the aliases
        # print(match_candidates)

        for candidate in match_candidates:
            if candidate in transcript_clean:
                matched.append((canonical, candidate))
                break
        # print(matched)


    return matched

def log_venue_mention(
    filename: str,
    transcript: str,
    station: str,
    venues: List[Tuple[str, str]],
    alias_data: dict,
    master_names: list[str]
):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    master_names = venue_coords["name"].tolist()

    file_exists = LOG_PATH.exists()
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "station", "filename", "venue", "transcript", "lat", "lon"])

        logged = set()
        for canonical_name, matched_alias in venues:
            # canonical = resolve_canonical_name(canonical_name, verbose=True)
            canonical = canonical_name
            if canonical.lower() in logged:
                continue
            lat, lon = get_coords_for_venue(canonical)
            write_venue_log_row(writer, timestamp, station, filename, canonical_name, transcript, lat, lon)
            print(f'Wrote mention of {canonical_name} at {lat}, {lon} on {station} to "data/logs/venue_mentions.csv".')
            logged.add(canonical.lower())

