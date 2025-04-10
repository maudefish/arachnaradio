# arachnaradio/stream_capture.py
import sys
from pathlib import Path

# Add the project root directory to Python's search path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
import subprocess
import time
from datetime import datetime
from pathlib import Path
from arachnaradio.song_identifier import identify_song
from arachnaradio.match_logger import log_match
from arachnaradio.whisper_transcriber import transcribe_clip
from arachnaradio.mention_logger import mentioned_artists, log_mention

favorite_artists = [
    "SPELLLING", "Bridget St. John", "Ibibio Sound Machine", "Broadcast"
]

STREAM_URL = "https://stream.kalx.berkeley.edu:8443/kalx-128.mp3"
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

def record_clip(duration=30):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = OUTPUT_DIR / f"kalx_clip_{timestamp}.mp3"

    command = [
        "ffmpeg",
        "-y",
        "-i", STREAM_URL,
        "-t", str(duration),
        "-acodec", "copy",
        str(filename)
    ]

    print(f"🎙️ Recording to {filename}...")
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    print("✅ Recording complete.")

    print("🔍 Identifying song...")
    
    match = identify_song(filename)

    if match and match.get("title") and match.get("artist"):
        title = match["title"]
        artist = match["artist"]
        print(f"🎶 {title} by {artist}")
        log_match(str(filename), match, station="KALX")
    else:
        print("🗣️ No song match — trying Whisper...")
        transcript = transcribe_clip(filename)
        print(f"📝 Transcript: {transcript}")

        matches = mentioned_artists(transcript, favorite_artists)
        if matches:
            print(f"🎯 Mentioned: {', '.join(matches)}")
            log_mention(str(filename), transcript, station="KALX", matches=matches)
        else:
            print("🕸️ No artist mentions found.")

    print()  # Keep this outside to space out logs regardless of branch

if __name__ == "__main__":
    while True:
        record_clip()
        time.sleep(60)  # Wait before next capture
