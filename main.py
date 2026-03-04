from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.text import Text

from parser import parse_followers, parse_following
from snapshot import save_snapshot, load_snapshots
from diff import get_diff
from ghost import get_ghosts, get_fans, get_mutuals
from trends import get_trends

console = Console()

KAOMOJI_HAPPY    = "＼(^ᗜ^)／"
KAOMOJI_GHOST    = "(⌐■_■)"
KAOMOJI_SAD      = "(╥_╥)"
KAOMOJI_SPARKLE  = "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧"
KAOMOJI_SURPRISED = "( ﾟдﾟ)"
KAOMOJI_CUTE     = "(｡♥‿♥｡)"

def show_banner():
    console.print(Panel.fit(
        f"[bold magenta]♡ instagram unfollow tracker ♡[/bold magenta]\n"
        f"[hot_pink2]{KAOMOJI_SPARKLE} your social life, visualized[/hot_pink2]",
        border_style="hot_pink2",
        padding=(1, 4)
    ))

def show_summary(followers, following, ghosts, fans, mutuals):
    table = Table(
        title=f"[bold magenta]♡ your stats {KAOMOJI_CUTE} ♡[/bold magenta]",
        box=box.ROUNDED,
        border_style="hot_pink2",
        header_style="bold magenta"
    )
    table.add_column("metric", style="bold magenta")
    table.add_column("count", style="bold hot_pink2", justify="right")

    table.add_row("followers", str(len(followers)))
    table.add_row("following", str(len(following)))
    table.add_row("mutuals", str(len(mutuals)))
    table.add_row("fans (they follow, u don't)", str(len(fans)))
    table.add_row("ghosts (u follow, they don't)", str(len(ghosts)))

    console.print(table)

def show_ghosts(ghosts):
    if not ghosts:
        console.print(f"\n[bold magenta]✧ no ghosts found! {KAOMOJI_HAPPY}[/bold magenta]")
        return

    table = Table(
        title=f"[bold magenta]ghosts who don't follow back {KAOMOJI_GHOST}[/bold magenta]",
        box=box.ROUNDED,
        border_style="hot_pink2",
        header_style="bold magenta"
    )
    table.add_column("username", style="magenta")
    table.add_column("profile", style="hot_pink2 dim")

    for ghost in sorted(ghosts):
        table.add_row(ghost, f"instagram.com/{ghost}")

    console.print(table)

def show_diff(diff):
    console.print(Panel.fit(
        f"[bold magenta]changes since last scan {KAOMOJI_SURPRISED}[/bold magenta]",
        border_style="hot_pink2"
    ))

    items = [
        ("unfollowed you", diff["unfollowed_you"], "magenta", KAOMOJI_SAD),
        ("you unfollowed", diff["you_unfollowed"], "hot_pink2", KAOMOJI_GHOST),
        ("new followers", diff["new_followers"], "magenta", KAOMOJI_HAPPY),
        ("new following", diff["new_following"], "hot_pink2", KAOMOJI_SPARKLE),
    ]

    for label, users, color, kaomoji in items:
        if users:
            console.print(f"\n[bold {color}]♡ {label} {kaomoji}[/bold {color}]")
            for user in sorted(users):
                console.print(f"  [{color}]• {user}[/{color}]")
        else:
            console.print(f"[dim magenta]♡ {label}: none[/dim magenta]")

def show_trends(trends):
    if not trends:
        return

    console.print(Panel.fit(
        f"[bold magenta]trend analysis {KAOMOJI_SPARKLE}[/bold magenta]",
        border_style="hot_pink2"
    ))

    table = Table(
        box=box.ROUNDED,
        border_style="hot_pink2",
        header_style="bold magenta"
    )
    table.add_column("metric", style="bold magenta")
    table.add_column("value", style="bold hot_pink2", justify="right")

    growth = trends["follower_growth"]
    growth_str = f"+{growth}" if growth > 0 else str(growth)
    growth_color = "magenta" if growth > 0 else "hot_pink2"

    table.add_row("total scans", str(trends["total_scans"]))
    table.add_row("follower growth", f"[{growth_color}]{growth_str}[/{growth_color}]")
    table.add_row("best period", trends["best_period"])
    table.add_row("worst period", trends["worst_period"])

    console.print(table)

# --- main ---
show_banner()

followers = parse_followers()
following = parse_following()

ghosts = get_ghosts(followers, following)
fans = get_fans(followers, following)
mutuals = get_mutuals(followers, following)

save_snapshot(followers, following)
snapshots = load_snapshots()

show_summary(followers, following, ghosts, fans, mutuals)
show_ghosts(ghosts)

if len(snapshots) >= 2:
    diff = get_diff(snapshots[-2], snapshots[-1])
    show_diff(diff)
    trends = get_trends(snapshots)
    show_trends(trends)
else:
    console.print(f"\n[dim magenta]run the app again to start tracking changes! {KAOMOJI_CUTE}[/dim magenta]")