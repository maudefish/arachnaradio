from backend.core.clip_processor import process_clip
from pathlib import Path

clip_path = Path("data/clips/kalx_clip_2025-04-27_18-31-54.mp3")
# clip_path = Path("data/clips/kalx_clip_2025-04-25_15-31-10.mp3")
# usage: python -m cli.scripts.test_clip.py
# You can set the model and station manually if needed
process_clip(clip_path, station="KALX", model_name="ggml-medium.en")
