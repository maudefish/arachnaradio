from pyprojroot import here
import argparse
import yaml
import subprocess
import time
import os
import threading
from pathlib import Path
from datetime import datetime
from backend.core.clip_processor import process_clip

CONFIG_PATH = here("data/masters/stations_master.yaml")
OUTPUT_DIR = here("data/clips")

def load_station_config(station_id: str) -> dict:
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
    return config.get(station_id)

def wait_until_fully_written(file_path, timeout=10):
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

# Record clips to disk. wait_until_fully_written() makes sure processing doesn't start early. 
# Call to process_clip() in backend.core.clip_processor
def record_clip(station_id, stream_url, duration=60, model="base.en"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = OUTPUT_DIR / f"{station_id}_clip_{timestamp}.mp3"
    # file_path = OUTPUT_DIR / "clips" / filename
    # file_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg",
        "-y",
        "-i", stream_url,
        "-t", str(duration),
        "-vn",                      # no video
        "-acodec", "libmp3lame",    # encode to mp3 explicitly
        "-ar", "44100",             # sample rate (standard CD quality)
        "-ac", "2",                 # stereo
        "-b:a", "192k",             # bitrate (can adjust higher/lower)
        str(filename)
    ]

    print(f"🎙 Beginning recording to disk at {filename}...")
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    if not wait_until_fully_written(filename):
        print(f"❌ Recording failed or incomplete: {filename}")
        return  # skip processing

    print(f"✅ Finished recording to disk at {filename}...")
    # 🧠 Let process_clip handle everything from here
    process_clip(filename, model_name=model)

    print()  # Visual spacing for logs

# Use threading to have ~5 seconds overlap between clips to account for jitter / time to transcribe b/w clips
def continuous_capture(station_id, stream_url, duration=60, overlap=5, model="base.en"):
    def loop():
        while True:
            start = time.time()
            thread = threading.Thread(target=record_clip, args=(station_id, stream_url, duration, model))
            thread.start()
            # Wait until (duration - overlap) seconds before starting next
            time.sleep(duration - overlap)
    
    loop()

# Starting point for capturing audio clips for transcription 
# Example usage:  python -m cli.capture_stream --station kalx --duration 60 --model ggml-medium.en
def main():
    parser = argparse.ArgumentParser(description="📻 Stream and analyze audio for a given station.")
    parser.add_argument("--station", required=True, help="Station ID (e.g., kalx, kdvs)")
    parser.add_argument("--duration", type=int, default=60, help="Recording duration (default: 60s)")
    parser.add_argument("--model", default="base.en", help="Whisper model to use")
    args = parser.parse_args()

    station_id = args.station.lower()
    station_cfg = load_station_config(station_id)
    if not station_cfg:
        raise ValueError(f"\n❌ Unknown station ID: {station_id}")

    station_name = station_cfg["name"]
    stream_url = station_cfg["stream_url"]

    print(f"\n📡 Starting continuous capture for {station_name}...\n")

    try:
        while True:
            continuous_capture(station_id, stream_url, duration=args.duration, overlap=5, model=args.model)

    except KeyboardInterrupt:
        print("🛑 Gracefully exiting clip capture.")

if __name__ == "__main__":
    main()


