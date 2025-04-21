# tooltip_formatter.py
from datetime import datetime
from pathlib import Path

# def create_venue_tooltip(row: dict, base_audio_path: str = "https://yourdomain.com/audio") -> str:
#     summary = row.get("summary", "")
#     if summary:
#         return summary

#     # Fallback formatting if no LLM summary exists
#     artist = row.get("artist", "Unknown Artist")
#     venue = row.get("venue", "Unknown Venue")
#     station = row.get("station", "Unknown Station")
#     ts = row.get("timestamp", "")
#     filename = row.get("filename", None)

#     try:
#         date_str = datetime.fromisoformat(ts).strftime("%b %d, %Y")
#     except Exception:
#         date_str = "Unknown Date"

#     audio_link = ""
#     if filename:
#         basename = Path(filename).name
#         audio_url = f"{base_audio_path}/{basename}"
#         audio_link = f'<br/><a href="{audio_url}" target="_blank">🎧 Listen</a>'

#     return (
#         f"<b>{artist}</b><br/>"
#         f"📍 {venue}<br/>"
#         f"📅 {date_str}<br/>"
#         f"📻 {station}"
#         f"{audio_link}"
#     )

def create_venue_tooltip(row, base_audio_path="https://yourdomain.com/audio"):
    artist = row.get("artist") or "Unknown Artist"
    venue = row.get("venue") or "Unknown Venue"
    date = row.get("date") or "Unknown Date"
    station = row.get("station") or "Unknown Station"
    filename = row.get("filename")

    audio_link = ""
    if filename and isinstance(filename, str):
        from pathlib import Path
        basename = Path(filename).name
        audio_link = f'<br/><a href="{base_audio_path}/{basename}" target="_blank">🎧 Listen</a>'

    return (
        f"<b>{artist}</b><br/>"
        f"📍 {venue}<br/>"
        f"📅 {date}<br/>"
        f"📻 {station}"
        f"{audio_link}"
    )


def create_venue_tooltip_from_summary(row: dict, base_audio_path: str = "https://yourdomain.com/audio") -> str:
    summary = row.get("summary", "No summary available.")
    filename = row.get("filename", "")
    
    audio_link = ""
    if filename:
        basename = Path(filename).name
        audio_url = f"{base_audio_path}/{basename}"
        audio_link = f'<br/><a href="{audio_url}" target="_blank">🎧 Listen</a>'

    return (
        f"<b>{summary}</b>"
        f"{audio_link}"
    )
