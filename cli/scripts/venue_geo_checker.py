from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.point import Point

# Define known radio station locations
station_coords = {
    "KALX": (37.8703, -122.2595),  # UC Berkeley
    "KEXP": (47.6255, -122.3561), # Seattle
    # Add more stations here if needed
}

def geocode_within_bounds(venue_name: str, station: str, radius_miles: float = 50):
    if station not in station_coords:
        print(f"❌ Unknown station: {station}")
        return None

    lat, lon = station_coords[station]
    geolocator = Nominatim(user_agent="arachnaradio")

    # Define bounding box using Points
    lat_margin = 1
    lon_margin = 1
    viewbox = [
        Point(lat + lat_margin, lon + lon_margin),  # NE corner
        Point(lat - lat_margin, lon - lon_margin)   # SW corner
    ]

    try:
        location = geolocator.geocode(
            venue_name,
            viewbox=viewbox,
            bounded=True,
            addressdetails=True
        )
        if location:
            venue_coords = (location.latitude, location.longitude)
            distance = geodesic((lat, lon), venue_coords).miles
            if distance <= radius_miles:
                print(f"✅ '{venue_name}' resolved to '{location.address}' ({venue_coords}), {distance:.1f} mi from station")
                return location
            else:
                print(f"⚠️ '{venue_name}' found but is {distance:.1f} mi from station (outside {radius_miles} mi)")
                return None
        else:
            print("❌ Could not geocode venue.")
            return None
    except Exception as e:
        print(f"❌ Geocoding error: {e}")
        return None


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python -m cli.scripts.geotest <venue_name> <station>")
    else:
        venue_name = sys.argv[1]
        station = sys.argv[2].upper()
        geocode_within_bounds(venue_name, station)
