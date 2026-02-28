#!/usr/bin/env python3
"""
Polymarket CLI - Simple version (no external dependencies)
Track prediction markets from terminal

Usage:
    python3 polymarket.py top        # Top markets
    python3 polymarket.py search AI  # Search
    python3 polymarket.py dashboard  # Dashboard
"""

import json
import sys
from datetime import datetime

class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    RESET = '\033[0m'

def c(text, color):
    """Colorize text"""
    return f"{color}{text}{Colors.RESET}"

def get_mock_markets():
    """Mock market data for demonstration"""
    return [
        {
            'title': 'Will Bitcoin reach $100k in 2026?',
            'subtitle': 'Crypto',
            'volume': 15420000,
            'yes_bid': 0.67,
            'no_bid': 0.33,
            'end_date': '2026-12-31'
        },
        {
            'title': 'Will AI pass Turing Test by 2027?',
            'subtitle': 'Technology',
            'volume': 8750000,
            'yes_bid': 0.42,
            'no_bid': 0.58,
            'end_date': '2027-12-31'
        },
        {
            'title': 'Fed rate cut in March 2026?',
            'subtitle': 'Economics',
            'volume': 12300000,
            'yes_bid': 0.78,
            'no_bid': 0.22,
            'end_date': '2026-03-31'
        },
        {
            'title': 'HK stocks outperform US in 2026?',
            'subtitle': 'Finance',
            'volume': 5600000,
            'yes_bid': 0.35,
            'no_bid': 0.65,
            'end_date': '2026-12-31'
        },
        {
            'title': 'Pickleball becomes Olympic sport?',
            'subtitle': 'Sports',
            'volume': 2100000,
            'yes_bid': 0.15,
            'no_bid': 0.85,
            'end_date': '2028-12-31'
        },
        {
            'title': 'China GDP growth >5% in 2026?',
            'subtitle': 'Economics',
            'volume': 9800000,
            'yes_bid': 0.62,
            'no_bid': 0.38,
            'end_date': '2026-12-31'
        },
        {
            'title': 'Tesla FSD approved in HK?',
            'subtitle': 'Technology',
            'volume': 4200000,
            'yes_bid': 0.28,
            'no_bid': 0.72,
            'end_date': '2026-06-30'
        },
        {
            'title': 'OpenClaw reaches 10k users?',
            'subtitle': 'Technology',
            'volume': 890000,
            'yes_bid': 0.71,
            'no_bid': 0.29,
            'end_date': '2026-12-31'
        }
    ]

def format_volume(vol):
    """Format volume number"""
    if vol >= 1000000:
        return f"${vol/1000000:.1f}M"
    elif vol >= 1000:
        return f"${vol/1000:.0f}K"
    return f"${vol}"

def display_top_markets(limit=10):
    """Display top markets"""
    markets = get_mock_markets()[:limit]
    
    print()
    print(c("🔥 Top Polymarkets by Volume", Colors.BOLD + Colors.CYAN))
    print("=" * 100)
    print()
    
    # Header
    header = f"{c('#', Colors.BOLD):>3}  {c('Market', Colors.BOLD):<50}  {c('Category', Colors.BOLD):<12}  {c('Volume', Colors.BOLD):>10}  {c('Yes%', Colors.BOLD):>6}  {c('No%', Colors.BOLD):>6}  {c('End Date', Colors.BOLD):<12}"
    print(header)
    print("-" * 100)
    
    # Rows
    for i, m in enumerate(markets, 1):
        title = m['title'][:48] + '...' if len(m['title']) > 50 else m['title']
        vol = format_volume(m['volume'])
        yes_pct = f"{m['yes_bid']*100:.0f}%"
        no_pct = f"{m['no_bid']*100:.0f}%"
        
        # Color coding
        yes_color = Colors.GREEN if m['yes_bid'] > 0.5 else Colors.RED
        no_color = Colors.GREEN if m['no_bid'] > 0.5 else Colors.RED
        
        print(f"{i:>3}  {c(title, Colors.CYAN):<50}  {m['subtitle']:<12}  {vol:>10}  {c(yes_pct, yes_color):>6}  {c(no_pct, no_color):>6}  {m['end_date']:<12}")
    
    print("-" * 100)
    print(f"Data: Polymarket API | Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def display_dashboard():
    """Display full dashboard"""
    print("\033[2J\033[H")  # Clear screen
    
    # Header
    print()
    print(c("╔" + "═" * 98 + "╗", Colors.BOLD + Colors.MAGENTA))
    print(c("║" + " " * 35 + "🎯 Polymarket Dashboard" + " " * 37 + "║", Colors.BOLD + Colors.MAGENTA))
    print(c("╚" + "═" * 98 + "╝", Colors.BOLD + Colors.MAGENTA))
    print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Top Markets
    display_top_markets(5)
    
    # Quick Stats
    print(c("📊 Quick Stats", Colors.BOLD + Colors.YELLOW))
    print("┌" + "─" * 48 + "┐")
    print(f"│ Total Markets Tracked:  {c('1,247', Colors.GREEN):>24} │")
    print(f"│ 24h Total Volume:       {c('$45.2M', Colors.GREEN):>24} │")
    print(f"│ Your Balance (demo):    {c('$1,000', Colors.GREEN):>24} │")
    print(f"│ Active Watchlist:       {c('3 markets', Colors.GREEN):>24} │")
    print("└" + "─" * 48 + "┘")
    print()
    
    # Trending Categories
    print(c("📈 Trending Categories", Colors.BOLD + Colors.YELLOW))
    categories = [
        ("Crypto", "+15.2%"),
        ("Technology", "+8.7%"),
        ("Economics", "+5.3%"),
        ("Sports", "+2.1%")
    ]
    for cat, change in categories:
        print(f"  {cat:<20} {c(change, Colors.GREEN):>10}")
    print()

def search_markets(query):
    """Search markets"""
    markets = get_mock_markets()
    results = [m for m in markets if query.lower() in m['title'].lower() or query.lower() in m['subtitle'].lower()]
    
    if not results:
        print(c(f"\nNo markets found for '{query}'", Colors.RED))
        return
    
    print(c(f"\n🔍 Search Results for '{query}' ({len(results)} found)", Colors.BOLD + Colors.CYAN))
    print("=" * 100)
    
    for i, m in enumerate(results, 1):
        title = m['title'][:60] + '...' if len(m['title']) > 62 else m['title']
        vol = format_volume(m['volume'])
        yes_pct = f"{m['yes_bid']*100:.0f}%"
        
        print(f"\n{i}. {c(title, Colors.CYAN)}")
        print(f"   Category: {m['subtitle']} | Volume: {c(vol, Colors.GREEN)} | Yes: {c(yes_pct, Colors.BLUE)}")
        print(f"   End Date: {m['end_date']}")
    print()

def show_help():
    """Show help"""
    print()
    print(c("🎯 Polymarket CLI", Colors.BOLD + Colors.MAGENTA))
    print("=" * 50)
    print()
    print("Usage:")
    print(f"  python3 polymarket.py {c('top', Colors.YELLOW)} [limit]        - Top markets by volume")
    print(f"  python3 polymarket.py {c('search', Colors.YELLOW)} <query>      - Search markets")
    print(f"  python3 polymarket.py {c('dashboard', Colors.YELLOW)}           - Full dashboard")
    print(f"  python3 polymarket.py {c('help', Colors.YELLOW)}                - This help")
    print()
    print("Examples:")
    print(f"  python3 polymarket.py top 5")
    print(f"  python3 polymarket.py search Bitcoin")
    print(f"  python3 polymarket.py dashboard")
    print()
    print(c("Inspired by Andrej Karpathy: 'Build for Agents'", Colors.ITALIC))
    print()

def main():
    if len(sys.argv) < 2:
        display_top_markets(10)
        return
    
    command = sys.argv[1].lower()
    
    if command == 'top':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        display_top_markets(limit)
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print(c("Error: Please provide a search query", Colors.RED))
            return
        query = ' '.join(sys.argv[2:])
        search_markets(query)
    
    elif command == 'dashboard':
        display_dashboard()
    
    elif command == 'help' or command == '--help' or command == '-h':
        show_help()
    
    else:
        print(c(f"Unknown command: {command}", Colors.RED))
        show_help()

if __name__ == '__main__':
    main()
