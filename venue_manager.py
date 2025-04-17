from pathlib import Path
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import yaml
from typing import List, Dict
import re 


VENUE_CSV_PATH = Path("data/venues_master.csv")
USER_PATH = Path("data/users")
geolocator = Nominatim(user_agent="arachnaradio", timeout=10)

def sanitize_venue_name(name: str) -> str:
    name = name.replace("&", "and")
    name = re.sub(r"[–/]", " ", name)  # dashes, slashes to spaces
    name = re.sub(r"\s+", " ", name).strip()  # collapse spaces
    return name

def geocode_with_retry(location, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return geolocator.geocode(location)
        except GeocoderTimedOut:
            time.sleep(delay)
        except Exception as e:
            print(f"Geocoding error for {location}: {e}")
            return None

def reverse_geocode(lat, lon):
    location = geolocator.reverse((lat, lon), exactly_one=True)
    address = location.raw.get("address", {})
    return address.get("city", ""), address.get("state", "")

def load_venue_master():
    if VENUE_CSV_PATH.exists():
        return pd.read_csv(VENUE_CSV_PATH)
    else:
        return pd.DataFrame(columns=["name", "city", "state", "lat", "lon"])

def save_venue_master(df):
    df.to_csv(VENUE_CSV_PATH, index=False)

def geocode_and_add_venues(venue_names: List[str], location_hint: str) -> List[Dict]:
    venues_df = load_venue_master()
    existing = venues_df["name"].str.lower().tolist()
    new_rows = []

    for venue in venue_names:
        if venue.lower() not in existing:
            sanitized = sanitize_venue_name(venue)
            location = geocode_with_retry(f"{sanitized}, {location_hint}")
            if location:
                city, state = reverse_geocode(location.latitude, location.longitude)
                new_rows.append({
                    "name": venue,
                    "city": city,
                    "state": state,
                    "lat": location.latitude,
                    "lon": location.longitude
                })
            else:
                print(f"❌ Failed to geocode: {venue} (hint: {location_hint})")

    if new_rows:
        venues_df = pd.concat([venues_df, pd.DataFrame(new_rows)], ignore_index=True)
        save_venue_master(venues_df)

    return new_rows

def update_master_with_favorites(username: str):
    user_file = USER_PATH / f"{username}_profile.yaml"
    if not user_file.exists():
        return
    with open(user_file) as f:
        user_data = yaml.safe_load(f)
    favorite_venues = user_data.get("favorite_venues", [])
    return geocode_and_add_venues(favorite_venues)

def update_master_venue_list(venue_names: List[str], location_hint: str) -> List[Dict]:
    return geocode_and_add_venues(venue_names, location_hint)


def save_favorite_venues(username: str, venues: List[str]):
    profile_path = USER_PATH / f"{username}_profile.yaml"
    if profile_path.exists():
        with open(profile_path, "r") as f:
            profile = yaml.safe_load(f)
    else:
        profile = {}

    profile["favorite_venues"] = venues
    with open(profile_path, "w") as f:
        yaml.dump(profile, f)

def load_favorite_venues(username: str) -> List[str]:
    profile_path = USER_PATH / f"{username}_profile.yaml"
    if not profile_path.exists():
        return []
    with open(profile_path, "r") as f:
        profile = yaml.safe_load(f)
    return profile.get("favorite_venues", [])

