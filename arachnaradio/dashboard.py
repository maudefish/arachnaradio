#dashboard.py

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Arachnaradio Dashboard", layout="wide")
st.title("🕸️ Arachnaradio Dashboard")

# Load logs
matches_path = Path("data/logs/song_matches.csv")
mentions_path = Path("data/logs/artist_mentions.csv")

# SONG MATCHES
st.subheader("🎶 Recent Song Matches")
if matches_path.exists():
    matches = pd.read_csv(matches_path)
    matches = matches.sort_values("timestamp", ascending=False)
    st.dataframe(matches, use_container_width=True)
else:
    st.info("No song matches logged yet.")

# ARTIST MENTIONS
st.subheader("🎯 Artist Mentions")
if mentions_path.exists():
    mentions = pd.read_csv(mentions_path)
    mentions = mentions.sort_values("timestamp", ascending=False)
    st.dataframe(mentions, use_container_width=True)
else:
    st.info("No artist mentions logged yet.")
