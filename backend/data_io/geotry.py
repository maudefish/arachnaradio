import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from pathlib import Path

# Sample venues to simulate input
venues_to_check = [
    "The Chapel, San Francisco, CA",
    "The Independent, San Francisco, CA",
    "Rickshaw Stop, San Francisco, CA",
    "Bottom of the Hill, San Francisco, CA",
    "Starline Social Club, Oakland, CA"
]

# Path to the master venue file
venue_csv_path = Path("data/venues_master.csv")

# Ensure directory exists
venue_csv_path.parent.mkdir(parents=True, exist_ok=True)

# Load or create venue dataframe
if venue_csv_path.exists():
    venues_df = pd.read_csv(venue_csv_path)
else:
    venues_df = pd.DataFrame(columns=["name", "city", "state", "lat", "lon"])

# Geocoder setup
geolocator = Nominatim(user_agent="arachnaradio")

# Forward geocode with retry
def geocode_with_retry(location, retries=3):
    for attempt in range(retries):
        try:
            return geolocator.geocode(location)
        except GeocoderTimedOut:
            time.sleep(1)
    return None

# Reverse geocode to get city/state from lat/lon
def reverse_lookup(lat, lon):
    try:
        reverse_loc = geolocator.reverse((lat, lon), exactly_one=True)
        address = reverse_loc.raw.get("address", {})
        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("hamlet")
        )
        state = (
            address.get("state")
            or address.get("region")
            or address.get("province")
        )
        return city or "", state or ""
    except Exception:
        return "", ""

# Add missing venues
new_venues = []
for full_venue in venues_to_check:
    name = full_venue.split(",")[0].strip()
    if not any(venues_df["name"].str.lower() == name.lower()):
        location = geocode_with_retry(full_venue)
        if location:
            city, state = reverse_lookup(location.latitude, location.longitude)
            new_venues.append({
                "name": name,
                "city": city,
                "state": state,
                "lat": location.latitude,
                "lon": location.longitude
            })

# Append and save
if new_venues:
    venues_df = pd.concat([venues_df, pd.DataFrame(new_venues)], ignore_index=True)
    venues_df.to_csv(venue_csv_path, index=False)
    print(f"✅ Added {len(new_venues)} new venues.")
else:
    print("ℹ️ No new venues to add.")
