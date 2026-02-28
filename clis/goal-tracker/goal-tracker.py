#!/usr/bin/env python3
"""
Goal Tracker CLI - Track personal goals
Inspired by Karpathy: "Build for Agents"

Usage:
    python3 goal-tracker.py pickleball          # Pickleball goal status
    python3 goal-tracker.py pickleball log      # Log session
    python3 goal-tracker.py pickleball progress # View progress
"""

import json
import sys
from datetime import datetime
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DIM = '\033[2m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def c(text, color):
    return f"{color}{text}{Colors.RESET}"

def display_pickleball_goal():
    """Display pickleball goal status"""
    print()
    print(c("🏓 Pickleball Mastery Goal", Colors.BOLD + Colors.CYAN))
    print("=" * 80)
    print()
    
    # Goal Overview
    print(c("🎯 Goal Overview", Colors.BOLD + Colors.YELLOW))
    print("┌" + "─" * 78 + "┐")
    print(f"│ Target:     {'Become a strong player and certified coach':<58} │")
    print(f"│ Timeline:   {'24 months (2 years)':<58} │")
    print(f"│ Started:    {'2026-02-27':<58} │")
    print(f"│ Priority:   {'High':<58} │")
    print("└" + "─" * 78 + "┘")
    print()
    
    # Current Phase
    print(c("📊 Current Phase: Phase 1 - Foundation Building (Months 1-6)", Colors.BOLD + Colors.GREEN))
    print()
    
    # Progress Bars
    phases = [
        ("Phase 1: Foundation", 1, 6, 0),  # Month 1 of 6
        ("Phase 2: Competitive", 7, 12, 0),
        ("Phase 3: Certification", 13, 18, 0),
        ("Phase 4: Professional", 19, 24, 0)
    ]
    
    print(c("📈 Phase Progress", Colors.BOLD + Colors.YELLOW))
    for name, start, end, progress in phases:
        bar_width = 40
        filled = int(progress / (end - start + 1) * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)
        status = Colors.GREEN if progress > 0 else Colors.DIM
        print(f"  {name:<25} [{c(bar, status)}] {progress}/{end-start+1} months")
    print()
    
    # Skill Ratings
    print(c("🎾 Skill Ratings (Current → Target)", Colors.BOLD + Colors.YELLOW))
    skills = [
        ("Serve", "3.0", "4.5+"),
        ("Return", "3.0", "4.5+"),
        ("Dinks", "3.0", "5.0"),
        ("Drives", "2.5", "4.5"),
        ("Drops", "2.5", "4.5"),
        ("Footwork", "3.0", "4.5")
    ]
    
    print(f"  {'Skill':<15} {'Current':>10} {'Target':>10} {'Gap':>10}")
    print("  " + "─" * 45)
    for skill, current, target in skills:
        gap = "Need work" if float(current.split('+')[0]) < 4.0 else "On track"
        gap_color = Colors.RED if "Need" in gap else Colors.GREEN
        print(f"  {skill:<15} {current:>10} {target:>10} {c(gap, gap_color):>10}")
    print()
    
    # Budget Tracking
    print(c("💰 Budget Tracking (Phase 1)", Colors.BOLD + Colors.YELLOW))
    print("┌" + "─" * 78 + "┐")
    print(f"│ Total Phase 1 Budget:  HKD $17,600{' ' * 50} │")
    print(f"│ Spent (MTD):           HKD $0{' ' * 63} │")
    print(f"│ Remaining:             HKD $17,600{' ' * 52} │")
    print("└" + "─" * 78 + "┘")
    print()
    
    # Upcoming Activities
    print(c("📅 Upcoming Activities", Colors.BOLD + Colors.YELLOW))
    activities = [
        ("2026-02-28 16:00", "Pickleball @ Clubhouse", "Family play"),
        ("2026-03-01 09:00", "Practice Session", "Technical drills"),
        ("2026-03-02", "Buy better paddle", "Equipment upgrade"),
        ("2026-03-07", "Book coaching session", "HKPA certified coach")
    ]
    
    for date, activity, notes in activities:
        print(f"  📌 {date:<18} {activity:<30} ({notes})")
    print()
    
    # Next Milestones
    print(c("🏆 Next Milestones", Colors.BOLD + Colors.YELLOW))
    milestones = [
        ("Month 3", "3+ shots improved", "Technical progress"),
        ("Month 6", "Rating 3.5+, tournament played", "Phase 1 complete"),
        ("Month 12", "Rating 4.0+, coaching started", "Phase 2 complete")
    ]
    
    for timeline, target, desc in milestones:
        print(f"  🎯 {timeline:<10} {target:<35} ({desc})")
    print()
    
    # Quick Stats
    print(c("📊 Quick Stats", Colors.BOLD + Colors.YELLOW))
    print("┌" + "─" * 78 + "┐")
    print(f"│ Days Since Start:        0 days{' ' * 58} │")
    print(f"│ Sessions Completed:      0{' ' * 66} │")
    print(f"│ Hours Played:            0 hours{' ' * 57} │")
    print(f"│ Money Invested:          HKD $0{' ' * 59} │")
    print(f"│ Coaching Hours:          0 hours{' ' * 57} │")
    print("└" + "─" * 78 + "┘")
    print()
    
    # Commands
    print(c("💡 Quick Commands", Colors.BOLD + Colors.YELLOW))
    print("┌" + "─" * 78 + "┐")
    print(f"│ goal-tracker.py pickleball log       - Log a playing session{' ' * 43} │")
    print(f"│ goal-tracker.py pickleball progress  - Detailed progress report{' ' * 44} │")
    print(f"│ goal-tracker.py pickleball budget    - Budget tracking{' ' * 56} │")
    print(f"│ goal-tracker.py pickleball schedule  - Training schedule{' ' * 54} │")
    print("└" + "─" * 78 + "┘")
    print()

def log_session():
    """Log a pickleball session"""
    print()
    print(c("🏓 Log Pickleball Session", Colors.BOLD + Colors.CYAN))
    print("=" * 80)
    print()
    print("Session logging coming soon!")
    print("For now, sessions are tracked in memory files.")
    print()

def show_help():
    """Show help"""
    print()
    print(c("🎯 Goal Tracker CLI", Colors.BOLD + Colors.CYAN))
    print("=" * 80)
    print()
    print("Usage:")
    print(f"  python3 goal-tracker.py {c('<goal>', Colors.YELLOW)}              - Goal status")
    print(f"  python3 goal-tracker.py {c('<goal> log', Colors.YELLOW)}          - Log activity")
    print(f"  python3 goal-tracker.py {c('<goal> progress', Colors.YELLOW)}     - Progress report")
    print(f"  python3 goal-tracker.py {c('<goal> budget', Colors.YELLOW)}       - Budget tracking")
    print(f"  python3 goal-tracker.py {c('help', Colors.YELLOW)}                - This help")
    print()
    print("Available Goals:")
    print(f"  {c('pickleball', Colors.YELLOW)} - Pickleball Mastery Goal")
    print()
    print(c("Inspired by Andrej Karpathy: 'Build for Agents'", Colors.DIM))
    print()

def main():
    if len(sys.argv) < 2:
        display_pickleball_goal()
        return
    
    goal = sys.argv[1].lower()
    command = sys.argv[2].lower() if len(sys.argv) > 2 else 'status'
    
    if goal == 'pickleball':
        if command == 'log':
            log_session()
        elif command == 'progress':
            display_pickleball_goal()
        elif command == 'budget':
            print(c("\n💰 Budget tracking coming soon!\n", Colors.YELLOW))
        elif command == 'schedule':
            print(c("\n📅 Schedule view coming soon!\n", Colors.YELLOW))
        else:
            display_pickleball_goal()
    elif goal == 'help' or goal == '--help':
        show_help()
    else:
        print(c(f"Unknown goal: {goal}", Colors.RED))
        show_help()

if __name__ == '__main__':
    main()
