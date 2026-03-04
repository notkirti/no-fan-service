from datetime import datetime

def get_trends(snapshots):
    """Analyse trends across all snapshots over time."""
    if len(snapshots) < 2:
        return None

    trend_data = []

    for snapshot in snapshots:
        followers = set(snapshot["followers"])
        following = set(snapshot["following"])
        timestamp = snapshot["timestamp"]

        trend_data.append({
            "timestamp": timestamp,
            "follower_count": len(followers),
            "following_count": len(following),
            "ghosts": len(following - followers),
            "fans": len(followers - following),
            "mutuals": len(followers & following)
        })

    # Growth stats
    first = trend_data[0]
    latest = trend_data[-1]

    follower_growth = latest["follower_count"] - first["follower_count"]
    following_growth = latest["following_count"] - first["following_count"]

    # Best and worst periods
    best_growth = max(
        range(1, len(trend_data)),
        key=lambda i: trend_data[i]["follower_count"] - trend_data[i-1]["follower_count"]
    )
    worst_growth = min(
        range(1, len(trend_data)),
        key=lambda i: trend_data[i]["follower_count"] - trend_data[i-1]["follower_count"]
    )

    return {
        "trend_data": trend_data,
        "follower_growth": follower_growth,
        "following_growth": following_growth,
        "best_period": trend_data[best_growth]["timestamp"],
        "worst_period": trend_data[worst_growth]["timestamp"],
        "total_scans": len(snapshots)
    }