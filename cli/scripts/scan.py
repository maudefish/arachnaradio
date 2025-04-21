import pandas as pd
from pathlib import Path

# Paths
mentions_path = Path("data/logs/venue_mentions.csv")
master_path = Path("data/venues_master.csv")

# Load CSVs
mentions_df = pd.read_csv(mentions_path)
master_df = pd.read_csv(master_path)

# Strip and lowercase all names for comparison
def normalize(name):
    return str(name).strip().lower()

mentioned_venues = set(normalize(v) for v in mentions_df["venue"].dropna().unique())
master_venues = set(normalize(n) for n in master_df["name"].dropna().unique())

# Identify unmatched
unmatched = sorted(mentioned_venues - master_venues)

# Debug output
print("🔍 Detailed Comparison Debug\n")

for venue in unmatched:
    print(f"❌ Unmatched: '{venue}'")
    print("    Close matches in master list:")
    for master_venue in master_venues:
        if venue in master_venue or master_venue in venue:
            print(f"      → '{master_venue}'")
    print()

print(f"✅ Matched: {len(mentioned_venues & master_venues)}")
print(f"🧹 Unmatched: {len(unmatched)} / {len(mentioned_venues)} total mentioned")
