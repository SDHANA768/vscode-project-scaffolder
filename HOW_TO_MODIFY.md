# 🛠️ HOW TO MODIFY `create_project.py`
### Complete Developer Guide — Written by Claude (Anthropic AI)

---

## 📌 QUICK REFERENCE — Section Map

This is the full map of `create_project.py`.
Every section, what it does, and the exact line number where it starts.

```
create_project.py
│
├── SECTION 1  — LANGUAGES dict              → Line 46
│   └── Add new language names here
│
├── SECTION 2  — get_language_files()        → Line 60
│   ├── common_folders   list                → Line 78   ← shared folders ALL languages
│   ├── shared_tasks     variable            → Line 99   ← VS Code tasks ALL languages
│   ├── shared_settings_base variable        → Line 139  ← VS Code settings ALL languages
│   ├── readme_content   variable            → Line 158  ← README template ALL languages
│   ├── common_files     dict                → Line 538  ← shared files ALL languages
│   │
│   ├── Language 1 — Python (FastAPI)        → Line 557
│   ├── Language 2 — Node.js (Express)       → Line 620
│   ├── Language 3 — Go                      → Line 675
│   └── Language 4 — PHP                     → Line 711
│
├── SECTION 3  — create_venv()               → Line 746  ← Python only
│
├── SECTION 4  — Package Wrappers
│   ├── create_pip_watcher()                 → Line 775  ← Python install
│   ├── create_pip_uninstall()               → Line 867  ← Python uninstall
│   ├── create_npm_wrappers()                → Line 941  ← Node.js install+uninstall
│   ├── create_go_wrappers()                 → Line 1050 ← Go install+uninstall
│   └── create_composer_wrappers()           → Line 1165 ← PHP install+uninstall
│
├── SECTION 5  — select_language()           → Line 1263 ← interactive menu
│
└── SECTION 6  — create_project()            → Line 1294 ← main orchestrator
```

---
---

## 🔗 HOW SECTIONS CONNECT TO EACH OTHER

Understanding this is the key to modifying without breaking anything.

```
User runs script
      ↓
SECTION 6 — create_project()           ← STARTS HERE, controls everything
      ↓
      ├── calls select_language()       ← SECTION 5 — shows 1/2/3/4 menu
      │         ↓
      │   returns lang number "1"/"2"/"3"/"4"
      │
      ├── calls get_language_files()    ← SECTION 2 — returns folders+files
      │         ↓
      │   reads: common_folders         ← shared by ALL languages
      │   reads: shared_tasks           ← shared by ALL languages
      │   reads: shared_settings_base   ← shared by ALL languages
      │   reads: readme_content         ← shared by ALL languages
      │   reads: common_files           ← shared by ALL languages
      │   reads: language block 1/2/3/4 ← language-specific extras
      │         ↓
      │   returns: (folders, files, run_hint, lang_type)
      │
      ├── creates all folders
      ├── creates all files
      │
      ├── if lang_type == "python"  → create_venv()          SECTION 3
      │                             → create_pip_watcher()   SECTION 4
      │                             → create_pip_uninstall() SECTION 4
      │
      ├── if lang_type == "node"    → create_npm_wrappers()  SECTION 4
      ├── if lang_type == "go"      → create_go_wrappers()   SECTION 4
      ├── if lang_type == "php"     → create_composer_wrappers() SECTION 4
      │
      └── creates scripts/ folder with all support files
```

**The rule:** If you add a new language in SECTION 1 and SECTION 2,
you MUST also wire it up in SECTION 6. Otherwise the language appears
in the menu but nothing gets created for it.

---
---

## ✏️ MODIFICATION 1 — Add a New Language

**Files to touch:** SECTION 1, SECTION 2, SECTION 6

---

### Step 1 — Add to LANGUAGES dict (Section 1, Line 46)

```python
# BEFORE:
LANGUAGES = {
    "1": "Python (FastAPI)",
    "2": "Node.js (Express)",
    "3": "Go",
    "4": "PHP",
}

# AFTER — adding C# and C:
LANGUAGES = {
    "1": "Python (FastAPI)",
    "2": "Node.js (Express)",
    "3": "Go",
    "4": "PHP",
    "5": "C# (.NET)",       ← new
    "6": "C (CMake)",       ← new
}
```

---

### Step 2 — Add language block in get_language_files() (Section 2, after Line 711)

Find the PHP block ending (around line 743) and add AFTER it:

```python
# ══════════════════════════════════════════════════════════════════════════════
#  LANGUAGE 5 — C# (.NET)
# ══════════════════════════════════════════════════════════════════════════════
elif lang == "5":
    folders = common_folders + [           # ← always start with common_folders
        "backend/src/Controllers",
        "backend/src/Models",
        "backend/src/Services",
        "backend/src/Interfaces",
        "backend/tests",
    ]
    files = {
        **common_files,                    # ← always include common_files first
        "backend/Program.cs": (
            '// C# Entry Point\n'
            'var builder = WebApplication.CreateBuilder(args);\n'
            'var app = builder.Build();\n'
            'app.MapGet("/", () => new { message = "Hello World" });\n'
            'app.Run();\n'
        ),
        "backend/backend.csproj": (
            '<Project Sdk="Microsoft.NET.Sdk.Web">\n'
            '  <PropertyGroup>\n'
            '    <TargetFramework>net8.0</TargetFramework>\n'
            '  </PropertyGroup>\n'
            '</Project>\n'
        ),
        "backend/src/Controllers/NodeController.cs": "// Node controller\n",
        "backend/src/Models/Node.cs":                "// Node model\n",
        "backend/.env":                              "PORT=5000\nDEBUG=true\n",
        ".vscode/settings.json":                     shared_settings_base,
    }
    run_hint = "dotnet run  (inside backend/)"
    return folders, files, run_hint, "csharp"   # ← lang_type = "csharp"


# ══════════════════════════════════════════════════════════════════════════════
#  LANGUAGE 6 — C (CMake)
# ══════════════════════════════════════════════════════════════════════════════
elif lang == "6":
    folders = common_folders + [
        "backend/src",
        "backend/include",
        "backend/tests",
        "backend/build",
    ]
    files = {
        **common_files,
        "backend/src/main.c": (
            '#include <stdio.h>\n\n'
            'int main() {\n'
            '    printf("Hello World\\n");\n'
            '    return 0;\n'
            '}\n'
        ),
        "backend/CMakeLists.txt": (
            'cmake_minimum_required(VERSION 3.10)\n'
            'project(my_project)\n'
            'add_executable(app src/main.c)\n'
        ),
        "backend/include/node.h":  "// Node header\n",
        "backend/.env":            "DEBUG=true\n",
        ".vscode/settings.json":   shared_settings_base,
    }
    run_hint = "cd build && cmake .. && make && ./app  (inside backend/)"
    return folders, files, run_hint, "c"        # ← lang_type = "c"
```

---

### Step 3 — Wire up in create_project() (Section 6, around Line 1360)

Find this block:
```python
elif lang_type == "php":
    create_composer_wrappers(base)
```

Add AFTER it:
```python
elif lang_type == "csharp":
    create_dotnet_wrappers(base)    # ← create this function (see Modification 5)

elif lang_type == "c":
    pass                            # ← no package manager for C, just skip
```

---

### Step 4 — Update success message (Section 6, around Line 1400)

Find the `elif lang_type == "php":` print block and add after:
```python
elif lang_type == "csharp":
    print(f"\n  👉 Install a package:")
    print(f"     Windows : dotnet_install.bat Newtonsoft.Json")
    print(f"     Linux   : ./dotnet_install.sh Newtonsoft.Json")
```

---
---

## ✏️ MODIFICATION 2 — Add or Remove Folders

### Add a folder to ALL languages (Section 2, Line 78)

```python
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
    "scripts",
    "config",              ← ADD: new config folder for all projects
    "tests/integration",   ← ADD: integration tests for all projects
]
```

### Add a folder to ONE language only (inside that language's block)

```python
# Example: add "backend/app/middleware" to Python only
if lang == "1":
    folders = common_folders + [
        "backend/app/api/routes",
        "backend/app/core",
        "backend/app/nodes/custom_nodes",
        "backend/app/models",
        "backend/app/services",
        "backend/app/utils",
        "backend/app/middleware",    ← ADD HERE for Python only
        "backend/tests",
    ]
```

### Remove a folder

Simply delete the line from the list. If it's in `common_folders`
it removes from ALL languages. If it's in a language block,
it removes from that language only.

---
---

## ✏️ MODIFICATION 3 — Rename Files or Folders

### Rename a shared file (Section 2, Line 538)

```python
common_files = {
    # BEFORE:
    "frontend/src/core/NodeGraph.js":  "// Node graph manager\n",

    # AFTER — renamed to GraphEngine.js:
    "frontend/src/core/GraphEngine.js": "// Graph engine\n",
}
```

### Rename a language-specific file

Find the file inside that language's block and change the key:
```python
# Python block — rename main.py to app.py
files = {
    **common_files,

    # BEFORE:
    "backend/app/main.py": "from fastapi import FastAPI...",

    # AFTER:
    "backend/app/app.py": "from fastapi import FastAPI...",
}
```

> ⚠️ If you rename a file that's referenced in `.vscode/settings.json`
> (like `python.defaultInterpreterPath`), update that too!

---
---

## ✏️ MODIFICATION 4 — Edit the README Template

**Location:** Section 2, Line 158 — `readme_content` variable

The README is one big f-string. `{project_name}` gets replaced
automatically with whatever the user types as their project name.

```python
readme_content = f"""# {project_name}

> Your new tagline here     ← CHANGE THIS

---

## 📁 Project Structure
...
```

### Add a new section to README

Find where you want it and paste a new block:
```python
readme_content = f"""# {project_name}

> Node-based web project

---

## 🆕 Prerequisites         ← ADD NEW SECTION

Before starting make sure you have:
- Python 3.8+
- Node.js 18+
- Git

---

## 📁 Project Structure
...
```

### Remove a section from README

Just delete those lines from the f-string. Be careful to keep
the `---` separators balanced.

### Change project description per language

The `readme_content` is shared across all languages right now.
If you want a different README per language, move it INSIDE
each language block like this:

```python
if lang == "1":   # Python
    readme_content = f"""# {project_name}
> Python FastAPI backend project
...
"""
    folders = common_folders + [...]
    files = {
        **common_files,
        "README.md": readme_content,   ← override common_files README
        ...
    }
```

---
---

## ✏️ MODIFICATION 5 — Add a New Package Wrapper

**Location:** Between Section 4 and Section 5 (after Line ~1255)

Copy the pattern from any existing wrapper. Here's the template:

```python
# =============================================================================
#  YOUR LANGUAGE INSTALL / UNINSTALL WRAPPERS
#  your_install.bat   — runs <install command> and updates <dependency file>
#  your_uninstall.bat — runs <remove command> and updates <dependency file>
# =============================================================================

def create_dotnet_wrappers(base):
    """Creates dotnet_install.bat/.sh and dotnet_uninstall.bat/.sh"""

    pkg_dir = os.path.join(base, "backend")   # ← folder where command runs

    if os.name == "nt":   # Windows — .bat files
        content_install = (
            f'@echo off\n'
            f':: ─────────────────────────────────────────────\n'
            f':: dotnet_install.bat\n'
            f':: Usage  : dotnet_install.bat <package>\n'
            f':: Example: dotnet_install.bat Newtonsoft.Json\n'
            f':: ─────────────────────────────────────────────\n\n'
            f'if "%1"=="" (\n'
            f'    echo No package specified!\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo Installing %* ...\n'
            f'cd /d "{pkg_dir}"\n'
            f'dotnet add package %*\n\n'           # ← YOUR INSTALL COMMAND
            f'if %errorlevel% neq 0 (\n'
            f'    echo Install failed!\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo Done! .csproj updated.\n'       # ← YOUR DEPENDENCY FILE
        )

        content_uninstall = (
            f'@echo off\n'
            f':: dotnet_uninstall.bat\n'
            f':: Usage: dotnet_uninstall.bat Newtonsoft.Json\n\n'
            f'if "%1"=="" (\n'
            f'    echo No package specified!\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo Removing %* ...\n'
            f'cd /d "{pkg_dir}"\n'
            f'dotnet remove package %*\n\n'        # ← YOUR REMOVE COMMAND
            f'if %errorlevel% neq 0 (\n'
            f'    echo Remove failed!\n'
            f'    exit /b 1\n'
            f')\n\n'
            f'echo Done! .csproj updated.\n'
        )

        # Write both files
        with open(os.path.join(base, "dotnet_install.bat"),   "w", encoding="utf-8") as f: f.write(content_install)
        with open(os.path.join(base, "dotnet_uninstall.bat"), "w", encoding="utf-8") as f: f.write(content_uninstall)

    else:   # Linux/Mac — .sh files
        content_install = (
            f'#!/bin/bash\n'
            f'# dotnet_install.sh\n'
            f'# Usage: ./dotnet_install.sh Newtonsoft.Json\n\n'
            f'if [ -z "$1" ]; then echo "No package specified!"; exit 1; fi\n\n'
            f'cd "{pkg_dir}"\n'
            f'echo "Installing $@ ..."\n'
            f'dotnet add package "$@"\n\n'
            f'if [ $? -ne 0 ]; then echo "Install failed!"; exit 1; fi\n'
            f'echo "Done!"\n'
        )
        content_uninstall = (
            f'#!/bin/bash\n'
            f'# dotnet_uninstall.sh\n'
            f'# Usage: ./dotnet_uninstall.sh Newtonsoft.Json\n\n'
            f'if [ -z "$1" ]; then echo "No package specified!"; exit 1; fi\n\n'
            f'cd "{pkg_dir}"\n'
            f'echo "Removing $@ ..."\n'
            f'dotnet remove package "$@"\n\n'
            f'if [ $? -ne 0 ]; then echo "Remove failed!"; exit 1; fi\n'
            f'echo "Done!"\n'
        )
        for fname, cont in [
            ("dotnet_install.sh",   content_install),
            ("dotnet_uninstall.sh", content_uninstall)
        ]:
            fpath = os.path.join(base, fname)
            with open(fpath, "w", encoding="utf-8") as f: f.write(cont)
            os.chmod(fpath, 0o755)    # ← make executable on Linux

    print("  ✅ dotnet wrappers created!")
```

---
---

## ✏️ MODIFICATION 6 — Edit VS Code Settings (all projects)

**Location:** Section 2, Line 139 — `shared_settings_base` variable

```python
shared_settings_base = (
    '{\n'
    '    "terminal.integrated.cwd": "${workspaceFolder}",\n'
    '    // "terminal.integrated.cwd": "${fileDirname}",\n'
    '    "terminal.integrated.defaultProfile.windows": "Command Prompt",\n'
    '    "editor.formatOnSave": true\n'

    # ── ADD NEW SETTINGS HERE ──
    '    "editor.fontSize": 14,\n'                    ← example: font size
    '    "editor.tabSize": 4,\n'                      ← example: tab size
    '    "editor.wordWrap": "on",\n'                  ← example: word wrap
    '    "files.autoSave": "afterDelay",\n'           ← example: auto save
    # ──────────────────────────

    '}\n'
)
```

> ⚠️ Every line inside the string except the last setting must end with `,\n`
> The LAST setting before `}` must NOT have a comma

---
---

## ✏️ MODIFICATION 7 — Edit VS Code Tasks (all projects)

**Location:** Section 2, Line 99 — `shared_tasks` variable

```python
shared_tasks = (
    '{\n'
    '    "version": "2.0.0",\n'
    '    "tasks": [\n'

    # ── ADD YOUR NEW TASK HERE ──────────────────────────────────
    '        {\n'
    '            "label": "🔥 Run Backend",\n'           ← display name
    '            "type": "shell",\n'
    '            "command": "uvicorn app.main:app --reload",\n'  ← command
    '            "options": {\n'
    '                "cwd": "${workspaceFolder}/backend",\n'  ← run from here
    '                "shell": {\n'
    '                    "executable": "cmd.exe",\n'
    '                    "args": ["/d", "/c"]\n'
    '                }\n'
    '            },\n'
    '            "problemMatcher": []\n'
    '        },\n'
    # ────────────────────────────────────────────────────────────

    # existing tasks below (keep these):
    '        {\n'
    '            "label": "\U0001f4c2 CD to Current File Folder",\n'
    ...
)
```

> 💡 The `"label"` is what appears in `Ctrl+Shift+P → Run Task`
> Use emoji at the start to make it easy to find in the list

---
---

## ✏️ MODIFICATION 8 — Add a File to Every Project

**Location:** Section 2, Line 538 — `common_files` dict

```python
common_files = {
    "frontend/public/index.html":      "...",
    "frontend/src/main.js":            "...",
    # ... existing files ...

    # ── ADD YOUR NEW FILE HERE ──────────────────────────────────
    "CHANGELOG.md": (
        "# Changelog\n\n"
        "## v1.0.0\n"
        "- Initial release\n"
    ),
    "config/app.json": (
        '{\n'
        '  "debug": true,\n'
        '  "version": "1.0.0"\n'
        '}\n'
    ),
    ".editorconfig": (
        "root = true\n\n"
        "[*]\n"
        "indent_style = space\n"
        "indent_size = 4\n"
        "end_of_line = lf\n"
    ),
    # ────────────────────────────────────────────────────────────
}
```

### Add a file to ONE language only

Find that language's `files` dict and add inside it:

```python
if lang == "1":   # Python only
    files = {
        **common_files,
        "backend/app/main.py":       "...",
        # ...
        "backend/Makefile": (        ← ADD: only Python projects get this
            "run:\n"
            "\tuvicorn app.main:app --reload\n\n"
            "test:\n"
            "\tpytest backend/tests/\n"
        ),
    }
```

---
---

## ✏️ MODIFICATION 9 — Change File Content (Starter Code)

Every file's content is just a string. Find the file in `common_files`
or the language block and edit the string value.

```python
# BEFORE — empty main.py:
"backend/app/main.py": 'from fastapi import FastAPI\n\napp = FastAPI()\n'

# AFTER — more complete starter:
"backend/app/main.py": (
    'from fastapi import FastAPI\n'
    'from fastapi.middleware.cors import CORSMiddleware\n\n'
    'app = FastAPI(title="My API", version="1.0.0")\n\n'
    'app.add_middleware(\n'
    '    CORSMiddleware,\n'
    '    allow_origins=["*"],\n'
    '    allow_methods=["*"],\n'
    '    allow_headers=["*"],\n'
    ')\n\n'
    '@app.get("/")\n'
    'def root():\n'
    '    return {"message": "Hello World", "status": "ok"}\n'
),
```

---
---

## ✅ GOLDEN RULES — Never Break These

| Rule | Why it matters |
|---|---|
| Always put `**common_files` first in every language `files` dict | Without it, shared files like README, frontend, .gitignore won't be created |
| Always end `return` with all 4 values: `return folders, files, run_hint, "lang_type"` | Section 6 unpacks all 4 — missing one crashes the script |
| Use `encoding="utf-8"` on ALL file writes | Prevents emoji/special character errors on Windows |
| `lang_type` string must match exactly in Section 6 | `"csharp"` in Section 2 must be `"csharp"` in Section 6 `if` check |
| Add to LANGUAGES dict AND add elif block — both needed | LANGUAGES adds it to menu, elif block creates the files |
| Test after every change: `python create_project.py test .` | Catches mistakes before real use |

---
---

## 🧪 HOW TO TEST YOUR CHANGES

After every modification, run this in CMD to verify:

```cmd
:: Test — creates a folder called "test" in current directory
python create_project.py test .

:: Check it created correctly
dir test /s
```

If it crashes, Python will show the exact line number of the error.

To test a specific language:
```cmd
:: On Windows you can't pass language interactively via args yet
:: Just run and type the number when prompted
python create_project.py test_python .
```

After confirming it works, delete the test folder:
```cmd
rmdir /s /q test
rmdir /s /q test_python
```

---

## 📋 CHECKLIST — Adding a New Language

Use this checklist every time you add a new language:

- [ ] Added to `LANGUAGES` dict (Section 1)
- [ ] Added `elif lang == "X":` block in `get_language_files()` (Section 2)
- [ ] Block starts with `folders = common_folders + [...]`
- [ ] Block's `files` dict starts with `**common_files`
- [ ] Block ends with `return folders, files, run_hint, "lang_type"`
- [ ] Added install/uninstall wrapper function (Section 4 area)
- [ ] Wired up in `create_project()` (Section 6)
- [ ] Added success message print in Section 6
- [ ] Tested: `python create_project.py test .`
- [ ] Updated README in repo to mention new language
- [ ] Added example output in `examples/` folder

---

*This guide was written by Claude (Anthropic AI) — https://claude.ai*
*Directed by Dhanasekar*

---
---

## 📝 HOW TO EDIT THE README FILES IN THE REPO

The repo has **7 README files** in total. Here's where each one is,
what it covers, and when to update it.

---

### README Map — All 7 Files

```
repo/
├── README.md                          ← 1. MAIN repo README (GitHub front page)
├── HOW_TO_MODIFY.md                   ← 2. This file
├── examples/
│   ├── README.md                      ← 3. Examples overview
│   ├── python_project/README.md       ← 4. Python template docs
│   ├── nodejs_project/README.md       ← 5. Node.js template docs
│   ├── go_project/README.md           ← 6. Go template docs
│   └── php_project/README.md          ← 7. PHP template docs
```

---

### 1. `README.md` — Main Repo README

**What it covers:** Project overview, how it works, quick start,
all language wrappers, VS Code tasks setup, customization guide,
repo files list, credits.

**When to update it:**
- Added a new language → update Supported Languages table
- Added new wrapper feature → update Package Manager Wrappers section
- Added new VS Code task → update VS Code Tasks section
- Added new file to repo → update Repo Files Guide section

**Key sections to find:**

| Section | Find by searching |
|---|---|
| How it works (terminal output) | `✅ Full project structure created!` |
| Folder structure diagram | `├── backend/` |
| Supported Languages table | `\| # \| Language \| Framework` |
| Package wrappers table | `\| Language \| Install \| Uninstall` |
| Examples links | `👀 Example Outputs` |
| Repo Files Guide | `📁 Repo Files Guide` |
| Credits | `👥 Credits` |

---

### 2. `HOW_TO_MODIFY.md` — This File

**What it covers:** How to modify `create_project.py` — add languages,
edit folders, change README template, add wrappers.

**When to update it:**
- Added a new modification type
- Line numbers changed significantly after big edits
- Added a new section to `create_project.py`

---

### 3. `examples/README.md` — Examples Overview

**What it covers:** Overview table of all 4 examples, folder structure
for each language, run commands, install/uninstall wrapper usage.

**When to update it:**
- Added a new language example
- Changed folder structure of any example
- Added new wrappers to any language
- Changed run commands

**Key sections to find:**

| Section | Find by searching |
|---|---|
| Overview table | `\| Folder \| Language \| Framework \| Port` |
| Python structure | `## 🐍 Python Project` |
| Node.js structure | `## 🟩 Node.js Project` |
| Go structure | `## 🔵 Go Project` |
| PHP structure | `## 🐘 PHP Project` |
| Common files table | `## 🔧 Files common to ALL languages` |
| Wrappers table | `## 📦 Package Manager Wrappers` |

---

### 4–7. `examples/LANGUAGE_project/README.md` — Per-Language README

Each example project has its own README. These are also the same files
that get generated inside every new project by `create_project.py`.

**What they cover:** That language's folder structure, how to run,
install/uninstall wrapper usage, VS Code tasks, settings toggle.

**When to update them:**
- Changed that language's folder structure
- Added/changed wrappers for that language
- Changed the run command
- Added new VS Code tasks or settings

**To edit all 4 at once** (for a change that affects all languages
like adding a new common file or VS Code setting):
1. Edit `examples/python_project/README.md` first
2. Copy the changed section to the other 3
3. Adjust language-specific details (port number, run command etc.)

---

### How the Per-Language READMEs Connect to `create_project.py`

The README inside each **example folder** is a static file — it
won't auto-update when you change `create_project.py`.

The README inside each **generated project** comes from the
`readme_content` variable in `create_project.py` (Section 2, Line 158).

So there are TWO places to update:

```
When you change create_project.py...

  1. Update readme_content variable    ← affects future generated projects
     (Section 2, Line 158)

  2. Update examples/LANG/README.md   ← affects what people see on GitHub
     (manual edit)
```

They are separate — changing one does NOT change the other!

---

### Quick Edit Checklist — When Adding a New Language

When you add language 5 (e.g. C#), update ALL these README files:

- [ ] `README.md` — add row to Supported Languages table
- [ ] `README.md` — add row to Package Manager Wrappers table
- [ ] `README.md` — update folder structure diagram to show new wrapper files
- [ ] `README.md` — update "How it works" terminal output block
- [ ] `examples/README.md` — add new language to overview table
- [ ] `examples/README.md` — add new `## C# Project` section
- [ ] `examples/README.md` — add new language row to common files/wrappers table
- [ ] `examples/csharp_project/README.md` — create this new file
- [ ] `HOW_TO_MODIFY.md` — update section map with new line numbers if changed
- [ ] `create_project.py` — update `readme_content` variable with new language info

---

*This guide was written by Claude (Anthropic AI) — https://claude.ai*
*Directed by Dhanasekar*
