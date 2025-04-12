#dashboard.py
import pydeck as pdk

import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime


st.set_page_config(page_title="Arachnaradio Dashboard", layout="wide")
st.title("🕸️ Arachnaradio Dashboard")

# Load logs
matches_path = Path("data/logs/song_matches.csv")
mentions_path = Path("data/logs/artist_mentions.csv")
venue_log_path = Path("data/logs/venue_mentions.csv")



def format_timestamp(ts):
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S").strftime("%b %d, %Y %I:%M %p")
    except:
        return ts  # fallback in case it's already clean or malformed

# SONG MATCHES
st.subheader("🎶 Recent Song Matches")
if matches_path.exists():
    matches = pd.read_csv(matches_path)
    matches = matches.drop(columns=["filename"])
    matches["timestamp"] = matches["timestamp"].apply(format_timestamp)
    matches = matches.sort_values("timestamp", ascending=False)
    st.dataframe(matches, use_container_width=True)

else:
    st.info("No song matches logged yet.")

# ARTIST MENTIONS
st.subheader("🎯 Artist Mentions")
if mentions_path.exists():
    mentions = pd.read_csv(mentions_path)
    mentions = mentions.drop(columns=["filename"])
    mentions["timestamp"] = mentions["timestamp"].apply(format_timestamp)
    mentions = mentions.sort_values("timestamp", ascending=False)
    st.dataframe(mentions, use_container_width=True)

else:
    st.info("No artist mentions logged yet.")

# artist_filter = st.sidebar.selectbox("Filter by Artist", matches["artist"].unique())
# filtered = matches[matches["artist"] == artist_filter]
# st.dataframe(filtered)



st.subheader("📍 Venue Mentions")

venue_log_path = Path("data/logs/venue_mentions.csv")

if venue_log_path.exists():
    venues = pd.read_csv(venue_log_path)

    # Show table
    if "timestamp" in venues.columns:
        venues["timestamp"] = venues["timestamp"].apply(format_timestamp)

    venues_display = venues.copy()
    venues_display = venues_display.dropna(how="all")


    if "filename" in venues_display.columns:
        venues_display = venues_display.drop(columns=["filename"])

    st.dataframe(venues_display, use_container_width=True)

    # Show map if lat/lon are present
    if {"lat", "lon"}.issubset(venues.columns):
        st.subheader("🗺️ Venue Map")

        venue_map_data = venues.dropna(subset=["lat", "lon"])

        tooltip = {
            "html": "<b>{venue}</b><br/>{station}<br/>{timestamp}",
            "style": {"backgroundColor": "white", "color": "black"},
        }

        st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",  # dark minimalist map
        initial_view_state=pdk.ViewState(
            latitude=37.77, longitude=-122.42, zoom=11
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=venues,
                get_position='[lon, lat]',
                get_color='[255, 0, 0, 180]',  # red markers
                get_radius=100,
                pickable=True
            )
        ],
        tooltip={
            "html": "<b>{venue}</b><br/>{station}<br/>{timestamp}<br/><i>{transcript}</i>",
            "style": {"backgroundColor": "black", "color": "white"}
        }


        ))
else:
    st.info("No venue mentions logged yet.")
