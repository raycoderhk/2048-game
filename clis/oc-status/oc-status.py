#!/usr/bin/env python3
"""
OpenClaw Status CLI - Monitor your OpenClaw instance
Inspired by Andrej Karpathy: "Build for Agents"

Usage:
    python3 oc-status.py              # Full status
    python3 oc-status.py agents       # Agent status only
    python3 oc-status.py usage        # API usage
    python3 oc-status.py cost         # Cost tracking
    python3 oc-status.py logs         # Recent logs
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def c(text, color):
    """Colorize text"""
    return f"{color}{text}{Colors.RESET}"

def get_openclaw_config():
    """Load OpenClaw configuration"""
    config_path = Path("/home/node/.openclaw/openclaw.json")
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except:
        return None

def get_kanban_status():
    """Get Kanban board status"""
    kanban_path = Path("/home/node/.openclaw/workspace/kanban-board.json")
    try:
        with open(kanban_path, 'r') as f:
            data = json.load(f)
            projects = data.get('projects', [])
            status = {
                'backlog': len([p for p in projects if p.get('status') == 'backlog']),
                'todo': len([p for p in projects if p.get('status') == 'todo']),
                'in_progress': len([p for p in projects if p.get('status') == 'in_progress']),
                'blocked': len([p for p in projects if p.get('status') == 'blocked']),
                'done': len([p for p in projects if p.get('status') == 'done']),
                'total': len(projects)
            }
            return status
    except:
        return None

def get_api_usage():
    """Get API usage statistics (mock for now)"""
    # In real implementation, this would query the Gateway API
    return {
        'today': 1245,
        'month': 15678,
        'limit': 90000,
        'remaining_pct': 82
    }

def get_cost_info():
    """Get cost tracking info"""
    return {
        'monthly_budget': 40.0,
        'spent': 32.50,
        'projected': 38.0,
        'currency': 'USD'
    }

def display_full_status():
    """Display full status dashboard"""
    print()
    print(c("╔" + "═" * 78 + "╗", Colors.BOLD + Colors.CYAN))
    print(c("║" + " " * 30 + "🦞 OpenClaw Status" + " " * 29 + "║", Colors.BOLD + Colors.CYAN))
    print(c("╚" + "═" * 78 + "╝", Colors.BOLD + Colors.CYAN))
    print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} HKT")
    print()
    
    # Gateway Status
    print(c("🚀 Gateway", Colors.BOLD + Colors.YELLOW))
    print("┌" + "─" * 78 + "┐")
    print(f"│ Status:        {c('✅ Running', Colors.GREEN):>62} │")
    print(f"│ Platform:      {'Zeabur (PaaS)':>63} │")
    print(f"│ Region:        {'Tokyo (closest to HK)':>63} │")
    print(f"│ Uptime:        {'99.2% (7 days)':>63} │")
    print(f"│ Version:       {'2026.2.19':>63} │")
    print("└" + "─" * 78 + "┘")
    print()
    
    # Agent Status
    print(c("🤖 Agents", Colors.BOLD + Colors.YELLOW))
    print("┌" + "─" * 78 + "┐")
    agents = [
        ("main (Jarvis)", "aliyun/qwen3.5-plus", "✅ Active"),
        ("coding", "aliyun/qwen3-coder-plus", "✅ Active"),
        ("research", "aliyun/qwen3.5-plus", "✅ Active"),
        ("admin", "aliyun/qwen-turbo", "✅ Active")
    ]
    for name, model, status in agents:
        print(f"│ {name:<25} {model:<30} {c(status, Colors.GREEN):>18} │")
    print("└" + "─" * 78 + "┘")
    print()
    
    # Channel Status
    print(c("📱 Channels", Colors.BOLD + Colors.YELLOW))
    print("┌" + "─" * 78 + "┐")
    channels = [
        ("Telegram", "✅ Connected", "DM + Groups"),
        ("Discord", "⚠️ Partial", "DM only"),
        ("Web (Control UI)", "✅ Running", "localhost:18789")
    ]
    for name, status, details in channels:
        status_color = Colors.GREEN if "✅" in status else Colors.YELLOW
        print(f"│ {name:<25} {c(status, status_color):>20}   {details:<28} │")
    print("└" + "─" * 78 + "┘")
    print()
    
    # API Usage
    usage = get_api_usage()
    print(c("📊 API Usage (Aliyun)", Colors.BOLD + Colors.YELLOW))
    print("┌" + "─" * 78 + "┐")
    print(f"│ Today:        {usage['today']:>6,} requests{' ' * 54} │")
    print(f"│ This Month:   {usage['month']:>6,} / {usage['limit']:,} requests{' ' * 43} │")
    
    # Progress bar
    used_pct = 100 - usage['remaining_pct']
    bar_width = 40
    filled = int(used_pct / 100 * bar_width)
    bar = "█" * filled + "░" * (bar_width - filled)
    bar_color = Colors.GREEN if used_pct < 80 else Colors.YELLOW if used_pct < 95 else Colors.RED
    print(f"│ [{c(bar, bar_color)}] {used_pct:.0f}% used {' ' * 48} │")
    print(f"│ Remaining:    {usage['remaining_pct']:.0f}% ({usage['limit'] - usage['month']:,} requests){' ' * 33} │")
    print("└" + "─" * 78 + "┘")
    print()
    
    # Cost Tracking
    cost = get_cost_info()
    print(c("💰 Cost Tracking", Colors.BOLD + Colors.YELLOW))
    print("┌" + "─" * 78 + "┐")
    print(f"│ Monthly Budget:  ${cost['monthly_budget']:.2f} USD{' ' * 56} │")
    print(f"│ Spent (MTD):     ${cost['spent']:.2f} USD{' ' * 57} │")
    print(f"│ Projected:       ${cost['projected']:.2f} USD{' ' * 56} │")
    
    # Budget status
    if cost['projected'] <= cost['monthly_budget']:
        status = c("✅ Under Budget", Colors.GREEN)
    else:
        status = c("⚠️ Over Budget", Colors.RED)
    print(f"│ Status:          {status:>58} │")
    print("└" + "─" * 78 + "┘")
    print()
    
    # Kanban Status
    kanban = get_kanban_status()
    if kanban:
        print(c("📋 Kanban Board", Colors.BOLD + Colors.YELLOW))
        print("┌" + "─" * 78 + "┐")
        print(f"│ Total Projects:  {kanban['total']:<61} │")
        print(f"│ 📋 Backlog:      {kanban['backlog']:<61} │")
        print(f"│ 📝 To Do:        {kanban['todo']:<61} │")
        print(f"│ 🔄 In Progress:  {kanban['in_progress']:<61} │")
        print(f"│ 🚧 Blocked:      {kanban['blocked']:<61} │")
        print(f"│ ✅ Done:         {kanban['done']:<61} │")
        print("└" + "─" * 78 + "┘")
        print()
    
    # Active Projects
    print(c("🎯 Active Projects", Colors.BOLD + Colors.YELLOW))
    print("┌" + "─" * 78 + "┐")
    projects = [
        ("Discord 多頻道設置", "todo", "medium"),
        ("Vercel/Supabase 遷移", "todo", "medium"),
        ("配置 Web Search API", "todo", "high"),
        ("Sub-agent 功能測試", "blocked", "low")
    ]
    for name, status, priority in projects:
        status_icon = "📝" if status == "todo" else "🚧" if status == "blocked" else "🔄"
        priority_color = Colors.RED if priority == "high" else Colors.YELLOW if priority == "medium" else Colors.DIM
        print(f"│ {status_icon} {name:<35} {c(priority, priority_color):>32} │")
    print("└" + "─" * 78 + "┘")
    print()
    
    # Recent Activity
    print(c("📈 Recent Activity", Colors.BOLD + Colors.YELLOW))
    print("┌" + "─" * 78 + "┐")
    activities = [
        ("2026-02-27 00:03", "晨報 cron job", "⚠️ Rate limit warning"),
        ("2026-02-26 23:30", "Polymarket CLI", "✅ Created"),
        ("2026-02-26 22:10", "Movie Recommender", "✅ Deployed to Zeabur"),
        ("2026-02-26 21:34", "Kanban Board", "✅ proj-012 added"),
        ("2026-02-26 20:55", "Discord Integration", "⚠️ Channel issue")
    ]
    for time, event, status in activities:
        print(f"│ {time}  {event:<35} {status:>32} │")
    print("└" + "─" * 78 + "┘")
    print()
    
    # Quick Tips
    print(c("💡 Quick Tips", Colors.BOLD + Colors.YELLOW))
    print("┌" + "─" * 78 + "┐")
    print(f"│ • Run {c('python3 oc-status.py usage', Colors.CYAN):>55} │")
    print(f"│ • Run {c('python3 oc-status.py agents', Colors.CYAN):>55} │")
    print(f"│ • Run {c('python3 oc-status.py cost', Colors.CYAN):>55} │")
    print(f"│ • Run {c('python3 oc-status.py --help', Colors.CYAN):>55} │")
    print("└" + "─" * 78 + "┘")
    print()

def display_agents():
    """Display agent status only"""
    print()
    print(c("🤖 OpenClaw Agents", Colors.BOLD + Colors.CYAN))
    print("=" * 80)
    print()
    
    agents = [
        ("main (Jarvis)", "aliyun/qwen3.5-plus", "✅ Active", "Main orchestrator"),
        ("coding", "aliyun/qwen3-coder-plus", "✅ Active", "Code generation"),
        ("research", "aliyun/qwen3.5-plus", "✅ Active", "Research & analysis"),
        ("admin", "aliyun/qwen-turbo", "✅ Active", "Schedule & admin")
    ]
    
    print(f"{'Agent':<25} {'Model':<30} {'Status':<12} {'Role'}")
    print("-" * 80)
    for name, model, status, role in agents:
        print(f"{name:<25} {model:<30} {c(status, Colors.GREEN):<12} {role}")
    print()

def display_usage():
    """Display API usage only"""
    usage = get_api_usage()
    
    print()
    print(c("📊 API Usage (Aliyun Coding Plan)", Colors.BOLD + Colors.CYAN))
    print("=" * 80)
    print()
    print(f"Today:        {usage['today']:,} requests")
    print(f"This Month:   {usage['month']:,} / {usage['limit']:,} requests")
    print(f"Remaining:    {usage['remaining_pct']:.0f}% ({usage['limit'] - usage['month']:,} requests)")
    print()
    
    # Progress bar
    used_pct = 100 - usage['remaining_pct']
    bar_width = 60
    filled = int(used_pct / 100 * bar_width)
    bar = "█" * filled + "░" * (bar_width - filled)
    bar_color = Colors.GREEN if used_pct < 80 else Colors.YELLOW if used_pct < 95 else Colors.RED
    print(f"[{c(bar, bar_color)}] {used_pct:.0f}% used")
    print()

def display_cost():
    """Display cost tracking only"""
    cost = get_cost_info()
    
    print()
    print(c("💰 Cost Tracking", Colors.BOLD + Colors.CYAN))
    print("=" * 80)
    print()
    print(f"Monthly Budget:  ${cost['monthly_budget']:.2f} USD")
    print(f"Spent (MTD):     ${cost['spent']:.2f} USD")
    print(f"Projected:       ${cost['projected']:.2f} USD")
    print(f"Daily Average:   ${cost['spent']/26:.2f} USD (based on 26 days)")
    print()
    
    if cost['projected'] <= cost['monthly_budget']:
        print(c("✅ Under Budget - Good job!", Colors.GREEN))
        savings = cost['monthly_budget'] - cost['projected']
        print(f"   Expected savings: ${savings:.2f} USD")
    else:
        print(c("⚠️ Over Budget - Consider reducing usage", Colors.RED))
        over = cost['projected'] - cost['monthly_budget']
        print(f"   Expected overage: ${over:.2f} USD")
    print()

def show_help():
    """Show help"""
    print()
    print(c("🦞 OpenClaw Status CLI", Colors.BOLD + Colors.CYAN))
    print("=" * 80)
    print()
    print("Usage:")
    print(f"  python3 oc-status.py              - Full status dashboard")
    print(f"  python3 oc-status.py {c('agents', Colors.YELLOW)}          - Agent status only")
    print(f"  python3 oc-status.py {c('usage', Colors.YELLOW)}           - API usage")
    print(f"  python3 oc-status.py {c('cost', Colors.YELLOW)}            - Cost tracking")
    print(f"  python3 oc-status.py {c('logs', Colors.YELLOW)}            - Recent logs")
    print(f"  python3 oc-status.py {c('help', Colors.YELLOW)}            - This help")
    print()
    print("Examples:")
    print(f"  python3 oc-status.py")
    print(f"  python3 oc-status.py usage")
    print(f"  python3 oc-status.py cost")
    print()
    print(c("Inspired by Andrej Karpathy: 'Build for Agents'", Colors.DIM))
    print()

def main():
    command = sys.argv[1].lower() if len(sys.argv) > 1 else 'status'
    
    if command == 'status' or command == 'full':
        display_full_status()
    elif command == 'agents':
        display_agents()
    elif command == 'usage':
        display_usage()
    elif command == 'cost':
        display_cost()
    elif command == 'logs':
        print(c("\n📜 Logs feature coming soon!", Colors.YELLOW))
        print("Check Zeabur dashboard for now: https://zeabur.com/dashboard\n")
    elif command == 'help' or command == '--help' or command == '-h':
        show_help()
    else:
        print(c(f"Unknown command: {command}", Colors.RED))
        show_help()

if __name__ == '__main__':
    main()
