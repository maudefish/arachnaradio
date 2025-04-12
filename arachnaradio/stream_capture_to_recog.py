# arachnaradio/stream_capture.py
import sys
from pathlib import Path

# Add the project root directory to Python's search path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
import subprocess
import os
import time
from datetime import datetime
from pathlib import Path
from arachnaradio.song_identifier import identify_song
from arachnaradio.match_logger import log_match
from arachnaradio.whisper_transcriber import transcribe_clip
from arachnaradio.mention_logger import mentioned_artists, log_mention
from arachnaradio.clip_processor import process_clip

favorite_artists = [
    "SPELLLING", "Bridget St. John", "Ibibio Sound Machine", "Broadcast"
]

STREAM_URL = "https://stream.kalx.berkeley.edu:8443/kalx-128.mp3"
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)


def wait_until_fully_written(file_path, timeout=5):
    previous_size = -1
    for _ in range(timeout * 10):  # 10 tries per second
        current_size = os.path.getsize(file_path)
        if current_size == previous_size:
            return True  # File stopped growing
        previous_size = current_size
        time.sleep(0.1)
    raise TimeoutError("File write didn't stabilize in time.")
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

    print("🎙️ Recording to", filename)
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    wait_until_fully_written(filename)
    print("✅ Recording complete.")

    # 🧠 Let process_clip handle everything from here
    process_clip(filename, model_name="ggml-medium.en")

    print()  # Visual spacing for logs
if __name__ == "__main__":
    while True:
        record_clip()
        time.sleep(30)  # Wait before next capture
