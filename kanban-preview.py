#!/usr/bin/env python3
"""
生成 Kanban Board 的可視化預覽
"""

import json
from datetime import datetime

def load_board():
    with open('kanban-board.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_preview():
    data = load_board()
    
    print("=" * 70)
    print(" " * 20 + "📊 Kanban Board 預覽")
    print(" " * 25 + "OpenClaw 項目管理")
    print("=" * 70)
    print()
    
    # 統計
    stats = {}
    for col in ['backlog', 'todo', 'in_progress', 'blocked', 'done']:
        stats[col] = len([p for p in data['projects'] if p['status'] == col])
    
    total = len(data['projects'])
    
    print(f"📊 統計：Backlog({stats['backlog']}) | To Do({stats['todo']}) | " +
          f"In Progress({stats['in_progress']}) | Blocked({stats['blocked']}) | " +
          f"Done({stats['done']}) | 總計：{total}")
    print()
    print("-" * 70)
    print()
    
    # 各列
    columns = [
        ('backlog', '📋 Backlog'),
        ('todo', '📝 To Do'),
        ('in_progress', '🔄 In Progress'),
        ('blocked', '🚧 Blocked'),
        ('done', '✅ Done')
    ]
    
    for col_id, col_name in columns:
        projects = [p for p in data['projects'] if p['status'] == col_id]
        
        print(f"{col_name} ({len(projects)})")
        print("-" * 40)
        
        if not projects:
            print("  (空)")
        else:
            for p in projects:
                priority_emoji = {'low': '🟢', 'medium': '🟡', 'high': '🟠', 'urgent': '🔴'}.get(p['priority'], '⚪')
                print(f"  {priority_emoji} [{p['id']}] {p['title']}")
                if p.get('description'):
                    desc = p['description'][:50] + "..." if len(p['description']) > 50 else p['description']
                    print(f"      {desc}")
                if p.get('tags'):
                    print(f"      標籤：{', '.join(p['tags'])}")
                if p.get('completed'):
                    completed_date = p['completed'][:10]
                    print(f"      完成日期：{completed_date}")
                print()
        
        print()
    
    print("=" * 70)
    print(f"最後更新：{data['meta'].get('updated', '未知')[:19].replace('T', ' ')}")
    print("=" * 70)

if __name__ == "__main__":
    generate_preview()
