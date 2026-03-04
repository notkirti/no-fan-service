# no-fan-service ♡ 

> your instagram follow tracker — visualized beautifully.

![Python](https://img.shields.io/badge/Python-3.9+-ff69b4?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-ff69b4?style=flat-square&logo=flask&logoColor=white)
![Rich](https://img.shields.io/badge/Rich-CLI-ff69b4?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-ff69b4?style=flat-square)

a local tool that parses your instagram data export to track followers,
detect ghosts, and visualise trends over time — no login required, no
third-party access, no ToS violations.

---

## features

- **ghost detection** — find accounts you follow that don't follow back
- **trend analysis** — track follower growth across multiple scans
- **rich CLI** — beautiful pink terminal output with kaomoji ＼(^ᗜ^)／
- **web dashboard** — local browser UI with live charts
- **100% private** — all data stays on your machine, nothing is pushed to github

---

## getting started

### 1. get your instagram data
1. open instagram → settings → your activity → download your information
2. select **followers and following** only
3. format: **JSON**
4. wait for the email from instagram, then download and unzip

### 2. clone the repo
```bash
git clone https://github.com/notkirti/no-fan-service.git
cd no-fan-service
```

### 3. set up environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install rich flask
```

### 4. add your data
drop `followers_1.json` and `following.json` into the `data/` folder.

### 5. run the CLI
```bash
python main.py
```

### 6. run the dashboard
```bash
python dashboard.py
```
then open `http://localhost:5000` in your browser.

---

## project structure
```
no-fan-service/
├── data/              # your instagram export files (gitignored)
├── snapshots/         # saved snapshots over time (gitignored)
├── main.py            # CLI entry point
├── parser.py          # reads instagram JSON export
├── snapshot.py        # saves and loads timestamped snapshots
├── diff.py            # detects changes between snapshots
├── ghost.py           # ghost follower detection
├── trends.py          # trend analysis across snapshots
└── dashboard.py       # flask web dashboard
```

---

## how it works

1. instagram exports your follower/following data as JSON files
2. the parser reads and cleans these into python sets
3. each run saves a timestamped snapshot locally
4. snapshots are compared to detect unfollowers and new followers
5. the dashboard visualises everything in your browser

---

## known limitations

- accuracy depends on when instagram processed your export request —
  re-export for the freshest data
- ghost list may include deactivated accounts since instagram's export
  doesn't distinguish them
- instagram occasionally changes their export format — if you hit a
  parsing error, open an issue

---

## privacy

all instagram data stays local on your machine. the `data/` and
`snapshots/` folders are gitignored and never pushed to github.

---

## tech stack

| tool | purpose |
|------|---------|
| Python | core logic |
| Rich | terminal UI |
| Flask | local web server |
| Chart.js | browser graphs |
| JSON files | local storage |