import whisper
from pathlib import Path

model = whisper.load_model("base")  # you can also try "tiny" or "small"

def transcribe_clip(file_path: Path) -> str:
    result = model.transcribe(str(file_path))
    return result["text"]
