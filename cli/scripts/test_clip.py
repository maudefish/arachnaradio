from backend.core.clip_processor import process_clip
from pathlib import Path

clip_path = Path("data/clips/kalx_clip_2025-04-15_18-32-51.mp3")

# You can set the model and station manually if needed
process_clip(clip_path, station="KALX", model_name="ggml-medium.en")
