#!/usr/bin/env python3
"""
Daily Xiaohongshu Post Generator for OpenClaw Hardware Integration Monitor
Generates daily posts based on the latest hardware integration data
"""

import json
import requests
from datetime import datetime
import random

def fetch_latest_projects():
    """Fetch the latest project data from GitHub raw content"""
    try:
        # Fetch the HTML file and extract JavaScript data
        url = "https://raw.githubusercontent.com/256ericpan/clawhardware/main/index.html"
        response = requests.get(url, timeout=30)
        html_content = response.text
        
        # Extract the projects array from JavaScript (simplified parsing)
        # In a real implementation, you'd use a proper HTML/JS parser
        if 'const projects = [' in html_content:
            start_idx = html_content.find('const projects = [')
            end_idx = html_content.find('];', start_idx)
            if start_idx != -1 and end_idx != -1:
                projects_js = html_content[start_idx:end_idx+1]
                # This is a simplified approach - in practice, you'd need proper JS parsing
                return projects_js
        
        return None
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return None

def generate_post_content():
    """Generate Xiaohongshu post content based on current projects"""
    
    # Hardcoded project data for now (would be dynamic in production)
    projects_data = [
        {
            "name": "Official OpenClaw Repository",
            "stars": 251095,
            "category": "robotics",
            "platforms": ["any"],
            "description": "Your own personal AI assistant. Any OS. Any Platform. The lobster way."
        },
        {
            "name": "clawd-reachy-mini", 
            "stars": 26,
            "category": "robotics",
            "platforms": ["robotics", "python"],
            "description": "Reachy Mini robotics integration project for OpenClaw"
        },
        {
            "name": "WireClaw",
            "stars": 30,
            "category": "iot", 
            "platforms": ["esp32", "arduino", "iot"],
            "description": "ESP32 AI agent with persistent memory and offline rule engine"
        },
        {
            "name": "openclaw-esp32c3-xiao-node",
            "stars": 4,
            "category": "embedded",
            "platforms": ["esp32", "xiao"],
            "tags": ["seeed-studio"],
            "description": "OpenClaw node firmware for Seeed XIAO ESP32-C3 + Expansion Board (~$13 IoT peripheral)"
        }
    ]
    
    # Calculate total stars and active projects
    total_stars = sum(p["stars"] for p in projects_data)
    active_projects = len(projects_data)
    
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Generate post content
    post_content = f"""🦞 OpenClaw硬件生态日报 | {today}

开源AI助手OpenClaw硬件生态持续活跃！

🔥 今日数据速览：
• 活跃项目：{active_projects}个
• 总Stars：{total_stars:,}+
• 跨平台支持：ESP32/Arduino/Raspberry Pi/Jetson

🔧 热门项目推荐：

🤖 机器人控制
• Official OpenClaw：{projects_data[0]['stars']:,} stars - 核心仓库持续更新
• clawd-reachy-mini：{projects_data[1]['stars']} stars - Reachy Mini机器人集成

🌐 IoT物联网  
• WireClaw：{projects_data[2]['stars']} stars - ESP32 AI代理，离线规则引擎
• IOnode：ESP32设备舰队管理，NATS协议支持

⚡ Seeed Studio亮点
• openclaw-esp32c3-xiao-node：{projects_data[3]['stars']} stars
• 专为Seeed XIAO ESP32-C3开发
• 成本仅~$13，性价比超高！

🔗 实时监控：https://256ericpan.github.io/clawhardware/

💡 今日建议：
入门开发者可以从Seeed XIAO开始，成本低功能强！

#OpenClaw #开源硬件 #SeeedStudio #XIAO #ESP32 #IoT #机器人 #AI助手 #每日更新

大家今天想用OpenClaw做什么项目？评论区聊聊！👇

---

🎨 **配图建议**：
中心：OpenClaw龙虾Logo
内圈：ESP32/XIAO、Raspberry Pi、Jetson三大硬件载体
外圈：各平台对应的开源项目图标
底部：实时监控链接和GitHub Stars统计
"""
    
    return post_content

def main():
    """Main function to generate and save the post"""
    post_content = generate_post_content()
    
    # Save to file with today's date
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"xiaohongshu_post_{today}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(post_content)
    
    print(f"Generated Xiaohongshu post: {filename}")
    print("\n" + "="*50)
    print(post_content)
    print("="*50)

if __name__ == "__main__":
    main()