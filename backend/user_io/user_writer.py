

def save_top_artists_to_yaml(username: str, artists: list[str]):
    path = get_user_profile_path(username)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        yaml.dump({"favorite_artists": artists}, f)

