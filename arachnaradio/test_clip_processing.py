#test_clip_processing.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from arachnaradio.song_identifier import identify_song
from arachnaradio.whisper_transcriber import transcribe_clip
from arachnaradio.match_logger import log_match
from arachnaradio.mention_logger import log_mention, mentioned_artists


# 👤 Customize this list!
favorite_artists = [
    "SPELLLING", "Bridget St. John", "Ibibio Sound Machine", "Broadcast", "Mercury"
]

# 🎧 Path to your test audio file
filename = Path("data/kalx_clip_2025-04-10_16-00-46.mp3")
station = "Test"

# 🧠 Run song match
match = identify_song(filename)

if match and match.get("title") and match.get("artist"):
    title = match["title"]
    artist = match["artist"]
    print(f"🎶 {title} by {artist}")
    log_match(str(filename), match, station=station)
else:
    print("🗣️ No song match — trying Whisper...")
    transcript = transcribe_clip(filename)
    print(f"📝 Transcript: {transcript}")

    matches = mentioned_artists(transcript, favorite_artists)
    if matches:
        print(f"🎯 Mentioned: {', '.join(matches)}")
        log_mention(str(filename), transcript, station=station, matches=matches)
    else:
        print("🕸️ No artist mentions found.")
