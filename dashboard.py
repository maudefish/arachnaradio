#dashboard.py

import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime


st.set_page_config(page_title="Arachnaradio Dashboard", layout="wide")
st.title("🕸️ Arachnaradio Dashboard")

# Load logs
matches_path = Path("data/logs/song_matches.csv")
mentions_path = Path("data/logs/artist_mentions.csv")

def format_timestamp(ts):
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S").strftime("%b %d, %Y %I:%M %p")
    except:
        return ts  # fallback in case it's already clean or malformed

# SONG MATCHES
st.subheader("🎶 Recent Song Matches")
if matches_path.exists():
    matches = pd.read_csv(matches_path)
    matches["timestamp"] = matches["timestamp"].apply(format_timestamp)
    matches = matches.sort_values("timestamp", ascending=False)
    st.dataframe(matches, use_container_width=True)

else:
    st.info("No song matches logged yet.")

# ARTIST MENTIONS
st.subheader("🎯 Artist Mentions")
if mentions_path.exists():
    mentions = pd.read_csv(mentions_path)
    mentions["timestamp"] = mentions["timestamp"].apply(format_timestamp)
    mentions = mentions.sort_values("timestamp", ascending=False)
    st.dataframe(mentions, use_container_width=True)

else:
    st.info("No artist mentions logged yet.")

artist_filter = st.sidebar.selectbox("Filter by Artist", matches["artist"].unique())
filtered = matches[matches["artist"] == artist_filter]
st.dataframe(filtered)

if "transcript" in mentions.columns:
    selected = st.selectbox("Pick a mention", mentions["filename"])
    row = mentions[mentions["filename"] == selected].iloc[0]
    st.text(row["transcript"])


# st.audio(str(matches["filename"].iloc[0]), format="audio/mp3")
