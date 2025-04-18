# tooltip_formatter.py
from datetime import datetime
from pathlib import Path

def create_venue_tooltip(row: dict, base_audio_path: str = "https://yourdomain.com/audio") -> str:
    """
    Generate a cleaner tooltip string for a venue map marker.
    """

    # Parse fields
    artist = row.get("artist", "Unknown Artist")
    venue = row.get("venue", "Unknown Venue")
    station = row.get("station", "Unknown Station")
    ts = row.get("timestamp", "")
    event_date = row.get("event_date", "Unknown Date")
    filename = row.get("filename", None)

    # Format date
    try:
        date_str = datetime.fromisoformat(ts).strftime("%b %d, %Y")
    except Exception:
        date_str = "Unknown Date"

    # Generate audio link if filename is provided
    audio_link = ""
    if filename:
        basename = Path(filename).name
        audio_url = f"{base_audio_path}/{basename}"
        audio_link = f'<br/><a href="{audio_url}" target="_blank">🎧 Listen</a>'

    # Return formatted tooltip
    return (
        f"<b>{artist}</b><br/>"
        f"📍 {venue}<br/>"
        f"📅 {event_date}<br/>"
        f"📻 {station}"
        f"{audio_link}"
    )
