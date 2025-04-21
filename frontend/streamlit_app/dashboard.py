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
from venue_manager import update_master_venue_list, save_favorite_venues, load_favorite_venues
from tooltip_formatter import create_venue_tooltip, create_venue_tooltip_from_summary
from event_map_utils import load_parsed_events_with_coords


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


# Load profile if it exists
if user_profile_path.exists():
    with open(user_profile_path, "r") as f:
        profile = yaml.safe_load(f) or {}

    # Ensure defaults are present
    profile.setdefault("favorite_artists", [])
    profile.setdefault("favorite_venues", [])
    profile.setdefault("location_hint", "San Francisco Bay Area, CA")

    # Save back any missing defaults (optional, but good habit)
    with open(user_profile_path, "w") as f:
        yaml.dump(profile, f)

    favorite_artists = profile["favorite_artists"]
    favorite_venues = profile["favorite_venues"]
    location_hint = profile["location_hint"]


else:
    top_artists = get_all_top_artists(sp)
    save_top_artists_to_yaml(username, top_artists)
    favorite_artists = top_artists
    favorite_venues = []  # default to empty list

if st.sidebar.button("🔄 Update Venue Locations"):
    with st.spinner("📍 Geocoding new venues..."):
        updated = update_master_venue_list(favorite_venues, location_hint)
        st.success(f"✅ Added {len(updated)} new venues to master list.")


st.sidebar.subheader("🎧 Manage Tracked Artists")

# Remove artists
with st.sidebar.expander("🔍 Tracked Artists", expanded=False):
    remove_artists = st.multiselect("Expand to view list. Highlight name to edit.", favorite_artists)
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

st.sidebar.subheader("📍 Manage Tracked Venues")

# 🔍 View + Remove
with st.sidebar.expander("🔍 Tracked Venues", expanded=False):
    if favorite_venues:
        remove_venues = st.multiselect("Select venues to remove", favorite_venues)
        if st.button("Remove Selected Venues"):
            favorite_venues = [v for v in favorite_venues if v not in remove_venues]
            save_favorite_venues(username, favorite_venues)
            st.success("Selected venues removed.")
            st.rerun()
    else:
        st.info("You are not tracking any venues yet.")

# ➕ Add
with st.sidebar.expander("➕ Add Venue", expanded=False):
    new_venue = st.text_input("Venue name")
    if st.button("Add Venue") and new_venue:
        if new_venue not in favorite_venues:
            favorite_venues.append(new_venue)
            favorite_venues = sorted(set(favorite_venues))
            save_favorite_venues(username, favorite_venues)
            st.success(f"Added {new_venue} to tracked venues!")
            st.rerun()
        else:
            st.info(f"{new_venue} is already being tracked.")

matches_path = Path("data/logs/song_matches.csv")

if matches_path.exists():
    matches = pd.read_csv(matches_path)

    # Normalize artist names
    matches["artist"] = matches["artist"].str.strip().str.lower()
    tracked = [a.lower() for a in favorite_artists]

    # Filter for tracked artist matches
    filtered = matches[matches["artist"].isin(tracked)].copy()

    # Only show relevant columns
    display_columns = ["timestamp", "station", "title", "artist", "album", "label", "score"]
    available_columns = [col for col in display_columns if col in filtered.columns]
    filtered = filtered[available_columns]

    # Format timestamp
    if "timestamp" in filtered.columns:
        filtered["timestamp"] = pd.to_datetime(filtered["timestamp"])
        filtered = filtered.sort_values("timestamp", ascending=False)
        filtered["timestamp"] = filtered["timestamp"].dt.strftime("%b %d, %Y %I:%M %p")

    st.subheader("🎶 Matched Tracks for Your Tracked Artists")
    st.dataframe(filtered, use_container_width=True)
else:
    st.info("No song matches logged yet.")


def format_timestamp(ts):
    try:
        ts = pd.to_datetime(ts)
        if pd.isna(ts):
            return "Unknown"
        return ts.strftime("%b %d, %Y %I:%M %p")
    except Exception:
        return "Unknown"


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
venue_log_path = Path("data/logs/parsed_events.csv")

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



# st.subheader("📍 Venue Mentions")

# venue_log_path = Path("data/logs/venue_mentions.csv")
# Assuming `venues_display` is your DataFrame
# venues_display["tooltip"] = venues_display.apply(lambda row: create_venue_tooltip(row), axis=1)



# if venue_log_path.exists():
#     venues = pd.read_csv(venue_log_path)

#     # Show table
#     if "timestamp" in venues.columns:
#         venues["timestamp"] = venues["timestamp"].apply(format_timestamp)

#     venues_display = venues.copy()
#     venues_display = venues_display.dropna(how="all")


#     if "filename" in venues_display.columns:
#         venues_display = venues_display.drop(columns=["filename"])

#     st.dataframe(venues_display, use_container_width=True)

#     # Show map if lat/lon are present
#     if {"lat", "lon"}.issubset(venues.columns):
#         st.subheader("🗺️ Venue Map")

#         venue_map_data = venues.dropna(subset=["lat", "lon"])

#         tooltip = {
#             "html": "<b>{venue}</b><br/>{station}<br/>{timestamp}",
#             "style": {"backgroundColor": "white", "color": "black"},
#         }

#         st.pydeck_chart(pdk.Deck(

#         map_style="mapbox://styles/mapbox/dark-v10",  # dark minimalist map
#         initial_view_state=pdk.ViewState(
#             latitude=37.77, longitude=-122.42, zoom=11
#         ),
#         layers=[
#             pdk.Layer(
#                 "ScatterplotLayer",
#                 data=venues,
#                 get_position='[lon, lat]',
#                 get_color='[255, 0, 0, 180]',
#                 get_radius=120,  # Increase for visual size
#                 radius_min_pixels=5,  # ensures it's not too small when zoomed out
#                 radius_max_pixels=20,  # cap for when zoomed in
#                 pickable=True
#                     )
#         ],

#         tooltip={"html": "{tooltip}", "style": {"backgroundColor": "black", "color": "white"}}
#         ))


        
# else:
#     st.info("No venue mentions logged yet.")
if venue_log_path.exists():
    venues = load_parsed_events_with_coords()
    st.write("Columns in merged event data:", venues.columns.tolist())
    st.write(venues.head())



    if "timestamp" in venues.columns:
        venues["timestamp"] = venues["timestamp"].apply(format_timestamp)

    venues = venues.dropna(how="all")
    venues_with_coords = venues.dropna(subset=["lat", "lon"]).copy()

    # ✅ Add LLM summary-based tooltip
    venues_with_coords["tooltip"] = venues_with_coords.apply(
    lambda row: create_venue_tooltip(row), axis=1
)

    # 🎯 Display table (optional: drop filename/transcript)
    st.subheader("📍 Venue Mentions")
    table_view = venues_with_coords.drop(columns=["filename", "transcript"], errors="ignore")
    st.dataframe(table_view, use_container_width=True)

    # 🗺️ Display map
    st.subheader("🗺️ Venue Map")
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=pdk.ViewState(latitude=37.77, longitude=-122.42, zoom=11),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=venues_with_coords,
                get_position='[lon, lat]',
                get_color='[255, 0, 0, 180]',
                get_radius=120,
                radius_min_pixels=5,
                radius_max_pixels=20,
                pickable=True
            )
        ],
        tooltip={
            "html": "{tooltip}",
            "style": {"backgroundColor": "black", "color": "white"}
        }
    ))
else:
    st.info("No venue mentions logged yet.")
# if venue_log_path.exists():
#     venues = pd.read_csv(venue_log_path)

#     # Format timestamp if present
#     if "timestamp" in venues.columns:
#         venues["timestamp"] = venues["timestamp"].apply(format_timestamp)

#     # Clean up null rows
#     venues = venues.dropna(how="all")

#     # Only show venues with coordinates
#     venues_with_coords = venues.dropna(subset=["lat", "lon"]).copy()

#     # Optional: drop unnecessary columns in table display
#     table_view = venues_with_coords.drop(columns=["filename"], errors="ignore")

#     # 🆕 Add custom tooltip field (after importing your function)
#     venues_with_coords["tooltip"] = venues_with_coords.apply(create_venue_tooltip, axis=1)

#     # 📊 Show table
#     st.subheader("📍 Venue Mentions")
#     st.dataframe(table_view, use_container_width=True)

#     # 🗺️ Show map
#     st.subheader("🗺️ Venue Map")
#     st.write("Columns in venues_with_coords:", venues_with_coords.columns.tolist())
#     st.write("Sample tooltip:", venues_with_coords["tooltip"].head())
#     st.pydeck_chart(pdk.Deck(
#         map_style="mapbox://styles/mapbox/dark-v10",
#         initial_view_state=pdk.ViewState(latitude=37.8, longitude=-122.35, zoom=11),
#         layers=[
#             pdk.Layer(
#                 "ScatterplotLayer",
#                 data=venues_with_coords,
#                 get_position='[lon, lat]',
#                 get_color='[255, 0, 0, 180]',
#                 get_radius=120,  # Increase for visual size
#                 radius_min_pixels=5,  # ensures it's not too small when zoomed out
#                 radius_max_pixels=20,  # cap for when zoomed in
#                 pickable=True
#             )
#         ],
#         tooltip={"html": "{tooltip}", "style": {"backgroundColor": "black", "color": "white"}}
#          ))

# else:
#     st.info("No venue mentions logged yet.")

