#!/bin/bash
#
# Auto-Sync Git Commits to Kanban Board
# Automatically adds commit links to kanban-board.json tasks
#
# Usage: 
#   Add to .git/hooks/post-commit or run manually after commits
#
# Commit Message Format:
#   feat: Add feature [proj-XXX]
#   fix: Bug fix [proj-035]
#   docs: Update docs [proj-001]
#

set -e

# Configuration
KANBAN_FILE="/home/node/.openclaw/workspace/kanban-zeabur/kanban-board.json"
GIT_REPO_URL="https://github.com/raycoderhk/2048-game"
WORKSPACE="/home/node/.openclaw/workspace"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get the latest commit info
get_latest_commit() {
    COMMIT_HASH=$(git rev-parse --short HEAD)
    COMMIT_MSG=$(git log -1 --pretty=%B | head -1)
    COMMIT_DATE=$(git log -1 --pretty=%ci | cut -d' ' -f1)
    COMMIT_URL="${GIT_REPO_URL}/commit/${COMMIT_HASH}"
    
    log_info "Latest commit: ${COMMIT_HASH}"
    log_info "Message: ${COMMIT_MSG}"
    log_info "Date: ${COMMIT_DATE}"
}

# Extract task ID from commit message (e.g., [proj-035])
extract_task_id() {
    TASK_ID=$(echo "$COMMIT_MSG" | grep -oP '\[proj-\w+\]' | tr -d '[]' | head -1)
    
    if [ -z "$TASK_ID" ]; then
        log_warning "No task ID found in commit message. Format: [proj-XXX]"
        return 1
    fi
    
    log_info "Task ID: ${TASK_ID}"
    return 0
}

# Update kanban-board.json with commit info
update_kanban() {
    log_info "Updating kanban-board.json..."
    
    # Check if kanban file exists
    if [ ! -f "$KANBAN_FILE" ]; then
        log_error "Kanban file not found: $KANBAN_FILE"
        return 1
    fi
    
    # Create Python script to update JSON
    python3 << PYTHON_SCRIPT
import json
import sys
from datetime import datetime

kanban_file = "$KANBAN_FILE"
task_id = "$TASK_ID"
commit_hash = "$COMMIT_HASH"
commit_msg = """$COMMIT_MSG"""
commit_date = "$COMMIT_DATE"
commit_url = "$COMMIT_URL"

try:
    # Load kanban board
    with open(kanban_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find the task
    task_found = False
    for project in data['projects']:
        if project['id'] == task_id:
            task_found = True
            
            # Initialize commits array if not exists
            if 'commits' not in project:
                project['commits'] = []
            
            # Check if commit already exists
            existing_hashes = [c.get('hash') for c in project['commits']]
            if commit_hash in existing_hashes:
                print(f"⚠️  Commit ${commit_hash} already exists in ${task_id}")
                sys.exit(0)
            
            # Add new commit
            commit_entry = {
                "hash": commit_hash,
                "message": commit_msg,
                "url": commit_url,
                "date": commit_date,
                "added_at": datetime.now().isoformat()
            }
            project['commits'].append(commit_entry)
            
            # Update task status to in_progress if it was todo/backlog
            if project.get('status') in ['todo', 'backlog']:
                project['status'] = 'in_progress'
                print(f"📊 Updated status: todo → in_progress")
            
            # Update timestamp
            project['updated'] = datetime.now().isoformat()
            
            # Add note about commit
            note = f"🔗 Commit: [{commit_hash}]({commit_url}) - {commit_msg[:50]}..."
            if 'notes' not in project:
                project['notes'] = []
            
            # Check if note already exists
            if not any(commit_hash in n for n in project['notes']):
                project['notes'].append(note)
            
            print(f"✅ Added commit ${commit_hash} to ${task_id}")
            break
    
    if not task_found:
        print(f"❌ Task ${task_id} not found in kanban-board.json")
        sys.exit(1)
    
    # Update meta timestamp
    data['meta']['updated'] = datetime.now().isoformat()
    
    # Save back to file
    with open(kanban_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved kanban-board.json")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    sys.exit(1)
PYTHON_SCRIPT
    
    return $?
}

# Commit and push the kanban update
commit_kanban_update() {
    log_info "Committing kanban update..."
    
    cd "$WORKSPACE"
    
    # Check if there are changes
    if ! git diff --quiet "$KANBAN_FILE"; then
        git add "$KANBAN_FILE"
        git commit -m "chore: Auto-add commit ${COMMIT_HASH} to ${TASK_ID} [skip-ci]"
        log_success "Committed kanban update"
        
        # Push to GitHub
        log_info "Pushing to GitHub..."
        git push origin main 2>&1 | head -5
        log_success "Pushed to GitHub"
    else
        log_warning "No changes to commit"
    fi
}

# Main execution
main() {
    echo "========================================"
    echo "  🔄 Auto-Sync Commits to Kanban"
    echo "========================================"
    echo ""
    
    # Get commit info
    get_latest_commit
    
    # Extract task ID
    if ! extract_task_id; then
        log_warning "Skipping auto-sync (no task ID in commit message)"
        exit 0
    fi
    
    # Update kanban
    if ! update_kanban; then
        log_error "Failed to update kanban"
        exit 1
    fi
    
    # Commit and push
    commit_kanban_update
    
    echo ""
    echo "========================================"
    log_success "✅ Auto-sync complete!"
    echo "========================================"
}

# Run main function
main "$@"
