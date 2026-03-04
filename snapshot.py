import json
import os
from datetime import datetime

def save_snapshot(followers, following):
    """Save a timestamped snapshot of followers and following."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    snapshot = {
        "timestamp": timestamp,
        "followers": list(followers),
        "following": list(following)
    }
    
    filepath = f"snapshots/{timestamp}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)
    
    print(f"Snapshot saved: {filepath}")
    return snapshot

def load_snapshots():
    """Load all saved snapshots sorted by date."""
    snapshots = []
    
    for filename in sorted(os.listdir("snapshots")):
        if filename.endswith(".json"):
            filepath = f"snapshots/{filename}"
            with open(filepath, "r", encoding="utf-8") as f:
                snapshots.append(json.load(f))
    
    return snapshots

def get_latest_snapshot():
    """Return the most recent snapshot."""
    snapshots = load_snapshots()
    return snapshots[-1] if snapshots else None