from pathlib import Path
import yaml

# Define the user profile data
user_profile = {
    "favorite_artists": [
        "SPELLLING", "Bridget St. John", "Ibibio Sound Machine", "Broadcast", "Mercury"
    ],
    "venue_list": [
        "Great American Music Hall", "The Chapel", "Rickshaw Stop",
        "The Independent", "Bottom of the Hill", "Fox Theater",
        "Greek Theatre", "Cafe du Nord", "The Fillmore", "Starline Social Club",
        "Kilowatt", "DNA Lounge", "Hotel Utah",
        "Ashkenaz", "Baltic Kiss", "The Back Room", "Cornerstone", "Eli’s Mile High Club",
        "Elbo Room", "The Freight", "Ivy Room", "Little Hill Lounge",
        "The New Parish", "Thee Stork Club", "Timbre Folk & Baroque", "UC Theatre",
        "Yoshi’s", "924 Gilman",
        "4 Star Theater", "August Hall", "Boom Boom Room", "Brick & Mortar Music Hall",
        "Cafe Du Nord", "CounterPulse", "Eagle", "Gray Area",
        "Hotel Utah", "Kilowatt", "Knockout", "The Lost Church",
        "Make Out Room", "Neck of the Woods", "Public Works", "Regency Ballroom",
        "SF Jazz Center", "Sweetwater Music Hall", "Thee Parkside", "Warfield"
    ]
}

# Save to YAML file
output_path = Path("arachnaradio/user_profile.yaml")
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w") as f:
    yaml.dump(user_profile, f, default_flow_style=False)

output_path.name
