#dashboard.py
import pydeck as pdk
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
st.set_page_config(page_title="Arachnaradio Dashboard", layout="wide")


# 🎧 Spotify Auth Setup
REDIRECT_URI = "http://127.0.0.1:8501/"
CLIENT_ID = "79ca8615ee02470c8a34ff3c15977965"
CLIENT_SECRET = "435216fbd8bf4d438e23ae83c419fc3a"
SCOPE = "user-read-private user-read-email user-top-read"

auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,  # must match exactly
    scope=SCOPE,
    show_dialog=True
)

code = st.query_params.get("code")
if code:
    try:
        token_info = auth_manager.get_access_token(code[0])
        sp = spotipy.Spotify(auth=token_info["access_token"])
        user_profile = sp.current_user()
        st.sidebar.success(f"🎶 Logged in as: {user_profile['display_name']}")
    except spotipy.oauth2.SpotifyOauthError as e:
        st.error(str(e))
        st.sidebar.error("Authorization failed. Please try logging in again.")
        st.stop()
else:
    auth_url = auth_manager.get_authorize_url()
    st.sidebar.link_button("🔐 Login with Spotify", auth_url)
    st.stop()

# ... existing dataframe views, charts, maps, etc.


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

st.title("🕸️ Arachnaradio Dashboard")

# Load logs
matches_path = Path("data/logs/song_matches.csv")
mentions_path = Path("data/logs/artist_mentions.csv")
venue_log_path = Path("data/logs/venue_mentions.csv")

# Get top artists (short_term, medium_term, or long_term)
top_artists = sp.current_user_top_artists(limit=10, time_range='medium_term')

st.subheader("🔥 Your Top Artists")
for idx, artist in enumerate(top_artists['items'], start=1):
    st.markdown(f"**{idx}. {artist['name']}**")


def format_timestamp(ts):
    return pd.to_datetime(ts).strftime("%b %d, %Y %I:%M %p")

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
