from pyprojroot import here
import pandas as pd
from pathlib import Path

PARSED_EVENTS_PATH = here("data/logs/parsed_events.csv")
VENUE_MASTER_PATH = here("data/masters/venues_geotagged.csv")

def load_parsed_events_with_coords():
    # Load parsed events
    events = pd.read_csv(PARSED_EVENTS_PATH)

    # Load venue coordinates
    master = pd.read_csv(VENUE_MASTER_PATH)

    # Merge on venue name
    merged = events.merge(master[["name", "lat", "lon"]], how="left", left_on="venue", right_on="name")

    # Optional cleanup
    merged = merged.drop(columns=["name"], errors="ignore")

    return merged
