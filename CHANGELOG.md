## Changelog

- [x] Stream and save live radio audio (KALX) 30 second chunks
- [x] Use ACRCloud to ID songs

## TO DO (Goal 1)
- [ ]  Create CSV for saving positive song ID (time, station, etc)
- [ ]  Create method for deleting mp3 once data extracted
- [ ]  Auth users in spotify to get taste profile
- [ ]  better to

## TO DO (Goal 2)
- [ ]  Whisper -> start recognizing artist names

# CHANGELOG

## [Apr 11, 2025]
- Set up Spotify OAuth login via Streamlit sidebar  
- Saved top Spotify artists to per-user YAML profiles  
- Began separating dashboard concerns into modular files  

## [Apr 12, 2025]
- Implemented user-tracked artists UI for viewing, adding, removing entries  
- Auto-sync Spotify top artists if no favorites exist yet  
- Persisted tracked artists in YAML using username-based filenames  

## [Apr 13, 2025]
- Parsed and displayed recent tracked artist matches  
- Grouped matched tracks by station and timestamp in UI  
- Cleaned up map visuals and hover tooltips  

## [Apr 14, 2025]
- Created venue master CSV and geocoding logic with fallback hints  
- Mapped venue mentions from logs using lat/lon info  
- Backfilled missing lat/lon values in venue_mentions.csv  

## [Apr 15, 2025]
- Added custom HTML tooltip generator with artist, venue, date, and audio link  
- Stored full transcript but displayed formatted summary on map hover  
- Synced venue map hover with updated data model  

## [Apr 16, 2025]
- Implemented fuzzy matching and alias resolution for venue names  
- Built alias YAML file to persist known variants (e.g. SFJAZZ Center)  
- Scripted scanner to find unmatched names in logs vs master  

## [Apr 17, 2025]
- Integrated fuzzy matching + alias resolution into `venue_logger.py` and `clip_processor.py`  
- Updated `backfill.py` to skip duplicates and respect fuzzy-resolved venues  
- Added support for auto-saving newly discovered aliases  
