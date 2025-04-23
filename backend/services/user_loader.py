from pyprojroot import here
from pathlib import Path
import yaml

# Calculate project root (one level up from current file)
USER_DATA_PATH = here("data/users")

def load_user_profile(username: str) -> dict:
    user_path = USER_DATA_PATH / f"{username}_profile.yaml"
    print(f"\nLooking for profile at: {user_path}\n")

    if not user_path.exists():
        raise FileNotFoundError(f"No profile found for user '{username}'")
    
    with open(user_path, "r") as f:
        profile = yaml.safe_load(f)
    
    return profile
