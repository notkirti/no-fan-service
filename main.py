from parser import parse_followers, parse_following
from snapshot import save_snapshot, load_snapshots, get_latest_snapshot

followers = parse_followers()
following = parse_following()

print(f"Followers: {len(followers)}")
print(f"Following: {len(following)}")

save_snapshot(followers, following)

latest = get_latest_snapshot()
print(f"Latest snapshot taken at: {latest['timestamp']}")
print(f"Snapshots saved so far: {len(load_snapshots())}")