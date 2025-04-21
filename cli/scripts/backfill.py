import pandas as pd
from pathlib import Path
from alias_resolver import resolve_canonical_name, load_aliases

# Paths
MENTIONS_PATH = Path("data/logs/venue_mentions.csv")
MASTER_PATH = Path("data/venues_master.csv")

# Load data
df = pd.read_csv(MENTIONS_PATH)
master_df = pd.read_csv(MASTER_PATH)
aliases = load_aliases()
master_names = master_df["name"].tolist()

# Add canonical column if not present
if "canonical_venue" not in df.columns:
    df["canonical_venue"] = ""

# Clean and resolve
for i, row in df.iterrows():
    original = row["venue"]
    canonical = resolve_canonical_name(original, aliases, master_names)
    df.at[i, "canonical_venue"] = canonical

    # Optionally: also fix lat/lon if missing
    if pd.isna(row.get("lat")) or pd.isna(row.get("lon")):
        matched_row = master_df[master_df["name"].str.lower() == canonical.lower()]
        if not matched_row.empty:
            df.at[i, "lat"] = matched_row.iloc[0]["lat"]
            df.at[i, "lon"] = matched_row.iloc[0]["lon"]

# Save it back
df.to_csv(MENTIONS_PATH, index=False)
print("✅ Backfill complete with canonical names and updated coordinates.")
