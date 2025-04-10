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
    title, artist = identify_song(filename)
    if title and artist:
        print(f"🎶 Match: {title} by {artist}")
    else:
        print("❌ No match found.")
    print()

if __name__ == "__main__":
    while True:
        record_clip()
        time.sleep(60)  # Wait before next capture
