import pandas as pd
import yaml
from pathlib import Path

# Paths
CSV_PATH = Path("data/masters/venues_geotagged.csv")
YAML_PATH = Path("data/masters/venues_master.yaml")

# Load CSV
df = pd.read_csv(CSV_PATH)

# Convert to structured YAML dictionary
yaml_dict = {}
for _, row in df.iterrows():
    name = row["name"]
    yaml_dict[name] = {
        "lat": row.get("lat"),
        "lon": row.get("lon"),
        "address": row.get("address") if "address" in row else None,
        "city": row.get("city") if "city" in row else None,
        "aliases": []  # Leave blank for now — ready for manual or automatic enrichment
    }

# Save to YAML
YAML_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(YAML_PATH, "w", encoding="utf-8") as f:
    yaml.dump(yaml_dict, f, sort_keys=False, allow_unicode=True)

print(f"✅ Saved YAML to {YAML_PATH}")
