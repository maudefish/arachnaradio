#dashboard.py
from dotenv import load_dotenv
import os
import pydeck as pdk
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import yaml
from typing import List
from auth_section import get_spotify_client
from artist_manager import get_all_top_artists, save_top_artists_to_yaml, load_favorite_artists

st.set_page_config(page_title="Arachnaradio Dashboard", layout="wide")
st.title("🕸️ Arachnaradio Dashboard")

sp = get_spotify_client()
user_profile = sp.current_user()
username = user_profile["id"]  # used for file naming

from artist_manager import (
    get_user_profile_path,
    get_all_top_artists,
    save_top_artists_to_yaml,
    load_favorite_artists,
)

# Only fetch & save Spotify top artists if user profile doesn't exist yet
user_profile_path = get_user_profile_path(username)
if not user_profile_path.exists():
    top_artists = get_all_top_artists(sp)
    save_top_artists_to_yaml(username, top_artists)

# Load current tracked artists
favorite_artists = load_favorite_artists(username)


st.sidebar.subheader("🎧 Manage Tracked Artists")

# Remove artists
with st.sidebar.expander("➖ Remove Artists", expanded=False):
    remove_artists = st.multiselect("Select artists to remove", favorite_artists)
    if st.button("Remove Selected"):
        favorite_artists = [artist for artist in favorite_artists if artist not in remove_artists]
        save_top_artists_to_yaml(username, favorite_artists)
        st.rerun()

# Add artist
with st.sidebar.expander("➕ Add Artist", expanded=False):
    new_artist = st.text_input("Artist name")
    if st.button("Add Artist") and new_artist:
        if new_artist not in favorite_artists:
            favorite_artists.append(new_artist)
            favorite_artists = sorted(set(favorite_artists))
            save_top_artists_to_yaml(username, favorite_artists)
            st.success(f"Added {new_artist} to tracked artists!")
            st.rerun()
        else:
            st.info(f"{new_artist} is already being tracked.")


def format_timestamp(ts):
    return pd.to_datetime(ts).strftime("%b %d, %Y %I:%M %p")


# 💅 Inject custom font via markdown
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono&display=swap');

    html, body, div, span, input, label, textarea, select, button {
        font-family: 'Space Mono', monospace !important;
    }

    .stText, .stMarkdown, .stDataFrame, .stSelectbox, .stTooltip {
        font-family: 'Space Mono', monospace !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# st.title("🕸️ Arachnaradio Dashboard")

# Load logs
matches_path = Path("data/logs/song_matches.csv")
mentions_path = Path("data/logs/artist_mentions.csv")
venue_log_path = Path("data/logs/venue_mentions.csv")

# # Get top artists (short_term, medium_term, or long_term)
# top_artists = sp.current_user_top_artists(limit=30, time_range='long_term')

# st.subheader("🔥 Your Top Artists")
# for idx, artist in enumerate(top_artists['items'], start=1):
#     st.markdown(f"**{idx}. {artist['name']}**")



# SONG MATCHES
st.subheader("🎶 Recent Song Matches")
if matches_path.exists():
    matches = pd.read_csv(matches_path)
    matches = matches.drop(columns=["filename"])
    # 🔁 Parse actual datetime *before* sorting
    matches["timestamp"] = pd.to_datetime(matches["timestamp"])

    # ✅ Now sort based on real time
    matches = matches.sort_values("timestamp", ascending=False)

    # 🧼 Format only for display after sorting
    matches["timestamp"] = matches["timestamp"].dt.strftime("%b %d, %Y %I:%M %p")
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
