from pyprojroot import here
from pathlib import Path
import pandas as pd
import re

parsed_path = here("data/logs/parsed_events.csv")
# master_path = here("data/masters/venues_geotagged.csv")
df = pd.read_csv(parsed_path)
# master_df = pd.read_csv(master_path)

def extract_timestamp(path):
	filename = Path(path).name
	match = re.search(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}", filename)
	timestamp = match.group() if match else None
	return timestamp

df["timestamp"] = df["filename"].apply(extract_timestamp)

df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d_%H-%M-%S").dt.strftime("%Y-%m-%dT%H:%M:%S")

df.to_csv('output.csv', index=False, sep=',', encoding='utf-8')


print(df)
