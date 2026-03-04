def get_ghosts(followers, following):
    """Find accounts you follow that don't follow you back."""
    return following - followers

def get_fans(followers, following):
    """Find accounts that follow you but you don't follow back."""
    return followers - following

def get_mutuals(followers, following):
    """Find accounts that follow each other."""
    return followers & following