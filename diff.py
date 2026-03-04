def get_diff(old_snapshot, new_snapshot):
    """Compare two snapshots and return what changed."""
    old_followers = set(old_snapshot["followers"])
    new_followers = set(new_snapshot["followers"])
    old_following = set(old_snapshot["following"])
    new_following = set(new_snapshot["following"])

    return {
        "unfollowed_you": old_followers - new_followers,
        "you_unfollowed": old_following - new_following,
        "new_followers": new_followers - old_followers,
        "new_following": new_following - old_following
    }