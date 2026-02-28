#!/usr/bin/env python3
"""
Kanban Board 後端處理器
處理來自 GUI 的命令並更新 board
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

class KanbanHandler:
    def __init__(self):
        self.board_file = Path("kanban-board.json")
        self.command_file = Path("kanban-command.json")
        self.data = self.load_board()
    
    def load_board(self):
        if self.board_file.exists():
            with open(self.board_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.create_default_board()
    
    def create_default_board(self):
        return {
            "meta": {"created": datetime.now().isoformat(), "updated": datetime.now().isoformat(), "version": "1.0"},
            "columns": {
                "backlog": {"name": "📋 Backlog", "order": 1},
                "todo": {"name": "📝 To Do", "order": 2},
                "in_progress": {"name": "🔄 In Progress", "order": 3},
                "blocked": {"name": "🚧 Blocked", "order": 4},
                "done": {"name": "✅ Done", "order": 5}
            },
            "projects": [],
            "settings": {"defaultPriority": "medium"}
        }
    
    def save_board(self):
        self.data["meta"]["updated"] = datetime.now().isoformat()
        with open(self.board_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def process_command(self, command):
        action = command.get("action")
        
        if action == "add":
            return self.add_project(command)
        elif action == "move":
            return self.move_project(command)
        elif action == "complete":
            return self.complete_project(command)
        elif action == "delete":
            return self.delete_project(command)
        elif action == "update":
            return self.update_project(command)
        elif action == "note":
            return self.add_note(command)
        else:
            return {"success": False, "error": f"未知動作：{action}"}
    
    def add_project(self, command):
        project_id = f"proj-{len(self.data['projects']) + 1:03d}"
        project = {
            "id": project_id,
            "title": command.get("title", "無標題"),
            "description": command.get("description", ""),
            "status": command.get("status", "todo"),
            "priority": command.get("priority", "medium"),
            "created": datetime.now().strftime("%Y-%m-%d"),
            "updated": datetime.now().isoformat(),
            "tags": command.get("tags", []),
            "notes": []
        }
        self.data["projects"].append(project)
        self.save_board()
        return {"success": True, "project_id": project_id, "message": f"已添加項目：{project['title']}"}
    
    def move_project(self, command):
        project_id = command.get("project_id")
        new_status = command.get("status")
        
        for project in self.data["projects"]:
            if project["id"] == project_id:
                old_status = project["status"]
                project["status"] = new_status
                project["updated"] = datetime.now().isoformat()
                if new_status == "done":
                    project["completed"] = datetime.now().isoformat()
                self.save_board()
                return {"success": True, "message": f"已移動項目從 {old_status} 到 {new_status}"}
        
        return {"success": False, "error": f"找不到項目：{project_id}"}
    
    def complete_project(self, command):
        command["status"] = "done"
        return self.move_project(command)
    
    def delete_project(self, command):
        project_id = command.get("project_id")
        
        for i, project in enumerate(self.data["projects"]):
            if project["id"] == project_id:
                deleted = self.data["projects"].pop(i)
                self.save_board()
                return {"success": True, "message": f"已刪除項目：{deleted['title']}"}
        
        return {"success": False, "error": f"找不到項目：{project_id}"}
    
    def update_project(self, command):
        project_id = command.get("project_id")
        
        for project in self.data["projects"]:
            if project["id"] == project_id:
                for key, value in command.items():
                    if key not in ["action", "project_id"] and key in project:
                        project[key] = value
                project["updated"] = datetime.now().isoformat()
                self.save_board()
                return {"success": True, "message": f"已更新項目：{project['title']}"}
        
        return {"success": False, "error": f"找不到項目：{project_id}"}
    
    def add_note(self, command):
        project_id = command.get("project_id")
        note = command.get("note", "")
        
        for project in self.data["projects"]:
            if project["id"] == project_id:
                if "notes" not in project:
                    project["notes"] = []
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                project["notes"].append(f"{timestamp}: {note}")
                project["updated"] = datetime.now().isoformat()
                self.save_board()
                return {"success": True, "message": "已添加備註"}
        
        return {"success": False, "error": f"找不到項目：{project_id}"}
    
    def run(self):
        """監聽命令文件並處理"""
        print("🔄 Kanban 後端處理器已啟動")
        print("📁 監聽文件：kanban-command.json")
        print("🛑 按 Ctrl+C 停止")
        print("")
        
        last_processed = None
        
        while True:
            try:
                if self.command_file.exists():
                    current_modified = self.command_file.stat().st_mtime
                    
                    if last_processed is None or current_modified > last_processed:
                        try:
                            with open(self.command_file, 'r', encoding='utf-8') as f:
                                command = json.load(f)
                            
                            print(f"📥 收到命令：{command.get('action')}")
                            result = self.process_command(command)
                            print(f"{'✅' if result['success'] else '❌'} {result.get('message', result.get('error', ''))}")
                            
                            # 刪除已處理的命令文件
                            self.command_file.unlink()
                            last_processed = current_modified
                            
                        except json.JSONDecodeError:
                            print("⚠️  無效的 JSON 格式")
                        except Exception as e:
                            print(f"❌ 處理錯誤：{e}")
                
                import time
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n👋 停止處理器")
                break
            except Exception as e:
                print(f"❌ 錯誤：{e}")
                import time
                time.sleep(1)


if __name__ == "__main__":
    handler = KanbanHandler()
    handler.run()
