# 🛠️ HOW TO SETUP VS CODE TASKS

## Step 1 — Global "Create New Full Project" task (do once)
1. Press Ctrl+Shift+P → type "Open User Tasks" → Enter
2. Copy contents of user_tasks.json into that file
3. Change YOUR_PATH to where create_project.py lives
4. Run: Ctrl+Shift+P → Run Task → 🚀 Create New Full Project

## Step 2 — Workspace tasks (optional)
1. Open your .code-workspace file
2. Paste blocks from workspace_tasks.json into it
3. Change the path in the Create task

## Step 3 — Project tasks (already done!)
.vscode/tasks.json is auto-created — works when folder opened directly

## Files in scripts/
| File                  | Purpose                                      |
|-----------------------|----------------------------------------------|
| create_project.py     | The project generator script                 |
| user_tasks.json       | Paste into User Tasks — works globally       |
| workspace_tasks.json  | Paste into .code-workspace — workspace only  |
| project_tasks.json    | Reference copy of .vscode/tasks.json         |
| HOW_TO_SETUP.md       | This file                                    |
