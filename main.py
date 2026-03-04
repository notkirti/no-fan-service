from parser import parse_followers, parse_following
from snapshot import save_snapshot, load_snapshots, get_latest_snapshot
from diff import get_diff

followers = parse_followers()
following = parse_following()

print(f"Followers: {len(followers)}")
print(f"Following: {len(following)}")

save_snapshot(followers, following)

snapshots = load_snapshots()

if len(snapshots) >= 2:
    old = snapshots[-2]
    new = snapshots[-1]
    diff = get_diff(old, new)

    print("\n--- Changes Since Last Scan ---")
    print(f"Unfollowed you:  {diff['unfollowed_you'] or 'none'}")
    print(f"You unfollowed:  {diff['you_unfollowed'] or 'none'}")
    print(f"New followers:   {diff['new_followers'] or 'none'}")
    print(f"New following:   {diff['new_following'] or 'none'}")
else:
    print("\nRun the app again to start tracking changes!")