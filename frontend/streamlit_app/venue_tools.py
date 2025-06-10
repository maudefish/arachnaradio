import streamlit as st
import yaml
from pathlib import Path
from cli.scripts.venue_geo_checker import geocode_within_bounds
from pyprojroot import here

# --- Paths ---
CANDIDATE_FILE = here("data/logs/fuzzy_misses.csv")
VENUE_MASTER_FILE = here("data/masters/venues_master.yaml")
STATION_MASTER_FILE = here("data/masters/stations_master.yaml")

# --- Load data ---
def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def save_yaml(data, path):
    with open(path, "w") as f:
        yaml.dump(data, f, sort_keys=False)

venue_master = load_yaml(VENUE_MASTER_FILE)
station_master = load_yaml(STATION_MASTER_FILE)

known_venues = set(venue_master.keys())

def render():

    with open(CANDIDATE_FILE) as f:
        candidates = sorted(set(line.strip() for line in f if line.strip()))

    # --- Streamlit UI ---
    # st.set_page_config(page_title="Venue Candidate Reviewer")
    st.title("🧭 Venue Candidate Reviewer")

    # Station selector
    station = st.selectbox("Select station:", list(station_master.keys()))
    station_coords = (station_master[station]["lat"], station_master[station]["lon"])

    # Filter unresolved candidates (those not already in venue master)
    unresolved = [v for v in candidates if v not in known_venues]

    selected_venue = st.selectbox("Select a candidate phrase:", unresolved)
    edited_name = st.text_input("Edit venue name (or alias):", value=selected_venue)
    radius = st.slider("Search radius (miles):", 5, 50, 25)

    # Check if this venue already exists (case-insensitive match)
    existing_match = next((k for k in known_venues if edited_name.lower() in [k.lower()] + [a.lower() for a in venue_master[k].get("aliases", [])]), None)

    option = st.radio("Action:", ["➕ Add as new venue", "🔁 Add as alias to existing venue"])

    if option == "🔁 Add as alias to existing venue":
        alias_target = st.selectbox("Select venue to add alias to:", sorted(venue_master.keys()))
    else:
        alias_target = None

    if st.button("💾 Process Venue"):
        if option == "🔁 Add as alias to existing venue":
            if edited_name not in venue_master[alias_target].get("aliases", []):
                venue_master[alias_target].setdefault("aliases", []).append(edited_name)
                save_yaml(venue_master, VENUE_MASTER_FILE)
                st.success(f"✅ Added alias '{edited_name}' to '{alias_target}'.")
            else:
                st.warning(f"'{edited_name}' is already an alias for '{alias_target}'.")
        else:
            location = geocode_within_bounds(edited_name, station, radius)
            if location:
                venue_master[edited_name] = {
                    "coords": [location.latitude, location.longitude],
                    "aliases": []
                }
                save_yaml(venue_master, VENUE_MASTER_FILE)
                st.success(f"✅ Added new venue '{edited_name}' with coordinates.")
            else:
                st.error("❌ Could not resolve venue with geopy.")
