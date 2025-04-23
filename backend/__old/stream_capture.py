# arachnaradio/stream_capture.py

import subprocess
import time
from datetime import datetime
from pathlib import Path

STREAM_URL = "https://stream.kalx.berkeley.edu:8443/kalx-128.mp3"  # Updated KALX stream
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

def record_clip(duration=30):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = OUTPUT_DIR / f"kalx_clip_{timestamp}.mp3"

    command = [
        "ffmpeg",
        "-y",  # overwrite if needed
        "-i", STREAM_URL,
        "-t", str(duration),
        "-acodec", "copy",
        str(filename)
    ]

    print(f"Recording to {filename}...")
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    print("Done.\n")

if __name__ == "__main__":
    while True:
        record_clip()
        time.sleep(60)  # wait 1 min before next clip
