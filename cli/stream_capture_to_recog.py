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
OUTPUT_DIR = Path("data/clips")
OUTPUT_DIR.mkdir(exist_ok=True)


def wait_until_fully_written(file_path, timeout=10):
    import time
    import os

    start_time = time.time()
    last_size = -1

    while time.time() - start_time < timeout:
        if os.path.exists(file_path):
            current_size = os.path.getsize(file_path)
            if current_size == last_size:
                return True  # done
            last_size = current_size
        time.sleep(0.5)

    print("⚠️ Timeout: File may not have finished writing.")
    return False

def record_clip(duration=30):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = OUTPUT_DIR / f"kalx_clip_{timestamp}.mp3"

    command = [
        "ffmpeg",
        "-y",
        "-i", STREAM_URL,
        "-t", str(duration),
        "-vn",                      # no video
        "-acodec", "libmp3lame",    # encode to mp3 explicitly
        "-ar", "44100",             # sample rate (standard CD quality)
        "-ac", "2",                 # stereo
        "-b:a", "192k",             # bitrate (can adjust higher/lower)
        str(filename)
    ]

    print(f"🎙️ Recording to {filename}...")
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    if not wait_until_fully_written(filename):
        print(f"❌ Recording failed or incomplete: {filename}")
        return  # skip processing


    print("✅ Recording complete.")

    # 🧠 Let process_clip handle everything from here
    process_clip(filename, model_name="ggml-medium.en")

    print()  # Visual spacing for logs
if __name__ == "__main__":
    while True:
        record_clip()
        time.sleep(30)  # Wait before next capture
