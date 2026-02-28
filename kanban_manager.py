#!/usr/bin/env python3
"""
Kanban Board Manager
管理項目任務的命令行工具
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

class KanbanBoard:
    def __init__(self, board_file="kanban-board.json"):
        self.board_file = Path(board_file)
        self.data = self.load_board()
    
    def load_board(self):
        """加載 Kanban board"""
        if self.board_file.exists():
            with open(self.board_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self.create_default_board()
    
    def create_default_board(self):
        """創建默認 board"""
        return {
            "meta": {
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat(),
                "version": "1.0"
            },
            "columns": {
                "backlog": {"name": "📋 Backlog", "description": "未來可能做的項目", "order": 1},
                "todo": {"name": "📝 To Do", "description": "計劃要做的項目", "order": 2},
                "in_progress": {"name": "🔄 In Progress", "description": "進行中的項目", "order": 3},
                "blocked": {"name": "🚧 Blocked", "description": "被阻擋的項目", "order": 4},
                "done": {"name": "✅ Done", "description": "已完成的項目", "order": 5}
            },
            "projects": [],
            "settings": {
                "archiveDoneAfterDays": 30,
                "defaultPriority": "medium",
                "priorities": ["low", "medium", "high", "urgent"]
            }
        }
    
    def save_board(self):
        """保存 board"""
        self.data["meta"]["updated"] = datetime.now().isoformat()
        with open(self.board_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_project(self, title, description="", status="todo", priority="medium", tags=None):
        """添加新項目"""
        project_id = f"proj-{len(self.data['projects']) + 1:03d}"
        project = {
            "id": project_id,
            "title": title,
            "description": description,
            "status": status,
            "priority": priority,
            "created": datetime.now().strftime("%Y-%m-%d"),
            "updated": datetime.now().isoformat(),
            "tags": tags or [],
            "notes": []
        }
        self.data["projects"].append(project)
        self.save_board()
        return project
    
    def move_project(self, project_id, new_status):
        """移動項目到不同狀態"""
        for project in self.data["projects"]:
            if project["id"] == project_id:
                old_status = project["status"]
                project["status"] = new_status
                project["updated"] = datetime.now().isoformat()
                
                if new_status == "done":
                    project["completed"] = datetime.now().isoformat()
                
                self.save_board()
                return f"✅ 移動項目 {project_id} 從 {old_status} 到 {new_status}"
        
        return f"❌ 找不到項目 {project_id}"
    
    def complete_project(self, project_id):
        """完成項目"""
        return self.move_project(project_id, "done")
    
    def list_projects(self, status=None):
        """列出項目"""
        projects = self.data["projects"]
        
        if status:
            projects = [p for p in projects if p["status"] == status]
        
        if not projects:
            return "暫無項目"
        
        result = []
        for p in projects:
            priority_emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "urgent": "🔴"}.get(p["priority"], "⚪")
            result.append(f"{priority_emoji} [{p['id']}] {p['title']}")
            if p.get("tags"):
                result.append(f"   標籤：{', '.join(p['tags'])}")
            if p.get("description"):
                result.append(f"   描述：{p['description']}")
            result.append("")
        
        return "\n".join(result)
    
    def show_board(self):
        """顯示完整 board"""
        result = []
        result.append("=" * 60)
        result.append("📊 項目 Kanban Board")
        result.append("=" * 60)
        result.append("")
        
        # 按狀態分組
        columns = ["backlog", "todo", "in_progress", "blocked", "done"]
        
        for col_id in columns:
            col = self.data["columns"].get(col_id, {})
            col_name = col.get("name", col_id)
            projects = [p for p in self.data["projects"] if p["status"] == col_id]
            
            result.append(f"{col_name} ({len(projects)})")
            result.append("-" * 40)
            
            if projects:
                for p in projects:
                    priority_emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "urgent": "🔴"}.get(p["priority"], "⚪")
                    result.append(f"  {priority_emoji} [{p['id']}] {p['title']}")
                    if p.get("tags"):
                        result.append(f"      標籤：{', '.join(p['tags'])}")
            else:
                result.append("  (空)")
            
            result.append("")
        
        result.append("=" * 60)
        return "\n".join(result)
    
    def get_project(self, project_id):
        """獲取項目詳情"""
        for project in self.data["projects"]:
            if project["id"] == project_id:
                return project
        return None
    
    def update_project(self, project_id, **kwargs):
        """更新項目"""
        project = self.get_project(project_id)
        if not project:
            return f"❌ 找不到項目 {project_id}"
        
        for key, value in kwargs.items():
            if key in project:
                project[key] = value
        
        project["updated"] = datetime.now().isoformat()
        self.save_board()
        return f"✅ 已更新項目 {project_id}"
    
    def add_note(self, project_id, note):
        """添加備註"""
        project = self.get_project(project_id)
        if not project:
            return f"❌ 找不到項目 {project_id}"
        
        if "notes" not in project:
            project["notes"] = []
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        project["notes"].append(f"{timestamp}: {note}")
        project["updated"] = datetime.now().isoformat()
        self.save_board()
        
        return f"✅ 已添加備註到項目 {project_id}"
    
    def delete_project(self, project_id):
        """刪除項目"""
        for i, project in enumerate(self.data["projects"]):
            if project["id"] == project_id:
                deleted = self.data["projects"].pop(i)
                self.save_board()
                return f"✅ 已刪除項目 {project_id}: {deleted['title']}"
        
        return f"❌ 找不到項目 {project_id}"
    
    def search_projects(self, keyword):
        """搜索項目"""
        results = []
        keyword_lower = keyword.lower()
        
        for project in self.data["projects"]:
            if (keyword_lower in project["title"].lower() or 
                keyword_lower in project.get("description", "").lower() or
                any(keyword_lower in tag.lower() for tag in project.get("tags", []))):
                results.append(project)
        
        if not results:
            return f"未找到匹配 '{keyword}' 的項目"
        
        result = [f"🔍 搜索結果 '{keyword}':", ""]
        for p in results:
            priority_emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "urgent": "🔴"}.get(p["priority"], "⚪")
            result.append(f"{priority_emoji} [{p['id']}] {p['title']} (狀態：{p['status']})")
        
        return "\n".join(result)


def print_help():
    """打印幫助信息"""
    help_text = """
📋 Kanban Board 使用指南

用法：python3 kanban_manager.py <命令> [參數]

命令:
  show                          顯示完整 board
  list [status]                 列出項目 (可選：backlog/todo/in_progress/blocked/done)
  add <標題> [描述]             添加新項目
  move <ID> <狀態>              移動項目 (狀態：backlog/todo/in_progress/blocked/done)
  complete <ID>                 完成項目
  update <ID> <字段>=<值>       更新項目
  note <ID> <備註>              添加備註
  search <關鍵詞>               搜索項目
  delete <ID>                   刪除項目
  help                          顯示此幫助信息

示例:
  python3 kanban_manager.py show
  python3 kanban_manager.py add "創建網站" "設計並開發新網站" high
  python3 kanban_manager.py move proj-001 in_progress
  python3 kanban_manager.py complete proj-001
  python3 kanban_manager.py note proj-001 "已完成初稿"
  python3 kanban_manager.py search 網站

狀態說明:
  📋 backlog    - 未來可能做的項目
  📝 todo       - 計劃要做的項目
  🔄 in_progress - 進行中的項目
  🚧 blocked    - 被阻擋的項目
  ✅ done       - 已完成的項目

優先級:
  🟢 low    - 低優先級
  🟡 medium - 中優先級 (默認)
  🟠 high   - 高優先級
  🔴 urgent - 緊急
"""
    print(help_text)


def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
    
    board = KanbanBoard()
    command = sys.argv[1].lower()
    
    if command == "show":
        print(board.show_board())
    
    elif command == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        print(board.list_projects(status))
    
    elif command == "add":
        if len(sys.argv) < 3:
            print("❌ 請提供項目標題")
            sys.exit(1)
        
        title = sys.argv[2]
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        priority = sys.argv[4] if len(sys.argv) > 4 else "medium"
        
        project = board.add_project(title, description, priority=priority)
        print(f"✅ 已添加項目:")
        print(f"   ID: {project['id']}")
        print(f"   標題：{project['title']}")
        print(f"   狀態：{project['status']}")
        print(f"   優先級：{project['priority']}")
    
    elif command == "move":
        if len(sys.argv) < 4:
            print("❌ 用法：move <項目 ID> <新狀態>")
            sys.exit(1)
        
        project_id = sys.argv[2]
        new_status = sys.argv[3]
        print(board.move_project(project_id, new_status))
    
    elif command == "complete":
        if len(sys.argv) < 3:
            print("❌ 請提供項目 ID")
            sys.exit(1)
        
        print(board.complete_project(sys.argv[2]))
    
    elif command == "update":
        if len(sys.argv) < 4:
            print("❌ 用法：update <項目 ID> <字段>=<值>")
            sys.exit(1)
        
        project_id = sys.argv[2]
        updates = {}
        
        for arg in sys.argv[3:]:
            if "=" in arg:
                key, value = arg.split("=", 1)
                updates[key] = value
        
        print(board.update_project(project_id, **updates))
    
    elif command == "note":
        if len(sys.argv) < 4:
            print("❌ 用法：note <項目 ID> <備註內容>")
            sys.exit(1)
        
        project_id = sys.argv[2]
        note = " ".join(sys.argv[3:])
        print(board.add_note(project_id, note))
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("❌ 請提供搜索關鍵詞")
            sys.exit(1)
        
        print(board.search_projects(" ".join(sys.argv[2:])))
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("❌ 請提供項目 ID")
            sys.exit(1)
        
        print(board.delete_project(sys.argv[2]))
    
    elif command == "help":
        print_help()
    
    else:
        print(f"❌ 未知命令：{command}")
        print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
