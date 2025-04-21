# auth_section.py
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

def get_spotify_client():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

    scope = "user-read-private user-read-email user-top-read"
    auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, show_dialog=True)

    code = st.query_params.get("code")
    if code:
        try:
            token_info = auth_manager.get_access_token(code)
            sp = spotipy.Spotify(auth=token_info["access_token"])
            user_profile = sp.current_user()
            st.sidebar.success(f"🎶 Logged in as: {user_profile['display_name']}")
            return sp
        except spotipy.oauth2.SpotifyOauthError:
            st.sidebar.error("Authorization failed.")
            st.stop()
    else:
        auth_url = auth_manager.get_authorize_url()
        st.sidebar.link_button("🔐 Login with Spotify", auth_url)
        st.stop()
