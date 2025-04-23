from backend.core.clip_processor import process_clip
from pathlib import Path
from backend.services.venue_mention_logger import check_for_mentioned_venues
from pyprojroot import here
from backend.core.whisper_transcriber import transcribe_clip


clip_path = Path("data/clips/kalx_clip_2025-04-14_08-30-25.mp3")  # path to your clip
model_name = "ggml-small.en"

process_clip(clip_path, model_name=model_name)


