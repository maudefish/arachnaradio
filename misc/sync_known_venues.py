import pandas as pd
import yaml
from pathlib import Path

CSV_PATH = Path("data/masters/venues_geotagged.csv")
YAML_PATH = Path("data/masters/venues_master.yaml")

def load_venue_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df["name"].dropna().unique()

def load_known_venues(yaml_path):
    if not yaml_path.exists():
        return {"known_venues": {}}
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)

def save_known_venues(yaml_path, data):
    with open(yaml_path, "w") as f:
        yaml.dump(data, f, sort_keys=False)

def sync_known_venues(csv_path, yaml_path):
    csv_venues = load_venue_csv(csv_path)
    yaml_data = load_known_venues(yaml_path)
    known_venues = yaml_data.get("known_venues", {})

    added = 0
    for venue in csv_venues:
        if venue not in known_venues:
            known_venues[venue] = {"aliases": []}
            added += 1

    if added > 0:
        yaml_data["known_venues"] = known_venues
        save_known_venues(yaml_path, yaml_data)
        print(f"✅ Added {added} new venue(s) to known_venues.yaml.")
    else:
        print("✅ YAML already includes all venues from CSV — no changes made.")

if __name__ == "__main__":
    sync_known_venues(CSV_PATH, YAML_PATH)
