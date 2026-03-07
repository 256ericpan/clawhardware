#!/usr/bin/env python3
"""
Daily update script for OpenClaw Hardware Projects
Fetches latest stats from GitHub and updates the data file
"""
import json
import os
import urllib.request
from datetime import datetime

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_OWNER = "256ericpan"
REPO_NAME = "clawhardware"
DATA_FILE = "data/projects.json"

SEARCH_QUERIES = [
    "openclaw+esp32",
    "openclaw+raspberry",
    "openclaw+jetson",
    "openclaw+robot",
    "openclaw+hardware",
    "openclaw+embedded",
    "esp32 ai assistant",
    "raspberry pi ai assistant",
]

def get_projects():
    """Load existing projects from data file"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_projects(projects):
    """Save projects to data file"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(projects, f, indent=2)

def search_github(query, per_page=10):
    """Search GitHub for repositories"""
    url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=stars&order=desc&per_page={per_page}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            return data.get("items", [])
    except Exception as e:
        print(f"Error searching {query}: {e}")
        return []

def fetch_repo_stats(owner, repo):
    """Fetch stats for a specific repository"""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching {owner}/{repo}: {e}")
        return None

def is_valid_openclaw_project(repo):
    """Check if repo is related to OpenClaw"""
    name = repo.get("full_name", "").lower()
    desc = repo.get("description", "").lower()
    topics = repo.get("topics", [])
    
    # Must have "openclaw" or similar in name/description
    keywords = ["openclaw", "ai assistant", "ai agent", "claude", "openai"]
    
    has_keyword = any(k in name or k in desc for k in keywords)
    
    # Or has relevant topics
    relevant_topics = ["openclaw", "ai-assistant", "ai-agent", "llm", "raspberry-pi", "esp32", "robotics"]
    has_topic = any(t in relevant_topics for t in topics)
    
    return has_keyword or has_topic

def determine_category(repo):
    """Determine project category based on name and topics"""
    name = repo.get("full_name", "").lower()
    topics = repo.get("topics", [])
    
    if any(t in topics for t in ["robotics", "robot", "humanoid", "quadruped"]):
        return "robotics"
    if any(t in topics for t in ["jetson", "nvidia", "edge-ai", "ai-compute"]):
        return "ai-compute"
    if any(t in topics for t in ["esp32", "iot", "embedded"]):
        return "embedded"
    if "raspberry" in name:
        return "embedded"
    if any(t in topics for t in ["seeed", "xiao"]):
        return "iot"
    
    return "alternative"

def determine_platforms(repo):
    """Determine hardware platforms"""
    name = repo.get("full_name", "").lower()
    desc = repo.get("description", "").lower()
    topics = repo.get("topics", [])
    
    platforms = []
    
    if "esp32" in name or "esp32" in desc or "esp32" in topics:
        platforms.append("ESP32")
    if "raspberry" in name or "raspberry pi" in desc:
        platforms.append("Raspberry Pi")
    if "jetson" in name or "nvidia" in desc:
        platforms.append("NVIDIA Jetson")
    if "xiao" in name or "xiao" in topics:
        platforms.append("Seeed XIAO")
    if "pico" in name:
        platforms.append("Pico")
    if "mobile" in topics or "ios" in topics or "android" in topics:
        platforms.append("Mobile")
    if "seeed" in name:
        platforms.append("Seeed")
    
    return platforms if platforms else ["PC"]

def main():
    print(f"🔄 Starting daily update at {datetime.now().isoformat()}")
    
    # Load existing projects
    projects = get_projects()
    existing_urls = {p.get("github_url", ""): p for p in projects}
    max_id = max((p.get("id", 0) for p in projects), default=0)
    
    print(f"📊 Current projects: {len(projects)}")
    
    # Search GitHub for new projects
    new_projects = []
    for query in SEARCH_QUERIES:
        print(f"🔍 Searching: {query}")
        results = search_github(query)
        
        for repo in results:
            url = repo.get("html_url", "")
            
            # Skip if already exists
            if url in existing_urls:
                continue
            
            # Validate it's OpenClaw related
            if not is_valid_openclaw_project(repo):
                continue
            
            # Create new project entry
            project = {
                "id": max_id + len(new_projects) + 1,
                "name": repo.get("name"),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "category": determine_category(repo),
                "platforms": determine_platforms(repo),
                "description": repo.get("description", "")[:200],
                "github_url": url,
                "seeedstudio": False,
                "product_links": [],
                "bom_cost": "Unknown",
                "daily_increment": 0,
                "created_at": datetime.now().isoformat() + "Z"
            }
            
            new_projects.append(project)
            print(f"  ➕ Found: {project['name']} ({project['stars']}⭐)")
    
    # Refresh stats for existing projects
    print("🔄 Refreshing existing project stats...")
    for project in projects:
        url = project.get("github_url", "")
        match = url.replace("https://github.com/", "").split("/")
        if len(match) >= 2:
            stats = fetch_repo_stats(match[0], match[1])
            if stats:
                old_stars = project.get("stars", 0)
                new_stars = stats.get("stargazers_count", 0)
                project["stars"] = new_stars
                project["daily_increment"] = max(0, new_stars - old_stars)
                project["forks"] = stats.get("forks_count", 0)
                project["updated_at"] = stats.get("updated_at")
    
    # Add new projects
    projects.extend(new_projects)
    
    # Sort by stars
    projects.sort(key=lambda x: -x.get("stars", 0))
    
    # Save
    save_projects(projects)
    
    print(f"✅ Update complete!")
    print(f"   Total projects: {len(projects)}")
    print(f"   New projects: {len(new_projects)}")

if __name__ == "__main__":
    main()
