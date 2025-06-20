from pathlib import Path
import re
from datetime import datetime

def extract_timestamp(path):
    filename = Path(path).name
    match = re.search(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}", filename)
    if match:
        # Convert from underscore format to ISO
        dt = datetime.strptime(match.group(), "%Y-%m-%d_%H-%M-%S")
        return dt.strftime("%Y-%m-%dT%H:%M:%S")
    return None

def path_to_weekday(path):
    dt = datetime.strptime(extract_timestamp(path), "%Y-%m-%dT%H:%M:%S")
    weekday = dt.strftime("%A, %B %d, %Y at %-I:%M %p")  # → 'Monday'
    return weekday