import pandas as pd

df = pd.read_csv("data/logs/parsed_events.csv")

if "venue_original" not in df.columns:
    df["venue_original"] = df["venue"]  # or ""

df.to_csv("data/logs/parsed_events.csv", index=False)
