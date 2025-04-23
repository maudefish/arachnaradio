# test_venue_logger.py

from arachnaradio.venue_logger import log_venue_mention

fake_transcript = "Don't miss SPELLLING live at The Chapel this Saturday night!"
filename = "data/test_clip_fake.mp3"
station = "KALX"
venues = ["The Chapel"]

log_venue_mention(filename, fake_transcript, station, venues)
