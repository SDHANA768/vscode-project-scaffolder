# =============================================================================
#  VS Code Project Scaffolder
#  GitHub: https://github.com/SDHANA768/vscode-project-scaffolder.git
# -----------------------------------------------------------------------------
#  Created by  : Claude (Anthropic AI) — https://claude.ai
#  Directed by : Dhanasekar
#  License     : MIT
# -----------------------------------------------------------------------------
#  This entire script — every line of code, structure, and logic —
#  was written by Claude AI through a conversation with Dhanasekar.
#  Dhanasekar directed every feature, tested every version, and shaped
#  this tool into what it is. Claude wrote the code.
# =============================================================================
#  create_project.py
#  Project Scaffolding Script
# -----------------------------------------------------------------------------
#  What this script does:
#    - Creates a full professional folder structure for web projects
#    - Supports 4 backend languages: Python, Node.js, Go, PHP
#    - Auto-creates Python venv (Python projects only)
#    - Creates install/uninstall wrappers for ALL languages:
#        Python  → pip_install.bat / pip_uninstall.bat
#        Node.js → npm_install.bat / npm_uninstall.bat
#        Go      → go_get.bat     / go_remove.bat
#        PHP     → composer_install.bat / composer_uninstall.bat
#    - All wrappers auto-update their dependency file after install/uninstall
#    - Generates .vscode/settings.json and .vscode/tasks.json
#    - Saves a commented copy of this script inside scripts/ folder
#    - Generates a full README.md with documentation
#
#  How to run:
#    python create_project.py <project_name> <output_path>
#    Example: python create_project.py my_app "D:\Projects"
#
#  Or via VS Code Task:
#    Ctrl+Shift+P → Run Task → Create New Full Project
# =============================================================================

import os       # For folder/file operations
import sys      # For reading command line arguments
import shutil   # For copying this script into the project
import subprocess  # For running venv creation command


# =============================================================================
#  SECTION 1 — LANGUAGE OPTIONS
#  Add new languages here by adding a new key-value pair
#  Then add a new section in get_language_files() below
# =============================================================================

LANGUAGES = {
    "1": "Python (FastAPI)",
    "2": "Node.js (Express)",
    "3": "Go",
    "4": "PHP",
}


# =============================================================================
#  SECTION 2 — LANGUAGE FILE & FOLDER TEMPLATES
#  Each language has its own folder structure and starter files
#  Common folders/files are shared across all languages
# =============================================================================

def get_language_files(lang, project_name):
    """
    Returns the folder list, file dict, run hint, and lang_type
    based on the selected language number.

    To add a new language:
      1. Add it to LANGUAGES dict above
      2. Add an elif block here with its folders, files, run_hint
    """

    # ── Folders shared by ALL languages ──────────────────────────────────────
    # These are the frontend, data, docs folders that stay the same
    # regardless of backend language choice
    common_folders = [
        "frontend/public",
        "frontend/src/core",
        "frontend/src/nodes",
        "frontend/src/components",
        "frontend/src/store",
        "frontend/src/styles",
        "frontend/src/utils",
        "data/graphs",
        "data/presets",
        "docs",
        ".vscode",
        "scripts",           # Stores a copy of this generator script
    ]

    # ── Shared VS Code tasks.json ─────────────────────────────────────────────
    # These tasks are created inside .vscode/tasks.json for every project
    # They use CMD shell instead of PowerShell to avoid path issues
    #
    # To add a new task: copy one task block below and change label/command
    # To change shell from CMD to PowerShell: remove the "shell" options block
    shared_tasks = (
        '{\n'
        '    "version": "2.0.0",\n'
        '    "tasks": [\n'
        '        {\n'
        '            "label": "\U0001f4c2 CD to Current File Folder",\n'
        '            "type": "shell",\n'
        '            "command": "cd /d \\"${fileDirname}\\" && cmd /k",\n'
        '            "options": {\n'
        '                "cwd": "${fileDirname}",\n'
        '                "shell": {\n'
        '                    "executable": "cmd.exe",\n'
        '                    "args": ["/d", "/c"]\n'
        '                }\n'
        '            },\n'
        '            "problemMatcher": []\n'
        '        },\n'
        '        {\n'
        '            "label": "\U0001f3e0 CD to Workspace Root",\n'
        '            "type": "shell",\n'
        '            "command": "cd /d \\"${workspaceFolder}\\" && cmd /k",\n'
        '            "options": {\n'
        '                "cwd": "${workspaceFolder}",\n'
        '                "shell": {\n'
        '                    "executable": "cmd.exe",\n'
        '                    "args": ["/d", "/c"]\n'
        '                }\n'
        '            },\n'
        '            "problemMatcher": []\n'
        '        }\n'
        '    ]\n'
        '}\n'
    )

    # ── VS Code settings.json shared base ────────────────────────────────────
    # Created in .vscode/settings.json for every project
    # Option 1 (default): terminal opens at workspace root
    # Option 2 (toggle): terminal auto-follows current file folder
    #
    # To enable Auto CD: comment out Option 1, uncomment Option 2
    shared_settings_base = (
        '{\n'
        '    // ── Terminal CD Mode ──────────────────────────────────────────\n'
        '    // Option 1: Terminal always opens at project ROOT (default)\n'
        '    "terminal.integrated.cwd": "${workspaceFolder}",\n\n'
        '    // Option 2: Terminal auto-follows the CURRENT FILE folder\n'
        '    // To enable: comment Option 1 above, uncomment line below\n'
        '    // "terminal.integrated.cwd": "${fileDirname}",\n'
        '    // ─────────────────────────────────────────────────────────────\n\n'
        '    // Use CMD as default terminal instead of PowerShell\n'
        '    "terminal.integrated.defaultProfile.windows": "Command Prompt",\n\n'
        '    "editor.formatOnSave": true\n'
        '}\n'
    )

    # ── README content ────────────────────────────────────────────────────────
    # Full documentation generated into README.md for every project
    # To update README content: edit the string below
    # Use {project_name} to insert the project name dynamically
    def build_readme(lang_name, lang_badge, backend_structure,
                      install_cmd, uninstall_cmd, install_note,
                      run_cmd, port, dep_file, wrapper_name):
        """
        Builds a language-specific README.
        Called once per language with that language's specific details.

        Args:
            lang_name        : e.g. "Python (FastAPI)"
            lang_badge       : markdown badge string
            backend_structure: multiline string of backend folder tree
            install_cmd      : e.g. "pip_install.bat requests"
            uninstall_cmd    : e.g. "pip_uninstall.bat requests"
            install_note     : extra note about install (e.g. venv activation)
            run_cmd          : e.g. "uvicorn app.main:app --reload"
            port             : e.g. "8000"
            dep_file         : e.g. "requirements.txt"
            wrapper_name     : e.g. "pip_install.bat"
        """
        return f"""# {project_name}

{lang_badge}
&nbsp; ![Generated](https://img.shields.io/badge/Generated_by-create__project.py-blue?style=flat)

> **{lang_name}** backend project — Generated by `create_project.py`

---

## \U0001f4c1 Project Structure

```
{project_name}/
\u251c\u2500\u2500 backend/                        # {lang_name} backend server
{backend_structure}
\u251c\u2500\u2500 frontend/                       # Web UI
\u2502   \u251c\u2500\u2500 public/index.html           # HTML entry
\u2502   \u2514\u2500\u2500 src/
\u2502       \u251c\u2500\u2500 core/NodeGraph.js       # Node graph manager
\u2502       \u251c\u2500\u2500 nodes/                  # Node UI components
\u2502       \u251c\u2500\u2500 components/             # UI components
\u2502       \u251c\u2500\u2500 store/                  # State management
\u2502       \u251c\u2500\u2500 styles/                 # CSS
\u2502       \u2514\u2500\u2500 utils/                  # API & WebSocket clients
\u2502
\u251c\u2500\u2500 data/                           # Saved graphs & presets
\u251c\u2500\u2500 docs/                           # Documentation
\u251c\u2500\u2500 scripts/                        # VS Code task files & generator script
\u251c\u2500\u2500 .vscode/
\u2502   \u251c\u2500\u2500 settings.json               # Terminal mode, formatter
\u2502   \u2514\u2500\u2500 tasks.json                  # CD tasks
\u251c\u2500\u2500 {wrapper_name}           # install + auto-update {dep_file}
\u251c\u2500\u2500 docker-compose.yml
\u2514\u2500\u2500 README.md
```

---

## \U0001f680 Getting Started

### 1. Run the Backend
```cmd
{run_cmd}
```
Server: `http://localhost:{port}`

### 2. Run the Frontend
```cmd
cd frontend
npm install
npm run dev
```

---

## \U0001f4e6 Installing & Uninstalling Packages

Always use the wrapper scripts — they install/remove AND auto-update `{dep_file}`.

```cmd
{install_cmd}
{uninstall_cmd}
```
{install_note}

> \u26a0\ufe0f Never use plain install commands — they won\'t update `{dep_file}`!

---

## \u2699\ufe0f VS Code Tasks

`Ctrl+Shift+P` \u2192 **Run Task**

| Task | Description |
|---|---|
| \U0001f4c2 CD to Current File Folder | Opens CMD in active file\'s folder |
| \U0001f3e0 CD to Workspace Root | Opens CMD at project root |

---

## \U0001f527 VS Code Settings (`.vscode/settings.json`)

| Setting | Default | Description |
|---|---|---|
| `terminal.integrated.cwd` | `workspaceFolder` | Terminal opens at root |
| `editor.formatOnSave` | `true` | Auto format on save |
| `terminal.integrated.defaultProfile.windows` | `Command Prompt` | Use CMD not PowerShell |

### \U0001f501 Toggle Auto CD
```json
// Option 1: Terminal always opens at ROOT (default)
"terminal.integrated.cwd": "${{workspaceFolder}}",

// Option 2: Terminal follows active file folder
// "terminal.integrated.cwd": "${{fileDirname}}"
```

---

## \U0001f433 Docker
```cmd
docker-compose up --build
```
Runs on: `http://localhost:{port}`

---

## \U0001f5c2\ufe0f Environment Variables (`backend/.env`)
```
PORT={port}
DEBUG=true
```

---

## \U0001f4c4 Docs
- `docs/api.md` \u2014 API endpoint documentation
- `docs/node-types.md` \u2014 Node type documentation
- `scripts/HOW_TO_MODIFY.md` \u2014 How to modify `create_project.py`
- `scripts/HOW_TO_SETUP.md` \u2014 How to set up VS Code tasks

---

*Generated by `create_project.py` \u2014 edit `scripts/create_project.py` to customize.*
"""


    # ── Files shared by ALL languages ────────────────────────────────────────
    common_files = {
        "frontend/public/index.html": "<!DOCTYPE html>\n<html>\n<head><title>Node Editor</title></head>\n<body><div id='root'></div></body>\n</html>\n",
        "frontend/src/main.js": "// Entry point\n",
        "frontend/src/core/NodeGraph.js": "// Node graph manager\n",
        "frontend/src/utils/api.js": "// API calls to backend\n",
        "frontend/src/utils/websocket.js": "// WebSocket client\n",
        "frontend/package.json": f'{{\n  "name": "{project_name.lower()}",\n  "version": "1.0.0",\n  "scripts": {{\n    "dev": "vite",\n    "build": "vite build"\n  }}\n}}\n',
        "data/graphs/example_graph.json": "{}\n",
        "docs/api.md": f"# {project_name} API Docs\n",
        "docs/node-types.md": "# Node Types\n",
        ".gitignore": "venv/\n__pycache__/\n*.pyc\n.env\nnode_modules/\ndist/\n",
        # README.md is set per-language below via build_readme()
        "docker-compose.yml": "version: '3'\nservices:\n  backend:\n    build: ./backend\n    ports:\n      - '8000:8000'\n",
        ".vscode/tasks.json": shared_tasks,
    }

    # ══════════════════════════════════════════════════════════════════════════
    #  LANGUAGE 1 — PYTHON (FastAPI)
    # ══════════════════════════════════════════════════════════════════════════
    if lang == "1":
        folders = common_folders + [
            "backend/app/api/routes",
            "backend/app/core",
            "backend/app/nodes/custom_nodes",
            "backend/app/models",
            "backend/app/services",
            "backend/app/utils",
            "backend/tests",
        ]
        files = {
            **common_files,
            "backend/app/__init__.py": "",
            "backend/app/main.py": (
                'from fastapi import FastAPI\n\n'
                'app = FastAPI()\n\n'
                '@app.get("/")\n'
                'def root():\n'
                '    return {"message": "Hello World"}\n'
            ),
            "backend/app/config.py": (
                'import os\n\n'
                'DEBUG = os.getenv("DEBUG", True)\n'
                'HOST  = os.getenv("HOST", "0.0.0.0")\n'
                'PORT  = int(os.getenv("PORT", 8000))\n'
            ),
            "backend/app/api/__init__.py": "",
            "backend/app/api/routes/nodes.py": "# Node API routes\n",
            "backend/app/api/routes/graph.py": "# Graph API routes\n",
            "backend/app/core/__init__.py": "",
            "backend/app/core/base_node.py": (
                'class BaseNode:\n'
                '    """Base class for all node types"""\n'
                '    def __init__(self, node_id, name):\n'
                '        self.node_id = node_id\n'
                '        self.name    = name\n'
                '        self.inputs  = []\n'
                '        self.outputs = []\n\n'
                '    def execute(self):\n'
                '        raise NotImplementedError\n'
            ),
            "backend/app/nodes/__init__.py": "",
            "backend/app/models/__init__.py": "",
            "backend/app/services/__init__.py": "",
            "backend/app/utils/__init__.py": "",
            "backend/tests/test_nodes.py": "# Node tests\n",
            "backend/tests/test_graph.py": "# Graph tests\n",
            "backend/requirements.txt": "fastapi\nuvicorn\npython-dotenv\nwebsockets\n",
            "backend/.env": "DEBUG=True\nHOST=0.0.0.0\nPORT=8000\n",
            # Python-specific VS Code settings — includes interpreter path
            ".vscode/settings.json": (
                '{\n'
                '    // Path to the Python interpreter inside this project venv\n'
                '    "python.defaultInterpreterPath": "./backend/venv/Scripts/python.exe",\n\n'
                + shared_settings_base[2:]  # merge without opening brace duplicate
            ).replace('{\n    // Path', '{\n    // Path'),
        }
        files["README.md"] = build_readme(
            lang_name   = "Python (FastAPI)",
            lang_badge  = "![Python](https://img.shields.io/badge/Python-FastAPI-3776AB?style=flat&logo=python&logoColor=white)",
            backend_structure = (
                "\u2502   \u251c\u2500\u2500 app/\n"
                "\u2502   \u2502   \u251c\u2500\u2500 main.py                 # FastAPI entry point\n"
                "\u2502   \u2502   \u251c\u2500\u2500 config.py               # Configuration\n"
                "\u2502   \u2502   \u251c\u2500\u2500 api/routes/             # API endpoints\n"
                "\u2502   \u2502   \u251c\u2500\u2500 core/base_node.py       # BaseNode class\n"
                "\u2502   \u2502   \u251c\u2500\u2500 nodes/custom_nodes/     # Custom node types\n"
                "\u2502   \u2502   \u251c\u2500\u2500 models/                 # Data models\n"
                "\u2502   \u2502   \u251c\u2500\u2500 services/               # Business logic\n"
                "\u2502   \u2502   \u2514\u2500\u2500 utils/                  # Helpers\n"
                "\u2502   \u251c\u2500\u2500 tests/\n"
                "\u2502   \u251c\u2500\u2500 requirements.txt\n"
                "\u2502   \u251c\u2500\u2500 .env\n"
                "\u2502   \u2514\u2500\u2500 venv/                       # Auto-created virtualenv"
            ),
            install_cmd   = "pip_install.bat requests numpy",
            uninstall_cmd = "pip_uninstall.bat numpy",
            install_note  = "\nActivate venv first:\n```cmd\nbackend\\\\venv\\\\Scripts\\\\activate\n```",
            run_cmd       = "cd backend\nuvicorn app.main:app --reload",
            port          = "8000",
            dep_file      = "requirements.txt",
            wrapper_name  = "pip_install.bat / pip_uninstall.bat",
        )
        run_hint = "uvicorn app.main:app --reload  (inside backend/)"
        return folders, files, run_hint, "python"

    # ══════════════════════════════════════════════════════════════════════════
    #  LANGUAGE 2 — NODE.JS (Express)
    # ══════════════════════════════════════════════════════════════════════════
    elif lang == "2":
        folders = common_folders + [
            "backend/src/routes",
            "backend/src/controllers",
            "backend/src/models",
            "backend/src/services",
            "backend/src/utils",
            "backend/tests",
        ]
        files = {
            **common_files,
            "backend/src/index.js": (
                'const express = require("express");\n'
                'const app     = express();\n'
                'const PORT    = process.env.PORT || 3000;\n\n'
                'app.use(express.json());\n\n'
                'app.get("/", (req, res) => {\n'
                '    res.json({ message: "Hello World" });\n'
                '});\n\n'
                'app.listen(PORT, () => console.log(`Server running on port ${PORT}`));\n'
            ),
            "backend/src/routes/nodes.js": "// Node routes\n",
            "backend/src/routes/graph.js": "// Graph routes\n",
            "backend/src/controllers/nodeController.js": "// Node controller\n",
            "backend/src/models/nodeModel.js": "// Node model\n",
            "backend/src/utils/helpers.js": "// Helper functions\n",
            "backend/tests/nodes.test.js": "// Node tests\n",
            "backend/package.json": (
                f'{{\n'
                f'  "name": "{project_name.lower()}-backend",\n'
                f'  "version": "1.0.0",\n'
                f'  "main": "src/index.js",\n'
                f'  "scripts": {{\n'
                f'    "start": "node src/index.js",\n'
                f'    "dev": "nodemon src/index.js"\n'
                f'  }},\n'
                f'  "dependencies": {{\n'
                f'    "express": "^4.18.2",\n'
                f'    "dotenv": "^16.0.3",\n'
                f'    "cors": "^2.8.5"\n'
                f'  }},\n'
                f'  "devDependencies": {{\n'
                f'    "nodemon": "^3.0.0"\n'
                f'  }}\n'
                f'}}\n'
            ),
            "backend/.env": "PORT=3000\nDEBUG=true\n",
            ".vscode/settings.json": shared_settings_base,
        }
        files["README.md"] = build_readme(
            lang_name   = "Node.js (Express)",
            lang_badge  = "![Node](https://img.shields.io/badge/Node.js-Express-339933?style=flat&logo=nodedotjs&logoColor=white)",
            backend_structure = (
                "\u2502   \u251c\u2500\u2500 src/\n"
                "\u2502   \u2502   \u251c\u2500\u2500 index.js                # Express entry point\n"
                "\u2502   \u2502   \u251c\u2500\u2500 routes/                 # API routes\n"
                "\u2502   \u2502   \u251c\u2500\u2500 controllers/            # Route controllers\n"
                "\u2502   \u2502   \u251c\u2500\u2500 models/                 # Data models\n"
                "\u2502   \u2502   \u251c\u2500\u2500 services/               # Business logic\n"
                "\u2502   \u2502   \u2514\u2500\u2500 utils/                  # Helpers\n"
                "\u2502   \u251c\u2500\u2500 tests/\n"
                "\u2502   \u251c\u2500\u2500 package.json                # express, dotenv, cors\n"
                "\u2502   \u2514\u2500\u2500 .env"
            ),
            install_cmd   = "npm_install.bat express axios",
            uninstall_cmd = "npm_uninstall.bat axios",
            install_note  = "\nFor dev dependencies: `npm_install.bat jest --save-dev`",
            run_cmd       = "cd backend\nnpm install\nnpm run dev",
            port          = "3000",
            dep_file      = "package.json",
            wrapper_name  = "npm_install.bat / npm_uninstall.bat",
        )
        run_hint = "npm install && npm run dev  (inside backend/)"
        return folders, files, run_hint, "node"

    # ══════════════════════════════════════════════════════════════════════════
    #  LANGUAGE 3 — GO
    # ══════════════════════════════════════════════════════════════════════════
    elif lang == "3":
        folders = common_folders + [
            "backend/cmd",
            "backend/internal/api",
            "backend/internal/models",
            "backend/internal/services",
            "backend/internal/utils",
        ]
        files = {
            **common_files,
            "backend/cmd/main.go": (
                'package main\n\n'
                'import (\n'
                '    "fmt"\n'
                '    "net/http"\n'
                ')\n\n'
                'func main() {\n'
                '    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {\n'
                '        fmt.Fprintf(w, `{"message": "Hello World"}`)\n'
                '    })\n'
                '    fmt.Println("Server running on :8080")\n'
                '    http.ListenAndServe(":8080", nil)\n'
                '}\n'
            ),
            "backend/internal/api/router.go": "package api\n\n// Router setup\n",
            "backend/internal/models/node.go": "package models\n\n// Node model\n",
            "backend/go.mod": f"module {project_name.lower()}\n\ngo 1.21\n",
            "backend/.env": "PORT=8080\nDEBUG=true\n",
            ".vscode/settings.json": shared_settings_base,
        }
        files["README.md"] = build_readme(
            lang_name   = "Go",
            lang_badge  = "![Go](https://img.shields.io/badge/Go-1.21-00ADD8?style=flat&logo=go&logoColor=white)",
            backend_structure = (
                "\u2502   \u251c\u2500\u2500 cmd/\n"
                "\u2502   \u2502   \u2514\u2500\u2500 main.go                 # Go entry point\n"
                "\u2502   \u251c\u2500\u2500 internal/\n"
                "\u2502   \u2502   \u251c\u2500\u2500 api/router.go           # Router\n"
                "\u2502   \u2502   \u251c\u2500\u2500 models/node.go          # Data models\n"
                "\u2502   \u2502   \u251c\u2500\u2500 services/               # Business logic\n"
                "\u2502   \u2502   \u2514\u2500\u2500 utils/                  # Helpers\n"
                "\u2502   \u251c\u2500\u2500 go.mod\n"
                "\u2502   \u2514\u2500\u2500 .env"
            ),
            install_cmd   = "go_get.bat github.com/gin-gonic/gin",
            uninstall_cmd = "go_remove.bat github.com/gin-gonic/gin",
            install_note  = "\nGo uses full package paths e.g. `github.com/package/name`",
            run_cmd       = "cd backend\ngo run cmd/main.go",
            port          = "8080",
            dep_file      = "go.mod",
            wrapper_name  = "go_get.bat / go_remove.bat",
        )
        run_hint = "go run cmd/main.go  (inside backend/)"
        return folders, files, run_hint, "go"

    # ══════════════════════════════════════════════════════════════════════════
    #  LANGUAGE 4 — PHP
    # ══════════════════════════════════════════════════════════════════════════
    elif lang == "4":
        folders = common_folders + [
            "backend/public",
            "backend/src/Controllers",
            "backend/src/Models",
            "backend/src/Routes",
            "backend/src/Services",
            "backend/tests",
        ]
        files = {
            **common_files,
            "backend/public/index.php": (
                '<?php\n'
                'header("Content-Type: application/json");\n'
                'echo json_encode(["message" => "Hello World"]);\n'
            ),
            "backend/src/Controllers/NodeController.php": "<?php\n\nclass NodeController {\n    // Node controller\n}\n",
            "backend/src/Models/Node.php": "<?php\n\nclass Node {\n    // Node model\n}\n",
            "backend/src/Routes/api.php": "<?php\n\n// API routes\n",
            "backend/.env": "DEBUG=true\nHOST=0.0.0.0\nPORT=8000\n",
            "backend/composer.json": (
                f'{{\n'
                f'    "name": "{project_name.lower()}/backend",\n'
                f'    "require": {{\n'
                f'        "php": ">=8.0"\n'
                f'    }}\n'
                f'}}\n'
            ),
            ".vscode/settings.json": shared_settings_base,
        }
        files["README.md"] = build_readme(
            lang_name   = "PHP",
            lang_badge  = "![PHP](https://img.shields.io/badge/PHP-8.0+-777BB4?style=flat&logo=php&logoColor=white)",
            backend_structure = (
                "\u2502   \u251c\u2500\u2500 public/\n"
                "\u2502   \u2502   \u2514\u2500\u2500 index.php               # PHP entry point\n"
                "\u2502   \u251c\u2500\u2500 src/\n"
                "\u2502   \u2502   \u251c\u2500\u2500 Controllers/            # MVC controllers\n"
                "\u2502   \u2502   \u251c\u2500\u2500 Models/                 # Data models\n"
                "\u2502   \u2502   \u251c\u2500\u2500 Routes/                 # Route definitions\n"
                "\u2502   \u2502   \u2514\u2500\u2500 Services/               # Business logic\n"
                "\u2502   \u251c\u2500\u2500 tests/\n"
                "\u2502   \u251c\u2500\u2500 composer.json\n"
                "\u2502   \u2514\u2500\u2500 .env"
            ),
            install_cmd   = "composer_install.bat guzzlehttp/guzzle",
            uninstall_cmd = "composer_uninstall.bat guzzlehttp/guzzle",
            install_note  = "\nRequires [Composer](https://getcomposer.org) installed.",
            run_cmd       = "cd backend\nphp -S localhost:8000 public/index.php",
            port          = "8000",
            dep_file      = "composer.json",
            wrapper_name  = "composer_install.bat / composer_uninstall.bat",
        )
        run_hint = "php -S localhost:8000 public/index.php  (inside backend/)"
        return folders, files, run_hint, "php"


# =============================================================================
#  SECTION 3 — PYTHON VENV CREATOR
#  Only runs for Python projects
#  Uses the same Python that is running this script to create the venv
# =============================================================================

def create_venv(venv_path):
    """Creates a Python virtual environment at the given path"""
    print("  \u23f3 Creating venv ...")
    result = subprocess.run(
        [sys.executable, "-m", "venv", venv_path],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("  \u2705 venv created!")
    else:
        print(f"  \u274c venv failed: {result.stderr}")


# =============================================================================
#  SECTION 4 — PIP WRAPPER CREATOR
#  Creates pip_install.bat (Windows) or pip_install.sh (Linux/Mac)
#  This wrapper installs packages AND auto-updates requirements.txt
#
#  Why not use plain pip install?
#  Plain pip install works but does NOT update requirements.txt
#  This wrapper does both in one step
# =============================================================================

def create_pip_watcher(base, venv_path):
    """
    Creates a pip wrapper script that:
      1. Installs the package into the project venv
      2. Runs pip freeze to update requirements.txt automatically

    Usage after creation:
      Windows: pip_install.bat requests
      Linux:   ./pip_install.sh requests
    """

    if os.name == "nt":  # Windows — create .bat file
        pip_wrapper_path = os.path.join(base, "pip_install.bat")
        venv_pip = os.path.join(venv_path, "Scripts", "pip.exe")
        req_file = os.path.join(base, "backend", "requirements.txt")
        content = (
            f'@echo off\n'
            f':: ─────────────────────────────────────────────\n'
            f':: pip_install.bat\n'
            f':: Usage  : pip_install.bat <package>\n'
            f':: Example: pip_install.bat requests\n'
            f':: Example: pip_install.bat numpy pandas flask\n'
            f'::\n'
            f':: Installs into venv AND updates requirements.txt\n'
            f':: ─────────────────────────────────────────────\n\n'
            f'set VENV_PIP={venv_pip}\n'
            f'set REQ={req_file}\n\n'
            f'if "%1"=="" (\n'
            f'    echo No package specified!\n'
            f'    echo Usage: pip_install.bat requests\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo Installing %* ...\n'
            f'"%VENV_PIP%" install %*\n\n'
            f'if %errorlevel% neq 0 (\n'
            f'    echo Install failed!\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo.\n'
            f'echo Updating requirements.txt ...\n'
            f'"%VENV_PIP%" freeze > "%REQ%"\n\n'
            f'echo.\n'
            f'echo Done! requirements.txt updated.\n'
        )
    else:  # Linux/Mac — create .sh file
        pip_wrapper_path = os.path.join(base, "pip_install.sh")
        venv_pip = os.path.join(venv_path, "bin", "pip")
        req_file = os.path.join(base, "backend", "requirements.txt")
        content = (
            f'#!/bin/bash\n'
            f'# ─────────────────────────────────────────────\n'
            f'# pip_install.sh\n'
            f'# Usage  : ./pip_install.sh <package>\n'
            f'# Example: ./pip_install.sh requests\n'
            f'# Example: ./pip_install.sh numpy pandas flask\n'
            f'#\n'
            f'# Installs into venv AND updates requirements.txt\n'
            f'# ─────────────────────────────────────────────\n\n'
            f'VENV_PIP="{venv_pip}"\n'
            f'REQ="{req_file}"\n\n'
            f'if [ -z "$1" ]; then\n'
            f'    echo "No package specified!"\n'
            f'    exit 1\n'
            f'fi\n\n'
            f'echo "Installing $@ ..."\n'
            f'"$VENV_PIP" install "$@"\n\n'
            f'if [ $? -ne 0 ]; then\n'
            f'    echo "Install failed!"\n'
            f'    exit 1\n'
            f'fi\n\n'
            f'echo ""\n'
            f'echo "Updating requirements.txt ..."\n'
            f'"$VENV_PIP" freeze > "$REQ"\n'
            f'echo "Done! requirements.txt updated."\n'
        )

    with open(pip_wrapper_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Make executable on Linux/Mac
    if os.name != "nt":
        os.chmod(pip_wrapper_path, 0o755)

    print("  \u2705 pip_install wrapper created!")


# =============================================================================
#  PYTHON UNINSTALL WRAPPER
#  Removes a package from venv AND updates requirements.txt
#  Usage: pip_uninstall.bat requests
# =============================================================================

def create_pip_uninstall(base, venv_path):
    """Creates pip_uninstall.bat / pip_uninstall.sh"""

    if os.name == "nt":
        path = os.path.join(base, "pip_uninstall.bat")
        venv_pip = os.path.join(venv_path, "Scripts", "pip.exe")
        req_file = os.path.join(base, "backend", "requirements.txt")
        content = (
            f'@echo off\n'
            f':: ─────────────────────────────────────────────\n'
            f':: pip_uninstall.bat\n'
            f':: Usage  : pip_uninstall.bat <package>\n'
            f':: Example: pip_uninstall.bat requests\n'
            f'::\n'
            f':: Removes from venv AND updates requirements.txt\n'
            f':: ─────────────────────────────────────────────\n\n'
            f'set VENV_PIP={venv_pip}\n'
            f'set REQ={req_file}\n\n'
            f'if "%1"=="" (\n'
            f'    echo No package specified!\n'
            f'    echo Usage: pip_uninstall.bat requests\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo Uninstalling %* ...\n'
            f'"%VENV_PIP%" uninstall %* -y\n\n'
            f'if %errorlevel% neq 0 (\n'
            f'    echo Uninstall failed!\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo.\n'
            f'echo Updating requirements.txt ...\n'
            f'"%VENV_PIP%" freeze > "%REQ%"\n\n'
            f'echo.\n'
            f'echo Done! requirements.txt updated.\n'
        )
    else:
        path = os.path.join(base, "pip_uninstall.sh")
        venv_pip = os.path.join(venv_path, "bin", "pip")
        req_file = os.path.join(base, "backend", "requirements.txt")
        content = (
            f'#!/bin/bash\n'
            f'# pip_uninstall.sh — Removes package and updates requirements.txt\n'
            f'# Usage: ./pip_uninstall.sh requests\n\n'
            f'VENV_PIP="{venv_pip}"\n'
            f'REQ="{req_file}"\n\n'
            f'if [ -z "$1" ]; then echo "No package specified!"; exit 1; fi\n\n'
            f'echo "Uninstalling $@ ..."\n'
            f'"$VENV_PIP" uninstall "$@" -y\n\n'
            f'if [ $? -ne 0 ]; then echo "Uninstall failed!"; exit 1; fi\n\n'
            f'echo "Updating requirements.txt ..."\n'
            f'"$VENV_PIP" freeze > "$REQ"\n'
            f'echo "Done! requirements.txt updated."\n'
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    if os.name != "nt":
        os.chmod(path, 0o755)
    print("  \u2705 pip_uninstall wrapper created!")


# =============================================================================
#  NODE.JS INSTALL / UNINSTALL WRAPPERS
#  npm_install.bat   — runs npm install <package> and saves to package.json
#  npm_uninstall.bat — runs npm uninstall <package> and updates package.json
#
#  Note: npm automatically updates package.json on install/uninstall
#  The wrapper just adds clear usage instructions and error handling
#
#  Usage:
#    npm_install.bat express cors
#    npm_uninstall.bat cors
# =============================================================================

def create_npm_wrappers(base):
    """Creates npm_install.bat/.sh and npm_uninstall.bat/.sh for Node.js projects"""

    pkg_dir = os.path.join(base, "backend")

    if os.name == "nt":
        # ── npm install wrapper ──
        content_install = (
            f'@echo off\n'
            f':: ─────────────────────────────────────────────\n'
            f':: npm_install.bat\n'
            f':: Usage  : npm_install.bat <package>\n'
            f':: Example: npm_install.bat express\n'
            f':: Example: npm_install.bat axios cors dotenv\n'
            f'::\n'
            f':: Installs package AND auto-saves to package.json\n'
            f':: Use --save-dev flag for dev dependencies:\n'
            f'::   npm_install.bat jest --save-dev\n'
            f':: ─────────────────────────────────────────────\n\n'
            f'if "%1"=="" (\n'
            f'    echo No package specified!\n'
            f'    echo Usage: npm_install.bat express\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo Installing %* ...\n'
            f'cd /d "{pkg_dir}"\n'
            f'npm install %*\n\n'
            f'if %errorlevel% neq 0 (\n'
            f'    echo Install failed!\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo.\n'
            f'echo Done! package.json updated automatically by npm.\n'
        )

        # ── npm uninstall wrapper ──
        content_uninstall = (
            f'@echo off\n'
            f':: ─────────────────────────────────────────────\n'
            f':: npm_uninstall.bat\n'
            f':: Usage  : npm_uninstall.bat <package>\n'
            f':: Example: npm_uninstall.bat cors\n'
            f'::\n'
            f':: Removes package AND updates package.json\n'
            f':: ─────────────────────────────────────────────\n\n'
            f'if "%1"=="" (\n'
            f'    echo No package specified!\n'
            f'    echo Usage: npm_uninstall.bat cors\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo Uninstalling %* ...\n'
            f'cd /d "{pkg_dir}"\n'
            f'npm uninstall %*\n\n'
            f'if %errorlevel% neq 0 (\n'
            f'    echo Uninstall failed!\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo.\n'
            f'echo Done! package.json updated automatically by npm.\n'
        )

        with open(os.path.join(base, "npm_install.bat"),   "w", encoding="utf-8") as f: f.write(content_install)
        with open(os.path.join(base, "npm_uninstall.bat"), "w", encoding="utf-8") as f: f.write(content_uninstall)

    else:  # Linux/Mac
        content_install = (
            f'#!/bin/bash\n'
            f'# npm_install.sh — Installs package and updates package.json\n'
            f'# Usage: ./npm_install.sh express\n'
            f'# Usage: ./npm_install.sh jest --save-dev\n\n'
            f'if [ -z "$1" ]; then echo "No package specified!"; exit 1; fi\n\n'
            f'cd "{pkg_dir}"\n'
            f'echo "Installing $@ ..."\n'
            f'npm install "$@"\n\n'
            f'if [ $? -ne 0 ]; then echo "Install failed!"; exit 1; fi\n'
            f'echo "Done! package.json updated."\n'
        )
        content_uninstall = (
            f'#!/bin/bash\n'
            f'# npm_uninstall.sh — Removes package and updates package.json\n'
            f'# Usage: ./npm_uninstall.sh cors\n\n'
            f'if [ -z "$1" ]; then echo "No package specified!"; exit 1; fi\n\n'
            f'cd "{pkg_dir}"\n'
            f'echo "Uninstalling $@ ..."\n'
            f'npm uninstall "$@"\n\n'
            f'if [ $? -ne 0 ]; then echo "Uninstall failed!"; exit 1; fi\n'
            f'echo "Done! package.json updated."\n'
        )
        for fname, cont in [("npm_install.sh", content_install), ("npm_uninstall.sh", content_uninstall)]:
            fpath = os.path.join(base, fname)
            with open(fpath, "w", encoding="utf-8") as f: f.write(cont)
            os.chmod(fpath, 0o755)

    print("  \u2705 npm_install / npm_uninstall wrappers created!")


# =============================================================================
#  GO INSTALL / UNINSTALL WRAPPERS
#  go_get.bat    — runs go get <package> and updates go.mod + go.sum
#  go_remove.bat — runs go get <package>@none (Go's way to remove) + tidies mod
#
#  Note: Go uses go.mod and go.sum to track dependencies
#  "go get package@none" is the official Go way to remove a dependency
#
#  Usage:
#    go_get.bat github.com/gin-gonic/gin
#    go_remove.bat github.com/gin-gonic/gin
# =============================================================================

def create_go_wrappers(base):
    """Creates go_get.bat/.sh and go_remove.bat/.sh for Go projects"""

    pkg_dir = os.path.join(base, "backend")

    if os.name == "nt":
        content_install = (
            f'@echo off\n'
            f':: ─────────────────────────────────────────────\n'
            f':: go_get.bat\n'
            f':: Usage  : go_get.bat <package>\n'
            f':: Example: go_get.bat github.com/gin-gonic/gin\n'
            f'::\n'
            f':: Installs package AND updates go.mod + go.sum\n'
            f':: ─────────────────────────────────────────────\n\n'
            f'if "%1"=="" (\n'
            f'    echo No package specified!\n'
            f'    echo Usage: go_get.bat github.com/gin-gonic/gin\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo Installing %* ...\n'
            f'cd /d "{pkg_dir}"\n'
            f'go get %*\n\n'
            f'if %errorlevel% neq 0 (\n'
            f'    echo Install failed!\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo.\n'
            f'echo Tidying go.mod ...\n'
            f'go mod tidy\n\n'
            f'echo.\n'
            f'echo Done! go.mod and go.sum updated.\n'
        )

        content_uninstall = (
            f'@echo off\n'
            f':: ─────────────────────────────────────────────\n'
            f':: go_remove.bat\n'
            f':: Usage  : go_remove.bat <package>\n'
            f':: Example: go_remove.bat github.com/gin-gonic/gin\n'
            f'::\n'
            f':: Removes package AND updates go.mod + go.sum\n'
            f':: Uses "go get package@none" (official Go removal method)\n'
            f':: ─────────────────────────────────────────────\n\n'
            f'if "%1"=="" (\n'
            f'    echo No package specified!\n'
            f'    echo Usage: go_remove.bat github.com/gin-gonic/gin\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo Removing %1 ...\n'
            f'cd /d "{pkg_dir}"\n'
            f'go get %1@none\n\n'
            f'if %errorlevel% neq 0 (\n'
            f'    echo Remove failed!\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo.\n'
            f'echo Tidying go.mod ...\n'
            f'go mod tidy\n\n'
            f'echo.\n'
            f'echo Done! go.mod and go.sum updated.\n'
        )

        with open(os.path.join(base, "go_get.bat"),    "w", encoding="utf-8") as f: f.write(content_install)
        with open(os.path.join(base, "go_remove.bat"), "w", encoding="utf-8") as f: f.write(content_uninstall)

    else:  # Linux/Mac
        content_install = (
            f'#!/bin/bash\n'
            f'# go_get.sh — Installs Go package and updates go.mod + go.sum\n'
            f'# Usage: ./go_get.sh github.com/gin-gonic/gin\n\n'
            f'if [ -z "$1" ]; then echo "No package specified!"; exit 1; fi\n\n'
            f'cd "{pkg_dir}"\n'
            f'echo "Installing $1 ..."\n'
            f'go get "$1"\n\n'
            f'if [ $? -ne 0 ]; then echo "Install failed!"; exit 1; fi\n\n'
            f'echo "Tidying go.mod ..."\n'
            f'go mod tidy\n'
            f'echo "Done! go.mod and go.sum updated."\n'
        )
        content_uninstall = (
            f'#!/bin/bash\n'
            f'# go_remove.sh — Removes Go package and updates go.mod + go.sum\n'
            f'# Usage: ./go_remove.sh github.com/gin-gonic/gin\n\n'
            f'if [ -z "$1" ]; then echo "No package specified!"; exit 1; fi\n\n'
            f'cd "{pkg_dir}"\n'
            f'echo "Removing $1 ..."\n'
            f'go get "$1@none"\n\n'
            f'if [ $? -ne 0 ]; then echo "Remove failed!"; exit 1; fi\n\n'
            f'echo "Tidying go.mod ..."\n'
            f'go mod tidy\n'
            f'echo "Done! go.mod and go.sum updated."\n'
        )
        for fname, cont in [("go_get.sh", content_install), ("go_remove.sh", content_uninstall)]:
            fpath = os.path.join(base, fname)
            with open(fpath, "w", encoding="utf-8") as f: f.write(cont)
            os.chmod(fpath, 0o755)

    print("  \u2705 go_get / go_remove wrappers created!")


# =============================================================================
#  PHP INSTALL / UNINSTALL WRAPPERS
#  composer_install.bat   — runs composer require <package>
#  composer_uninstall.bat — runs composer remove <package>
#  Both auto-update composer.json and composer.lock
#
#  Note: Composer must be installed on the system
#  Install from: https://getcomposer.org
#
#  Usage:
#    composer_install.bat guzzlehttp/guzzle
#    composer_uninstall.bat guzzlehttp/guzzle
# =============================================================================

def create_composer_wrappers(base):
    """Creates composer_install.bat/.sh and composer_uninstall.bat/.sh for PHP projects"""

    pkg_dir = os.path.join(base, "backend")

    if os.name == "nt":
        content_install = (
            f'@echo off\n'
            f':: ─────────────────────────────────────────────\n'
            f':: composer_install.bat\n'
            f':: Usage  : composer_install.bat <package>\n'
            f':: Example: composer_install.bat guzzlehttp/guzzle\n'
            f'::\n'
            f':: Requires Composer installed: https://getcomposer.org\n'
            f':: Installs package AND updates composer.json + composer.lock\n'
            f':: ─────────────────────────────────────────────\n\n'
            f'if "%1"=="" (\n'
            f'    echo No package specified!\n'
            f'    echo Usage: composer_install.bat guzzlehttp/guzzle\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo Installing %* ...\n'
            f'cd /d "{pkg_dir}"\n'
            f'composer require %*\n\n'
            f'if %errorlevel% neq 0 (\n'
            f'    echo Install failed! Is Composer installed?\n'
            f'    echo Download from: https://getcomposer.org\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo.\n'
            f'echo Done! composer.json and composer.lock updated.\n'
        )

        content_uninstall = (
            f'@echo off\n'
            f':: ─────────────────────────────────────────────\n'
            f':: composer_uninstall.bat\n'
            f':: Usage  : composer_uninstall.bat <package>\n'
            f':: Example: composer_uninstall.bat guzzlehttp/guzzle\n'
            f'::\n'
            f':: Removes package AND updates composer.json + composer.lock\n'
            f':: ─────────────────────────────────────────────\n\n'
            f'if "%1"=="" (\n'
            f'    echo No package specified!\n'
            f'    echo Usage: composer_uninstall.bat guzzlehttp/guzzle\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo Removing %* ...\n'
            f'cd /d "{pkg_dir}"\n'
            f'composer remove %*\n\n'
            f'if %errorlevel% neq 0 (\n'
            f'    echo Uninstall failed!\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo.\n'
            f'echo Done! composer.json and composer.lock updated.\n'
        )

        with open(os.path.join(base, "composer_install.bat"),   "w", encoding="utf-8") as f: f.write(content_install)
        with open(os.path.join(base, "composer_uninstall.bat"), "w", encoding="utf-8") as f: f.write(content_uninstall)

    else:  # Linux/Mac
        content_install = (
            f'#!/bin/bash\n'
            f'# composer_install.sh — Installs PHP package\n'
            f'# Usage: ./composer_install.sh guzzlehttp/guzzle\n\n'
            f'if [ -z "$1" ]; then echo "No package specified!"; exit 1; fi\n\n'
            f'cd "{pkg_dir}"\n'
            f'echo "Installing $@ ..."\n'
            f'composer require "$@"\n\n'
            f'if [ $? -ne 0 ]; then echo "Install failed! Is Composer installed?"; exit 1; fi\n'
            f'echo "Done! composer.json updated."\n'
        )
        content_uninstall = (
            f'#!/bin/bash\n'
            f'# composer_uninstall.sh — Removes PHP package\n'
            f'# Usage: ./composer_uninstall.sh guzzlehttp/guzzle\n\n'
            f'if [ -z "$1" ]; then echo "No package specified!"; exit 1; fi\n\n'
            f'cd "{pkg_dir}"\n'
            f'echo "Removing $@ ..."\n'
            f'composer remove "$@"\n\n'
            f'if [ $? -ne 0 ]; then echo "Remove failed!"; exit 1; fi\n'
            f'echo "Done! composer.json updated."\n'
        )
        for fname, cont in [("composer_install.sh", content_install), ("composer_uninstall.sh", content_uninstall)]:
            fpath = os.path.join(base, fname)
            with open(fpath, "w", encoding="utf-8") as f: f.write(cont)
            os.chmod(fpath, 0o755)

    print("  \u2705 composer_install / composer_uninstall wrappers created!")


# =============================================================================
#  SECTION 5 — LANGUAGE SELECTOR
#  Shows an interactive menu for the user to pick backend language
#  To add a new language: add to LANGUAGES dict at top of file
# =============================================================================

def select_language():
    """Shows language selection menu and returns the chosen key"""
    print("\n" + "\u2550" * 42)
    print("   SELECT BACKEND LANGUAGE")
    print("\u2550" * 42)
    for key, name in LANGUAGES.items():
        print(f"   {key}. {name}")
    print("\u2550" * 42)

    while True:
        choice = input("   Enter number (1-4): ").strip()
        if choice in LANGUAGES:
            print(f"\n   \u2705 Selected: {LANGUAGES[choice]}\n")
            return choice
        else:
            print("   \u274c Invalid. Enter 1, 2, 3 or 4.")


# =============================================================================
#  SECTION 6 — MAIN PROJECT CREATOR
#  Orchestrates everything:
#    1. Asks for language if not provided
#    2. Gets folder/file templates for chosen language
#    3. Creates all folders
#    4. Creates all files
#    5. Creates venv (Python only)
#    6. Creates pip wrapper (Python only)
#    7. Copies this script into scripts/ folder
#    8. Prints success message
# =============================================================================

def create_project(project_name, path=".", lang=None):
    """
    Main function to create a full project structure.

    Args:
        project_name : Name of the project (becomes the root folder name)
        path         : Where to create the project (default: current directory)
        lang         : Language number "1"-"4" (if None, user is prompted)
    """

    base = os.path.join(path, project_name)

    # Step 1 — Ask language if not passed as argument
    if lang is None:
        lang = select_language()

    # Step 2 — Get all folders/files for chosen language
    folders, files, run_hint, lang_type = get_language_files(lang, project_name)

    print(f"\n  \u23f3 Creating project '{project_name}' ...")

    # Step 3 — Create all folders
    for folder in folders:
        os.makedirs(os.path.join(base, folder), exist_ok=True)

    # Step 4 — Create all files
    for filepath, content in files.items():
        full_path = os.path.join(base, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    print("  \u2705 Folders and files created!")

    # Step 5 & 6 — Create language-specific install/uninstall wrappers
    if lang_type == "python":
        # Python: create venv first, then pip wrappers
        venv_path = os.path.join(base, "backend", "venv")
        create_venv(venv_path)
        create_pip_watcher(base, venv_path)
        create_pip_uninstall(base, venv_path)
    elif lang_type == "node":
        # Node.js: npm wrappers (npm auto-updates package.json)
        create_npm_wrappers(base)
    elif lang_type == "go":
        # Go: go get/remove wrappers (updates go.mod + go.sum)
        create_go_wrappers(base)
    elif lang_type == "php":
        # PHP: composer wrappers (updates composer.json + composer.lock)
        create_composer_wrappers(base)

    # Step 7 — Create scripts/ folder with all supporting files
    # This gives the developer everything they need in one place:
    #   - create_project.py   : this generator script (copy)
    #   - user_tasks.json     : paste into VS Code User Tasks
    #   - workspace_tasks.json: paste into .code-workspace file
    #   - project_tasks.json  : already in .vscode/tasks.json (reference copy)
    #   - HOW_TO_SETUP.md     : step-by-step setup guide
    scripts_dir = os.path.join(base, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    # ── 7a. Copy this generator script itself ─────────────────────────────
    script_source = os.path.abspath(__file__)
    script_dest   = os.path.join(scripts_dir, "create_project.py")
    try:
        shutil.copy2(script_source, script_dest)
        print("  \u2705 create_project.py copied to scripts/")
    except Exception as e:
        print(f"  \u26a0\ufe0f  Could not copy script: {e}")

    # ── 7b. User Profile Tasks file ───────────────────────────────────────
    # Paste this into: Ctrl+Shift+P → Open User Tasks
    # This makes "Create New Full Project" task available in ALL workspaces
    # Change the path in "args" to point to where create_project.py lives
    user_tasks_content = """\
// =============================================================================
// user_tasks.json
// HOW TO USE:
//   1. Press Ctrl+Shift+P in VS Code
//   2. Type "Open User Tasks" and press Enter
//   3. Copy everything inside the "tasks" array below into that file
//   4. Change YOUR_PATH to the actual path of create_project.py on your PC
//      Example: "C:\\\\DHANA\\\\templates\\\\create_project.py"
//
// RESULT:
//   The "Create New Full Project" task will be available in ALL workspaces
//   and projects globally — no need to add it to each workspace manually
// =============================================================================
{
    "version": "2.0.0",
    "tasks": [
        {
            // This task runs create_project.py to scaffold a new project
            // It asks for a project name then shows the language selector
            "label": "\U0001f680 Create New Full Project",
            "type": "shell",
            "command": "python",
            "args": [
                // !! CHANGE THIS PATH to where create_project.py is stored !!
                "C:\\\\YOUR_PATH\\\\TEMPLETS\\\\create_project.py",

                // ${input:projectName} → VS Code will prompt you to type the name
                "${input:projectName}",

                // ${workspaceFolder} → automatically uses current open folder
                "${workspaceFolder}"
            ],
            "problemMatcher": []
        }
    ],
    "inputs": [
        {
            // This creates the "Enter project name" prompt when task runs
            "id": "projectName",
            "type": "promptString",
            "description": "Enter project name"
        }
    ]
}
"""

    # ── 7c. Workspace Tasks file ──────────────────────────────────────────
    # Paste this into your .code-workspace file
    # Use this if you want tasks available only inside a specific workspace
    # Also includes settings to hide grunt/gulp/npm noise from task list
    workspace_tasks_content = """\
// =============================================================================
// workspace_tasks.json
// HOW TO USE:
//   1. Open your .code-workspace file (e.g. PROJECTS.code-workspace)
//   2. Add the "settings" and "tasks" blocks shown below into it
//   3. Change YOUR_PATH to actual path of create_project.py
//
// RESULT:
//   Tasks will appear only inside this specific workspace
//   grunt/gulp/npm auto-detected tasks will be hidden (cleaner list)
//
// FULL .code-workspace STRUCTURE:
// {
//     "folders": [ {"path": "."} ],
//     "settings": { ... paste settings block here ... },
//     "tasks":    { ... paste tasks block here ... }
// }
// =============================================================================

// ── Paste this as the "settings" block ──────────────────────────────────────
"settings": {
    // Hides auto-detected tasks (grunt, gulp, npm) from task list
    // Only your custom tasks defined below will show up
    "task.quickOpen.showAll": false,
    "task.autoDetect": "off"
},

// ── Paste this as the "tasks" block ─────────────────────────────────────────
"tasks": {
    "version": "2.0.0",
    "tasks": [
        {
            // Creates a new full project using create_project.py
            "label": "\U0001f680 Create New Full Project",
            "type": "shell",
            "command": "python",
            "args": [
                // !! CHANGE THIS to actual path of create_project.py !!
                "C:\\\\YOUR_PATH\\\\TEMPLETS\\\\create_project.py",
                "${input:projectName}",
                "${workspaceFolder}"
            ],
            "problemMatcher": []
        },
        {
            // Opens a CMD terminal in the folder of whichever file is active
            // Useful when you have many subfolders and want to cd quickly
            "label": "\U0001f4c2 CD to Current File Folder",
            "type": "shell",
            "command": "cd /d \\"${fileDirname}\\" && cmd /k",
            "options": {
                "cwd": "${fileDirname}",
                "shell": {
                    // Forces CMD instead of PowerShell
                    // Remove this block if you prefer PowerShell
                    "executable": "cmd.exe",
                    "args": ["/d", "/c"]
                }
            },
            "problemMatcher": []
        },
        {
            // Opens a CMD terminal at the workspace root folder
            "label": "\U0001f3e0 CD to Workspace Root",
            "type": "shell",
            "command": "cd /d \\"${workspaceFolder}\\" && cmd /k",
            "options": {
                "cwd": "${workspaceFolder}",
                "shell": {
                    "executable": "cmd.exe",
                    "args": ["/d", "/c"]
                }
            },
            "problemMatcher": []
        }
    ],
    "inputs": [
        {
            // Prompts user to type a project name when Create task runs
            "id": "projectName",
            "type": "promptString",
            "description": "Enter project name"
        }
    ]
}
"""

    # ── 7d. Project tasks.json reference copy ────────────────────────────
    # This is the same file auto-created in .vscode/tasks.json
    # Saved here as a reference/backup with extra explanation comments
    project_tasks_content = """\
// =============================================================================
// project_tasks.json  (reference copy — actual file is .vscode/tasks.json)
// HOW TO USE:
//   This file is already auto-created at .vscode/tasks.json by create_project.py
//   It activates when you open this project FOLDER DIRECTLY in VS Code
//   (not via a .code-workspace file)
//
// NOTE:
//   If you open this project via a .code-workspace file, these tasks are
//   IGNORED and the workspace tasks take over instead.
//
// TO ADD A NEW TASK:
//   Copy one task block and paste it inside the "tasks": [] array
//   Change the "label" and "command" to what you need
// =============================================================================
{
    "version": "2.0.0",
    "tasks": [
        {
            // Opens CMD terminal in the folder of the currently active file
            // How to run: Ctrl+Shift+P → Run Task → CD to Current File Folder
            "label": "\U0001f4c2 CD to Current File Folder",
            "type": "shell",
            "command": "cd /d \\"${fileDirname}\\" && cmd /k",
            "options": {
                "cwd": "${fileDirname}",
                "shell": {
                    // Using cmd.exe to avoid PowerShell path issues
                    "executable": "cmd.exe",
                    "args": ["/d", "/c"]
                }
            },
            "problemMatcher": []
        },
        {
            // Opens CMD terminal at the project root folder
            // How to run: Ctrl+Shift+P → Run Task → CD to Workspace Root
            "label": "\U0001f3e0 CD to Workspace Root",
            "type": "shell",
            "command": "cd /d \\"${workspaceFolder}\\" && cmd /k",
            "options": {
                "cwd": "${workspaceFolder}",
                "shell": {
                    "executable": "cmd.exe",
                    "args": ["/d", "/c"]
                }
            },
            "problemMatcher": []
        }
    ]
}
"""

    # ── 7e. HOW_TO_SETUP.md — Quick step-by-step setup guide ─────────────
    # Plain language guide for setting up VS Code tasks from scratch
    how_to_content = """\
# \U0001f6e0\ufe0f HOW TO SETUP VS CODE TASKS

This guide explains how to wire up the VS Code tasks for this project.
All the JSON files you need are in this `scripts/` folder.

---

## Step 1 — Set Up the "Create New Full Project" Task

This task lets you scaffold new projects from inside VS Code.
You only need to do this **once** — it works globally after that.

1. Press `Ctrl+Shift+P` in VS Code
2. Type **"Open User Tasks"** and press Enter
3. Open `scripts/user_tasks.json` from this folder
4. Copy the task block and paste it into the User Tasks file
5. **Change the path** in `"args"` to where `create_project.py` lives:
   ```
   "C:\\\\YOUR_ACTUAL_PATH\\\\create_project.py"
   ```
6. Save the file

**To run it:**
```
Ctrl+Shift+P → Run Task → Create New Full Project
→ Type project name → Select language (1-4) → Done!
```

---

## Step 2 — Set Up Workspace Tasks (optional)

Use this if you want tasks available only inside a specific workspace.

1. Open your `.code-workspace` file
2. Open `scripts/workspace_tasks.json` from this folder
3. Copy the `"settings"` block and paste it into `.code-workspace`
4. Copy the `"tasks"` block and paste it into `.code-workspace`
5. Change the path in the Create task args (same as Step 1)
6. Save

**Result:** grunt/gulp/npm tasks are hidden, only your custom tasks show up.

---

## Step 3 — Project Tasks (already done!)

The `.vscode/tasks.json` in this project is **already set up** by `create_project.py`.
It works automatically when you open this folder directly in VS Code.

See `scripts/project_tasks.json` for the reference copy with comments.

---

## Task Priority (which tasks show up when)

| How you open VS Code | Tasks that appear |
|---|---|
| Via `.code-workspace` | Workspace tasks (Step 2) |
| Folder opened directly | Project tasks `.vscode/tasks.json` (Step 3) |
| Always available | User profile tasks (Step 1) |

---

## Files in this scripts/ folder

| File | What it is |
|---|---|
| `create_project.py` | The project generator script (this script!) |
| `user_tasks.json` | Paste into User Tasks — works globally |
| `workspace_tasks.json` | Paste into `.code-workspace` — workspace only |
| `project_tasks.json` | Reference copy of `.vscode/tasks.json` |
| `HOW_TO_SETUP.md` | This file |

---

## How to Add a New Task

1. Open the relevant JSON file (`user_tasks.json`, `workspace_tasks.json`, or `.vscode/tasks.json`)
2. Copy an existing task block inside `"tasks": []`
3. Change the `"label"` (display name) and `"command"` (what runs)
4. Save — task appears immediately in `Ctrl+Shift+P → Run Task`

---

## How to Add a New Language to create_project.py

1. Open `scripts/create_project.py`
2. Find `LANGUAGES = {{ ... }}` at the top
3. Add: `"5": "Your Language"`
4. Find `get_language_files()` function
5. Add an `elif lang == "5":` block with folders, files, run_hint
6. Save — new language appears in selector next time you run the task
"""

    # ── Write all script files ────────────────────────────────────────────
    script_files = {
        "user_tasks.json"      : user_tasks_content,
        "workspace_tasks.json" : workspace_tasks_content,
        "project_tasks.json"   : project_tasks_content,
        "HOW_TO_SETUP.md"      : how_to_content,
    }

    for filename, content in script_files.items():
        filepath = os.path.join(scripts_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    print("  \u2705 All script files created in scripts/ folder!")

    # Step 8 — Print success summary
    print(f"\n  {'='*40}")
    print(f"  \U0001f389 Project '{project_name}' is ready!")
    print(f"  \U0001f4c1 Location : {base}")
    print(f"  \U0001f680 Run      : {run_hint}")

    if lang_type == "python":
        print(f"\n  \U0001f449 Activate venv:")
        print(f"     Windows : backend\\venv\\Scripts\\activate")
        print(f"     Linux   : source backend/venv/bin/activate")
        print(f"\n  \U0001f449 Install a package (auto-updates requirements.txt):")
        print(f"     Windows : pip_install.bat <package>")
        print(f"     Linux   : ./pip_install.sh <package>")
        print(f"\n  \U0001f449 Uninstall a package:")
        print(f"     Windows : pip_uninstall.bat <package>")
        print(f"     Linux   : ./pip_uninstall.sh <package>")
        print(f"\n  \U0001f449 Install all requirements:")
        print(f"     pip install -r backend/requirements.txt")
    elif lang_type == "node":
        print(f"\n  \U0001f449 Install a package (auto-updates package.json):")
        print(f"     Windows : npm_install.bat <package>")
        print(f"     Linux   : ./npm_install.sh <package>")
        print(f"\n  \U0001f449 Uninstall a package:")
        print(f"     Windows : npm_uninstall.bat <package>")
        print(f"     Linux   : ./npm_uninstall.sh <package>")
        print(f"\n  \U0001f449 Install all dependencies:")
        print(f"     cd backend && npm install")
    elif lang_type == "go":
        print(f"\n  \U0001f449 Install a package (auto-updates go.mod):")
        print(f"     Windows : go_get.bat github.com/package/name")
        print(f"     Linux   : ./go_get.sh github.com/package/name")
        print(f"\n  \U0001f449 Remove a package:")
        print(f"     Windows : go_remove.bat github.com/package/name")
        print(f"     Linux   : ./go_remove.sh github.com/package/name")
    elif lang_type == "php":
        print(f"\n  \U0001f449 Install a package (auto-updates composer.json):")
        print(f"     Windows : composer_install.bat vendor/package")
        print(f"     Linux   : ./composer_install.sh vendor/package")
        print(f"\n  \U0001f449 Uninstall a package:")
        print(f"     Windows : composer_uninstall.bat vendor/package")
        print(f"     Linux   : ./composer_uninstall.sh vendor/package")

    print(f"  {'='*40}\n")


# =============================================================================
#  ENTRY POINT
#  Reads project name and output path from command line arguments
#  If not provided, prompts the user interactively
#
#  Usage:
#    python create_project.py my_app
#    python create_project.py my_app "D:\Projects"
# =============================================================================

if __name__ == "__main__":
    # Get project name from args or ask user
    name = sys.argv[1] if len(sys.argv) > 1 else input("  Enter project name: ").strip()
    # Get output path from args or use current directory
    path = sys.argv[2] if len(sys.argv) > 2 else "."
    create_project(name, path)
