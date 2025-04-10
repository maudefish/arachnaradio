```mermaid
flowchart TD;
    A[stream_capture_to_recog.py] --> C[song_identifier.py];
    C --> D[];
    C --> F[ffmpeg subprocess];
    C --> E[identify_song];
    C --> F[ACRCloud API];
    C --> G[match_logger.py optional];
    A --> H[dotenv / os.getenv];
```
