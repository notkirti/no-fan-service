import json
import os

def load_json(filepath):
    """Load a JSON file and return its contents."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find file: {filepath}")
    
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def parse_followers(filepath="data/followers_1.json"):
    """Extract a clean set of follower usernames."""
    data = load_json(filepath)
    return {
        entry["string_list_data"][0]["value"]
        for entry in data
    }

def parse_following(filepath="data/following.json"):
    """Extract a clean set of following usernames."""
    data = load_json(filepath)
    return {
        entry["title"]
        for entry in data["relationships_following"]
    }