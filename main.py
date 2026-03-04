from parser import parse_followers, parse_following
from snapshot import save_snapshot, load_snapshots
from diff import get_diff
from ghost import get_ghosts, get_fans, get_mutuals
from trends import get_trends

followers = parse_followers()
following = parse_following()

print(f"Followers: {len(followers)}")
print(f"Following: {len(following)}")

save_snapshot(followers, following)

# Ghost detection
ghosts = get_ghosts(followers, following)
fans = get_fans(followers, following)
mutuals = get_mutuals(followers, following)

print(f"\n--- Ghost Report ---")
print(f"👻 Ghosts (you follow, they don't): {len(ghosts)}")
print(f"🤩 Fans (they follow, you don't):   {len(fans)}")
print(f"🤝 Mutuals:                          {len(mutuals)}")

if ghosts:
    print(f"\nGhost accounts:")
    for ghost in sorted(ghosts):
        print(f"  - {ghost}")

# Diff logic
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

    # Trend analysis
    trends = get_trends(snapshots)
    if trends:
        print(f"\n--- Trend Analysis ---")
        print(f"📈 Follower growth since first scan: {trends['follower_growth']:+d}")
        print(f"📊 Following growth since first scan: {trends['following_growth']:+d}")
        print(f"🔍 Total scans: {trends['total_scans']}")
        print(f"🌟 Best growth period:  {trends['best_period']}")
        print(f"📉 Worst growth period: {trends['worst_period']}")
else:
    print("\nRun the app again to start tracking changes!")