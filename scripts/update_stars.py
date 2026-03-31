#!/usr/bin/env python3
"""Update projects.json with new projects and refreshed star counts."""
import json
import urllib.request
import urllib.error
import time

TOKEN = "${GITHUB_TOKEN}"

def gh_api(path):
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  ERROR {path}: {e}")
        return None

def get_repo(owner, repo):
    return gh_api(f"/repos/{owner}/{repo}")

# Load existing projects
with open("data/projects.json") as f:
    projects = json.load(f)

existing_urls = {p["github_url"] for p in projects}
url_to_project = {p["github_url"]: p for p in projects}

# Projects to check for star updates (top ones by old star count)
top_repos = [
    ("openclaw", "openclaw"),
    ("zhayujie", "chatgpt-on-wechat"),
    ("CherryHQ", "cherry-studio"),
    ("HKUDS", "nanobot"),
    ("zeroclaw-labs", "zeroclaw"),
    ("sipeed", "picoclaw"),
    ("memovai", "mimiclaw"),
    ("huangjunsen0406", "py-xiaozhi"),
    ("martin-ger", "esp32_nat_router"),
    ("tnm", "zclaw"),
    ("RightNow-AI", "picolm"),
    ("Seeed-Studio", "ModelAssistant"),
    ("Seeed-Studio", "reCamera"),
    ("brenpoly", "be-more-agent"),
    ("liu233w", "xiaozhi-esp32-server-golang"),
    ("nguyenduchoai", "bizclaw"),
    ("Seeed-Studio", "SenseCraft-AI_Server"),
    ("d4rkmen", "M5Gemini"),
    ("M64GitHub", "WireClaw"),
    ("ArturSkowronski", "clawd-reachy-mini"),
    ("Demwunz", "openclaw-pi-installation"),
    ("apisit31120", "miniclaw-esp32"),
    ("turmyshevd", "openclawgotchi"),
    ("This-Is-Captain-Code", "monagotchi"),
    ("LooperRobotics", "OpenClaw-Robotics"),
    ("ychenjk-sudo", "daily-paper-skill"),
    ("next-open-ai", "openclawx"),
    ("tigerbryan", "openclaw-xiaozhi"),
    ("tomrikert", "clawbody"),
    ("sanchorelaxo", "openclaw-raspberry-installer"),
    ("xuankuzcr", "openclaw-paper-digest"),
    ("chilu18", "openclaw-esp32c3-xiao-node"),
    ("danmartinez78", "VectorClaw"),
    ("omeriko9", "HeyClawy"),
    ("lorryjovens-hub", "clawlink-triarch"),
    ("rhuanssauro", "jetson-openclaw"),
    ("leohuang8688", "XiaozhiClaw"),
]

print("Updating star counts for existing projects...")
star_updates = {}
for owner, repo in top_repos:
    r = get_repo(owner, repo)
    if r:
        star_updates[f"https://github.com/{owner}/{repo}"] = r["stargazers_count"]
        print(f"  {owner}/{repo}: {r['stargazers_count']}")
    time.sleep(0.3)

# New projects found from search
new_projects_data = [
    {
        "name": "xiaozhi-esp32-server-golang",
        "owner": "hackers365",
        "stars": 235,
        "description": "golang版本的小智后端服务，支持websocket和mqtt+udp协议，支持声纹识别/声音克隆/知识库/mcp远程调用/openclaw等功能",
        "platforms": ["ESP32"],
        "category": "iot",
        "highlights": ["Go后端", "WebSocket/MQTT/UDP", "声纹识别"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "~$15",
    },
    {
        "name": "ClawPuter",
        "owner": "bryant24hao",
        "stars": 78,
        "description": "ClawPuter — pixel desktop companion for M5Stack Cardputer (ESP32-S3). AI chat, voice input, real-time weather, synced macOS desktop pet.",
        "platforms": ["ESP32", "M5Stack"],
        "category": "iot",
        "highlights": ["M5Stack Cardputer", "AI chat", "桌面宠物"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "~$30",
    },
    {
        "name": "openclaw-control-center",
        "owner": "TianyiDataScience",
        "stars": 3144,
        "description": "Turn OpenClaw from a black box into a local control center you can see, trust, and control.",
        "platforms": ["PC"],
        "category": "tool",
        "highlights": ["本地控制中心", "可视化仪表板"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "Free",
    },
    {
        "name": "agent-sessions",
        "owner": "jazzyalex",
        "stars": 418,
        "description": "Session browser + Agent Cockpit + Analytics + Limits tracker for Codex CLI, Claude Code, OpenCode, Gemini CLI, Factory Droid, GitHub Copilot CLI & OpenClaw.",
        "platforms": ["Mac"],
        "category": "tool",
        "highlights": ["macOS原生", "会话管理", "限流追踪"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "Free",
    },
    {
        "name": "opik-openclaw",
        "owner": "comet-ml",
        "stars": 395,
        "description": "Official plugin for OpenClaw that exports agent traces to Opik. See and monitor agent behaviour, cost, tokens, errors and more.",
        "platforms": ["PC", "Mac", "Linux", "Windows"],
        "category": "tool",
        "highlights": ["Agent监控", "成本追踪", "错误日志"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "Free",
    },
    {
        "name": "clawmetry",
        "owner": "vivekchand",
        "stars": 213,
        "description": "See your agent think. Real-time observability dashboard for OpenClaw AI agents.",
        "platforms": ["PC", "Mac", "Linux", "Windows"],
        "category": "tool",
        "highlights": ["实时观测", "思维可视化"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "Free",
    },
    {
        "name": "Kongnitive-EdgeMCP",
        "owner": "Kongnitive",
        "stars": 9,
        "description": "An MCP base layer running on ESP32 that exposes hardware capabilities to AI. AI reads logs, pushes scripts, swaps drivers, and iterates device logic directly through MCP tools.",
        "platforms": ["ESP32"],
        "category": "iot",
        "highlights": ["ESP32 MCP", "硬件抽象层"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "~$10",
    },
    {
        "name": "RealWorldClaw",
        "owner": "brianzhibo-design",
        "stars": 7,
        "description": "The open platform where any AI gains any physical capability — through 3D printing and open hardware.",
        "platforms": ["3D Printing"],
        "category": "robotics",
        "highlights": ["3D打印", "开源硬件", "AI物理能力"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "Varies",
    },
    {
        "name": "openclaw-setup",
        "owner": "anomixer",
        "stars": 38,
        "description": "OpenClaw + Ollama + Telegram Quick Setup Guide | 快速安裝教學",
        "platforms": ["PC", "Linux"],
        "category": "tool",
        "highlights": ["Ollama集成", "Telegram", "快速部署"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "Free",
    },
    {
        "name": "GUI-Agent-Harness",
        "owner": "Fzkuji",
        "stars": 21,
        "description": "Vision-based desktop automation skills for OpenClaw agents on macOS. See, learn, click — any app.",
        "platforms": ["Mac"],
        "category": "tool",
        "highlights": ["macOS视觉自动化", "桌面UI交互"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "Free",
    },
    {
        "name": "Star-Office-UI-Node",
        "owner": "wangmiaozero",
        "stars": 8,
        "description": "A pixelated office dashboard for multi-agent collaboration: visualizes the real-time work status of the AI assistant (OpenClaw/Lobster).",
        "platforms": ["PC"],
        "category": "tool",
        "highlights": ["多智能体协作", "办公室仪表板"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "Free",
    },
    {
        "name": "claw-stream-bot",
        "owner": "averyjennings",
        "stars": 6,
        "description": "Enable OpenClaw agents to see and participate in Twitch streams for Claw Con.",
        "platforms": ["PC"],
        "category": "tool",
        "highlights": ["Twitch集成", "直播互动"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "Free",
    },
    {
        "name": "openclaw-security",
        "owner": "X-Scale-AI",
        "stars": 4,
        "description": "Harden your OpenClaw and NemoClaw AI agent installations -- security audit tools.",
        "platforms": ["PC", "Linux"],
        "category": "tool",
        "highlights": ["安全加固", "安全审计"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "Free",
    },
    {
        "name": "agenthq",
        "owner": "98kiran",
        "stars": 3,
        "description": "Lightweight ops dashboard for OpenClaw agent teams. See who's online, what they're working on.",
        "platforms": ["PC"],
        "category": "tool",
        "highlights": ["团队仪表板", "任务管理"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "Free",
    },
    {
        "name": "ClawDeck",
        "owner": "KtKID",
        "stars": 2,
        "description": "A clear and focused interface for interacting with OpenClaw tasks — see agent states, understand progress.",
        "platforms": ["PC"],
        "category": "tool",
        "highlights": ["任务界面", "进度追踪"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "Free",
    },
    {
        "name": "hardware-wiki-generator",
        "owner": "lsw031105guge-bit",
        "stars": 1,
        "description": "OpenClaw skill for generating bilingual (Chinese/English) hardware product wiki documentation for Docusaurus/Seeed Studio/Adafruit platforms.",
        "platforms": ["Seeed Studio"],
        "category": "maker",
        "highlights": ["Seeed Studio", "文档生成", "中英双语"],
        "seeedstudio": True,
        "product_links": [],
        "bom_cost": "Free",
    },
    {
        "name": "reachy-claw",
        "owner": "suharvest",
        "stars": 7,
        "description": "Sub-200ms voice assistant for Reachy Mini — powered by sherpa-onnx and OpenClaw.",
        "platforms": ["Reachy Mini"],
        "category": "robotics",
        "highlights": ["Reachy Mini", "低延迟语音", "200ms响应"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "~$500",
    },
    {
        "name": "reachyclaw",
        "owner": "EdLuxAI",
        "stars": 2,
        "description": "ReachyClaw - Your OpenClaw AI agent embodied in a Reachy Mini robot. OpenClaw is the brain; OpenAI Realtime API handles voice I/O.",
        "platforms": ["Reachy Mini"],
        "category": "robotics",
        "highlights": ["Reachy Mini", "语音交互", "AI具身"],
        "seeedstudio": False,
        "product_links": [],
        "bom_cost": "~$500",
    },
]

# Apply star updates
updated_count = 0
for url, new_stars in star_updates.items():
    if url in url_to_project:
        old_stars = url_to_project[url]["stars"]
        url_to_project[url]["stars"] = new_stars
        url_to_project[url]["daily_increment"] = max(0, new_stars - old_stars)
        updated_count += 1

print(f"\nUpdated {updated_count} star counts")

# Add new projects
added = 0
for np in new_projects_data:
    url = f"https://github.com/{np['owner']}/{np['name']}"
    if url not in existing_urls:
        new_entry = {
            "id": len(projects) + 1,
            "name": np["name"],
            "stars": np["stars"],
            "category": np["category"],
            "platforms": np["platforms"],
            "description": np["description"],
            "highlights": np["highlights"],
            "github_url": url,
            "seeedstudio": np["seeedstudio"],
            "product_links": np["product_links"],
            "bom_cost": np["bom_cost"],
            "daily_increment": 0,
            "created_at": "2026-03-31T00:00:00Z",
        }
        projects.append(new_entry)
        existing_urls.add(url)
        added += 1
        print(f"  + NEW: {np['owner']}/{np['name']} ({np['stars']} stars)")

print(f"\nAdded {added} new projects")
print(f"Total projects: {len(projects)}")

# Save
with open("data/projects.json", "w") as f:
    json.dump(projects, f, indent=2, ensure_ascii=False)

print("Saved data/projects.json")