import yaml
import pandas as pd

with open("data/masters/venues_master.yaml") as f:
    data = yaml.safe_load(f)

rows = []
for name, props in data.items():
    row = {
        "name": name,
        "lat": props.get("lat"),
        "lon": props.get("lon"),
        "address": props.get("address"),
        "city": props.get("city")
    }
    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv("data/masters/venues_geotagged.csv", index=False)
