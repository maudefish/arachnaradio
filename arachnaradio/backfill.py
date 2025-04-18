# backfill.py
import pandas as pd
from pathlib import Path

MENTIONS_PATH = Path("data/logs/venue_mentions.csv")
MASTER_PATH = Path("data/venues_master.csv")

# Load files
mentions_df = pd.read_csv(MENTIONS_PATH)
master_df = pd.read_csv(MASTER_PATH)

# Normalize venue names
mentions_df["venue_clean"] = mentions_df["venue"].str.strip().str.lower()
master_df["venue_clean"] = master_df["name"].str.strip().str.lower()

# Merge to add missing lat/lon from master
merged = mentions_df.merge(
    master_df[["venue_clean", "lat", "lon"]],
    on="venue_clean",
    how="left",
    suffixes=("", "_master")
)

# Fill missing lat/lon values
merged["lat"] = merged["lat"].combine_first(merged["lat_master"])
merged["lon"] = merged["lon"].combine_first(merged["lon_master"])

# Drop temp columns
merged.drop(columns=["venue_clean", "lat_master", "lon_master"], inplace=True)

# Optional: trim whitespace from 'venue' and 'station'
merged["venue"] = merged["venue"].str.strip()
merged["station"] = merged["station"].str.strip()

# Drop duplicates
deduped = merged.drop_duplicates(
    subset=["timestamp", "station", "venue", "transcript"], keep="first"
)

# Overwrite original CSV
deduped.to_csv(MENTIONS_PATH, index=False)

print(f"✅ Cleaned and backfilled {len(mentions_df) - len(deduped)} duplicate rows.")
print("✅ Filled in missing lat/lon where available.")
