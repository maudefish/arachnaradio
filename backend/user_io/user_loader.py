# artist_manager.py
import yaml
from pathlib import Path
from typing import List

# artist_manager.py
def get_user_profile_path(username: str) -> Path:
    return Path(f"data/users/{username}_profile.yaml")


def load_favorite_artists(username: str) -> List[str]:
    path = get_user_profile_path(username)
    if path.exists():
        with open(path, "r") as f:
            profile = yaml.safe_load(f)
            return profile.get("favorite_artists", [])
    return []

def get_all_top_artists(sp) -> List[str]:
    """Fetches user's top artists across all time ranges (short, medium, long)."""
    time_ranges = ['short_term', 'medium_term', 'long_term']
    artist_set = set()

    for time_range in time_ranges:
        results = sp.current_user_top_artists(limit=20, time_range=time_range)
        for artist in results["items"]:
            artist_set.add(artist["name"])

    return sorted(artist_set)

    

def save_top_artists_to_yaml(username: str, artists: list[str]):
    path = get_user_profile_path(username)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        yaml.dump({"favorite_artists": artists}, f)

