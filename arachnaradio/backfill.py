import pandas as pd
from pathlib import Path

# Paths
log_path = Path("data/logs/venue_mentions.csv")
master_path = Path("data/venues_master.csv")

# Load files
mentions_df = pd.read_csv(log_path)
master_df = pd.read_csv(master_path)

# Normalize for matching
mentions_df["venue_normalized"] = mentions_df["venue"].str.lower().str.strip()
master_df["venue_normalized"] = master_df["name"].str.lower().str.strip()

# Merge lat/lon from master into mentions
updated = pd.merge(
    mentions_df.drop(columns=["lat", "lon"], errors="ignore"),
    master_df[["venue_normalized", "lat", "lon"]],
    on="venue_normalized",
    how="left"
)

# Drop helper column
updated = updated.drop(columns=["venue_normalized"])

# Save back to CSV
updated.to_csv(log_path, index=False)
print("✅ Backfilled lat/lon values in venue_mentions.csv")
