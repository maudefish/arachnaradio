# CHANGELOG

## [Apr 10, 2025]

### 🧠 Transcription & Matching Pipeline
- Created `clip_processor.py` for audio transcription using Whisper.
- Integrated ACRCloud for music segment identification.
- Logged artist mentions and track matches to CSV with filename, timestamp, and station info.

### 📊 Initial Dashboard
- Built `dashboard.py` using Streamlit.
- Displayed artist matches and mentions with formatted timestamps.
- Created basic layout and expandable sections.

---

## [Apr 11, 2025]

### 🔐 Spotify Integration (Phase 1)
- Set up Spotify OAuth login via Streamlit sidebar.
- Retrieved user profile display name on login.
- Saved top Spotify artists to per-user YAML profiles.
- Began separating dashboard concerns into modular files.

---

## [Apr 12, 2025]

### 🎧 Tracked Artist Management
- Implemented UI to view, add, and remove tracked artists via sidebar.
- Auto-synced Spotify top artists if no favorites existed.
- Persisted tracked artists in YAML using Spotify user ID.

---

## [Apr 13, 2025]

### 🎯 Artist Match Filtering
- Parsed and displayed recent tracked artist matches.
- Grouped matched tracks by station and timestamp in dashboard.
- Cleaned up map visuals and hover tooltips.

---

## [Apr 14, 2025]

### 🗺️ Venue Geocoding + Mapping
- Created venue master CSV and geocoding logic with fallback hints.
- Mapped venue mentions from logs using lat/lon.
- Backfilled missing lat/lon values in `venue_mentions.csv`.

---

## [Apr 15, 2025]

### 🧩 Tooltip Summarization
- Added custom HTML tooltip generator with artist, venue, date, and audio link.
- Stored full transcript in logs but displayed structured summary on map hover.
- Synced venue map hover with updated data model.

---

## [Apr 16, 2025]

### 🧬 Spotify Favorites + Profile Refactor
- Automatically fetched and saved user's top artists to `user_profile.yaml`.
- Modularized profile YAML read/write in `artist_manager.py`.
- Supported manual artist additions/removals with real-time update.
- Displayed filtered song match log based on tracked artists.
- Profile state persisted via Spotify user ID.
- Added custom font and improved sidebar UI.

---

## [Apr 17, 2025]

### 🔎 Fuzzy Venue Matching + Alias Resolution
- Integrated fuzzy matching and alias resolution into `venue_logger.py` and `clip_processor.py`.
- Implemented `alias_resolver.py` to store aliases in YAML for canonical venue names.
- Updated `backfill.py` to skip duplicates and resolve fuzzy venue matches.
- Added support for auto-saving newly discovered aliases.
- Refined map radius/tooltip and normalized display data.

---

## [NEXT UP]
- Use local AI calls to ollama / mistral to refactor transcripts of venue mentions for display in map / notifications
- Re-organize directory structure (keep streamlit files together, backend utilities, etc) 

## [RANDOM THOUGHTS]
- Potential for listening to talk radio for topics of interest to the user also (climate change, local politics, hobbies, etc)
- Eventually need to figure out a way to record quasicontinuously
- ... probably will be best to save only clips that feature event mentions for use in map
