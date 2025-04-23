# backend/data_io/writers.py

from pathlib import Path
import yaml
import pandas as pd

def save_yaml(data: dict, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f)

def save_csv(df: pd.DataFrame, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

def write_venue_log_row(writer, timestamp, station, filename, venue, transcript, lat, lon):
    writer.writerow([timestamp, station, filename, venue, transcript, lat, lon])
