import argparse
import yaml
import subprocess
import time
from pathlib import Path
from datetime import datetime
from backend.core.clip_processor import process_clip

CONFIG_PATH = Path("data/masters/stations.yaml")
OUTPUT_DIR = Path("data/clips")

def load_station_config(station_id: str) -> dict:
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
    return config.get(station_id)

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

def record_clip(stream_url, station_id, duration=30):
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

    print(f"🎙️ Saving to disk at {filename}...")
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    if not wait_until_fully_written(filename):
        print(f"❌ Recording failed or incomplete: {filename}")
        return  # skip processing

    print("✅ Recording complete.")

    # 🧠 Let process_clip handle everything from here
    process_clip(filename, model_name="ggml-medium.en")

    print()  # Visual spacing for logs

def main():
    parser = argparse.ArgumentParser(description="📻 Stream and analyze audio for a given station.")
    parser.add_argument("--station", required=True, help="Station ID (e.g., kalx, kdvs)")
    parser.add_argument("--duration", type=int, default=60, help="Recording duration in seconds")
    parser.add_argument("--model", default="base.en", help="Whisper model")
    args = parser.parse_args()

    station_id = args.station.lower()
    # print(station_id)
    station_cfg = load_station_config(station_id)
    if not station_cfg:
        raise ValueError(f"❌ Unknown station ID: {station_id}")

    station_name = station_cfg["name"]
    stream_url = station_cfg["stream_url"]

    while True:
        print(f"📡 Recording {station_name} ({stream_url}) for {args.duration}s...")
        record_clip(stream_url, station_id, duration=args.duration)
        # time.sleep(args.duration)

if __name__ == "__main__":
    main()
