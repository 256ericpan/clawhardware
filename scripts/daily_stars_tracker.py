#!/usr/bin/env python3
"""
Daily GitHub Stars Tracker
Run via cron: 0 8 * * * /usr/bin/python3 /path/to/daily_stars_tracker.py

Fetches current star counts, calculates daily increment,
updates projects.json, and maintains stars_history.json.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

GITHUB_TOKEN = os.environ.get("CLAWHARDWARE_GITHUB_TOKEN", "") or os.environ.get("GITHUB_TOKEN", "")
PROJECTS_FILE = Path(__file__).parent.parent / "data" / "projects.json"
HISTORY_FILE = Path(__file__).parent.parent / "data" / "stars_history.json"
SKIPPED_FILE = Path(__file__).parent.parent / "data" / "skipped_repos.json"


def get_owner_repo(url):
    parts = url.rstrip("/").split("/")
    if len(parts) >= 2 and parts[-2] and parts[-1]:
        return parts[-2], parts[-1]
    return None, None


def fetch_stars_batch(repos, token):
    """Fetch stars for multiple repos in batch using GraphQL API."""
    if not repos:
        return {}
    
    query = """
    query {
    """
    for i, (owner, repo) in enumerate(repos):
        query += f"""
        r{i}: repository(owner: "{owner}", name: "{repo}") {{
            stargazerCount
        }}
    """
    query += "}"
    
    import urllib.request
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            results = {}
            if "data" in data:
                for i, (owner, repo) in enumerate(repos):
                    r = data["data"].get(f"r{i}", {}) or {}
                    results[f"{owner}/{repo}"] = r.get("stargazerCount") or 0
            return results
    except Exception as e:
        print(f"Batch fetch error: {e}", file=sys.stderr)
        return {}


def fetch_stars_individual(owner, repo, token):
    """Fetch stars for a single repo via REST API."""
    import urllib.request
    url = f"https://api.github.com/repos/{owner}/{repo}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "clawhardware-tracker/1.0"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data.get("stargazer_count", 0)
    except Exception as e:
        return None


def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    print(f"[{datetime.now().isoformat()}] Starting daily stars tracker...")
    
    projects = load_json(PROJECTS_FILE, [])
    history = load_json(HISTORY_FILE, {})
    skipped = load_json(SKIPPED_FILE, [])
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # Parse all repos
    repos = []
    repo_indices = {}
    for i, p in enumerate(projects):
        url = p.get("github_url", "")
        owner, repo = get_owner_repo(url)
        if owner and repo:
            repos.append((owner, repo))
            repo_indices[f"{owner}/{repo}"] = i
        else:
            skipped.append({"project": p.get("name"), "url": url, "skipped_at": today})
    
    # Fetch stars
    print(f"Fetching stars for {len(repos)} repos...")
    batch_results = fetch_stars_batch(repos, GITHUB_TOKEN)
    
    updated = 0
    errors = 0
    new_stars_data = {}
    
    for owner, repo in repos:
        key = f"{owner}/{repo}"
        idx = repo_indices[key]
        current_stars = batch_results.get(key)
        
        if current_stars is None:
            # Fallback to individual fetch
            current_stars = fetch_stars_individual(owner, repo, GITHUB_TOKEN)
        
        if current_stars is None:
            errors += 1
            print(f"  ERROR: {key}")
            continue
        
        prev = history.get(key, {})
        prev_stars = prev.get(today) or prev.get("last_stars", 0)
        increment = current_stars - prev_stars
        
        # Update project
        projects[idx]["stars"] = current_stars
        projects[idx]["daily_increment"] = increment
        
        # Update history
        new_stars_data[key] = {
            "last_stars": current_stars,
            today: current_stars
        }
        
        updated += 1
        if updated % 20 == 0:
            print(f"  Processed {updated}/{len(repos)}...")
    
    # Merge history (keep last 30 days)
    for key, data in new_stars_data.items():
        if key not in history:
            history[key] = {}
        history[key].update(data)
        # Keep only last 60 days to prevent bloat
        dates = sorted(history[key].keys())
        if len(dates) > 60:
            for d in dates[:-60]:
                del history[key][d]
    
    # Save
    save_json(PROJECTS_FILE, projects)
    save_json(HISTORY_FILE, history)
    if skipped:
        save_json(SKIPPED_FILE, skipped)
    
    # Report
    print(f"\n=== {today} Stars Update ===")
    print(f"Updated: {updated}, Errors: {errors}")
    
    # Top gainers today
    top_gainers = sorted(projects, key=lambda x: x.get("daily_increment", 0), reverse=True)[:10]
    print("\n📈 Top Gainers Today:")
    for p in top_gainers:
        inc = p.get("daily_increment", 0)
        if inc != 0:
            print(f"  +{inc:,} | {p['name']} ({p['stars']:,})")
    
    # Save summary for cron report
    summary = {
        "date": today,
        "updated": updated,
        "errors": errors,
        "top_gainers": [
            {"name": p["name"], "increment": p.get("daily_increment", 0), "stars": p["stars"]}
            for p in top_gainers[:5]
        ]
    }
    summary_file = Path(__file__).parent.parent / "data" / "last_summary.json"
    save_json(summary_file, summary)
    
    print(f"\nDone! Summary saved.")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
