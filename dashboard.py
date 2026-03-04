from flask import Flask, render_template_string
from snapshot import load_snapshots
from ghost import get_ghosts, get_fans, get_mutuals
from trends import get_trends
from parser import parse_followers, parse_following

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>♡ instagram tracker ♡</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --rose: #c0185a;
            --rose-light: #e8547a;
            --blush: #f9e4ec;
            --cream: #fdf6f9;
            --deep: #1a0a0f;
            --muted: #9e6878;
            --white: #ffffff;
            --border: #f0c8d8;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'DM Sans', sans-serif;
            background-color: var(--cream);
            background-image:
                radial-gradient(ellipse at 0% 0%, rgba(192,24,90,0.08) 0%, transparent 60%),
                radial-gradient(ellipse at 100% 100%, rgba(232,84,122,0.06) 0%, transparent 60%);
            min-height: 100vh;
            color: var(--deep);
            padding: 3rem 2rem;
        }

        header {
            text-align: center;
            margin-bottom: 3rem;
        }

        header h1 {
            font-family: 'DM Serif Display', serif;
            font-size: 3rem;
            color: var(--rose);
            letter-spacing: -0.5px;
            margin-bottom: 0.4rem;
        }

        header h1 span {
            font-style: italic;
            color: var(--rose-light);
        }

        header p {
            color: var(--muted);
            font-size: 0.95rem;
            font-weight: 300;
            letter-spacing: 0.5px;
        }

        .divider {
            width: 60px;
            height: 2px;
            background: linear-gradient(90deg, var(--rose), var(--rose-light));
            margin: 1rem auto;
            border-radius: 2px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 1rem;
            margin-bottom: 2rem;
            max-width: 1100px;
            margin-left: auto;
            margin-right: auto;
        }

        .stat-card {
            background: var(--white);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem 1rem;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
            position: relative;
            overflow: hidden;
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--rose), var(--rose-light));
        }

        .stat-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(192,24,90,0.12);
        }

        .stat-card .number {
            font-family: 'DM Serif Display', serif;
            font-size: 2.8rem;
            color: var(--rose);
            line-height: 1;
            margin-bottom: 0.4rem;
        }

        .stat-card .label {
            font-size: 0.78rem;
            color: var(--muted);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }

        .section {
            background: var(--white);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            max-width: 1100px;
            margin-left: auto;
            margin-right: auto;
        }

        .section-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }

        .section-header h2 {
            font-family: 'DM Serif Display', serif;
            font-size: 1.4rem;
            color: var(--deep);
            font-weight: 400;
        }

        .section-header .tag {
            background: var(--blush);
            color: var(--rose);
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            letter-spacing: 0.3px;
        }

        .ghost-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .ghost-pill {
            background: var(--blush);
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 0.35rem 1rem;
            font-size: 0.82rem;
            font-weight: 500;
            color: var(--rose);
            transition: background 0.15s;
        }

        .ghost-pill:hover { background: #f5cedd; }

        .ghost-pill a {
            color: inherit;
            text-decoration: none;
        }

        .empty {
            color: var(--muted);
            font-style: italic;
            font-size: 0.9rem;
        }

        .notice {
            text-align: center;
            background: var(--blush);
            border: 1px solid var(--border);
            color: var(--muted);
            font-size: 0.82rem;
            padding: 0.6rem 1.5rem;
            border-radius: 999px;
            max-width: 600px;
            margin: -1.5rem auto 2.5rem;
        }

        canvas { max-height: 280px; }

        @media (max-width: 768px) {
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            header h1 { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <header>
        <h1>instagram <span>tracker</span> ♡</h1>
        <div class="divider"></div>
        <p>＼(^ᗜ^)／ &nbsp; your social life, visualized</p>
    </header>

    <div class="notice">
        accuracy depends on your instagram export date — re-export for the freshest data!
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="number">{{ stats.followers }}</div>
            <div class="label">followers</div>
        </div>
        <div class="stat-card">
            <div class="number">{{ stats.following }}</div>
            <div class="label">following</div>
        </div>
        <div class="stat-card">
            <div class="number">{{ stats.mutuals }}</div>
            <div class="label">mutuals</div>
        </div>
        <div class="stat-card">
            <div class="number">{{ stats.fans }}</div>
            <div class="label">fans (｡♥‿♥｡)</div>
        </div>
        <div class="stat-card">
            <div class="number">{{ stats.ghosts }}</div>
            <div class="label">ghosts (⌐■_■)</div>
        </div>
    </div>

    <div class="section">
        <div class="section-header">
            <h2>Follower History</h2>
            <span class="tag">over time</span>
        </div>
        <canvas id="growthChart"></canvas>
    </div>

    <div class="section">
        <div class="section-header">
            <h2>Ghost Accounts</h2>
            <span class="tag">{{ ghost_list|length }} accounts</span>
        </div>
        {% if ghost_list %}
            <div class="ghost-grid">
                {% for ghost in ghost_list %}
                    <span class="ghost-pill">
                        <a href="https://instagram.com/{{ ghost }}" target="_blank">@{{ ghost }}</a>
                    </span>
                {% endfor %}
            </div>
        {% else %}
            <p class="empty">＼(^ᗜ^)／ no ghosts found!</p>
        {% endif %}
    </div>

    <div class="section">
        <div class="section-header">
            <h2>Trend Analysis</h2>
            <span class="tag">followers vs ghosts</span>
        </div>
        <canvas id="trendChart"></canvas>
    </div>

    <script>
        const labels = {{ labels | tojson }};
        const followerData = {{ follower_data | tojson }};
        const ghostData = {{ ghost_data | tojson }};

        const rose = '#c0185a';
        const roseLight = '#e8547a';
        const roseFill = 'rgba(192,24,90,0.08)';
        const lightFill = 'rgba(232,84,122,0.08)';

        const chartDefaults = {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: '#9e6878',
                        font: { family: 'DM Sans', size: 12, weight: '500' },
                        usePointStyle: true,
                        pointStyleWidth: 8
                    }
                }
            },
            scales: {
                x: {
                    ticks: { color: '#c0a0ac', font: { family: 'DM Sans', size: 11 }, maxRotation: 30 },
                    grid: { color: 'rgba(240,200,216,0.4)' },
                    border: { color: 'rgba(240,200,216,0.6)' }
                },
                y: {
                    ticks: { color: '#c0a0ac', font: { family: 'DM Sans', size: 11 } },
                    grid: { color: 'rgba(240,200,216,0.4)' },
                    border: { color: 'rgba(240,200,216,0.6)' }
                }
            }
        };

        new Chart(document.getElementById('growthChart'), {
            type: 'line',
            data: {
                labels,
                datasets: [{
                    label: 'followers',
                    data: followerData,
                    borderColor: rose,
                    backgroundColor: roseFill,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: rose,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    borderWidth: 2
                }]
            },
            options: chartDefaults
        });

        new Chart(document.getElementById('trendChart'), {
            type: 'line',
            data: {
                labels,
                datasets: [
                    {
                        label: 'followers',
                        data: followerData,
                        borderColor: rose,
                        backgroundColor: roseFill,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: rose,
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        borderWidth: 2
                    },
                    {
                        label: 'ghosts',
                        data: ghostData,
                        borderColor: roseLight,
                        backgroundColor: lightFill,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: roseLight,
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        borderWidth: 2
                    }
                ]
            },
            options: chartDefaults
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    followers = parse_followers()
    following = parse_following()
    snapshots = load_snapshots()

    ghosts = get_ghosts(followers, following)
    fans = get_fans(followers, following)
    mutuals = get_mutuals(followers, following)

    stats = {
        "followers": len(followers),
        "following": len(following),
        "mutuals": len(mutuals),
        "fans": len(fans),
        "ghosts": len(ghosts)
    }

    trends = get_trends(snapshots) if len(snapshots) >= 2 else None

    labels = []
    follower_data = []
    ghost_data = []

    if trends:
        for point in trends["trend_data"]:
            labels.append(point["timestamp"])
            follower_data.append(point["follower_count"])
            ghost_data.append(point["ghosts"])

    return render_template_string(
        HTML,
        stats=stats,
        ghost_list=sorted(ghosts),
        labels=labels,
        follower_data=follower_data,
        ghost_data=ghost_data
    )

if __name__ == "__main__":
    app.run(debug=True)