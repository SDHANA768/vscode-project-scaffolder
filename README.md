<div align="center">

# 🚀 VS Code Project Scaffolder

**Instantly generate professional full-stack project structures from inside VS Code**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![VS Code](https://img.shields.io/badge/VS%20Code-Task-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)](https://code.visualstudio.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Open Source](https://img.shields.io/badge/Open-Source-orange?style=for-the-badge)]()

---

> 🤖 **AI-Assisted Project** — Coded by [Claude (Anthropic)](https://claude.ai) · Instructed & Directed by **Dhanasekar**
>
> *This is Dhanasekar's first open source project on GitHub!* 🎉

---

</div>

## ✨ What is this?

A single Python script that scaffolds a **complete, production-ready project structure** in seconds — directly from a VS Code task. No more manually creating folders, config files, or boilerplate code.

Press `Ctrl+Shift+P` → `Run Task` → `🚀 Create New Full Project`, type a name, pick a language — done!

---

## 🎬 How it works

```
Ctrl+Shift+P → Run Task → 🚀 Create New Full Project
        ↓
  Enter project name: my_app
        ↓
  ════════════════════════════════════════
    SELECT BACKEND LANGUAGE
  ════════════════════════════════════════
    1. Python (FastAPI)
    2. Node.js (Express)
    3. Go
    4. PHP
  ════════════════════════════════════════
        ↓
  ✅ Folders and files created!
  ✅ venv created!              (Python only)
  ✅ Install wrappers created!  (all languages)
  ✅ All script files created in scripts/
```

---

## 🌐 Supported Languages

| # | Language | Dependency File | Run Command |
|---|---|---|---|
| 1 | **Python (FastAPI)** | `requirements.txt` | `uvicorn app.main:app --reload` |
| 2 | **Node.js (Express)** | `package.json` | `npm install && npm run dev` |
| 3 | **Go** | `go.mod` | `go run cmd/main.go` |
| 4 | **PHP** | `composer.json` | `php -S localhost:8000 public/index.php` |

---

## 👀 Example Outputs

Browse the [`examples/`](examples/) folder to see the exact output before running:

| Folder | Language |
|---|---|
| [`examples/python_project/`](examples/python_project/) | ![Python](https://img.shields.io/badge/Python-FastAPI-3776AB?style=flat&logo=python&logoColor=white) |
| [`examples/nodejs_project/`](examples/nodejs_project/) | ![Node](https://img.shields.io/badge/Node.js-Express-339933?style=flat&logo=nodedotjs&logoColor=white) |
| [`examples/go_project/`](examples/go_project/) | ![Go](https://img.shields.io/badge/Go-1.21-00ADD8?style=flat&logo=go&logoColor=white) |
| [`examples/php_project/`](examples/php_project/) | ![PHP](https://img.shields.io/badge/PHP-8.0+-777BB4?style=flat&logo=php&logoColor=white) |

---

## ⚡ Quick Start

### Step 1 — Get the script

```bash
git clone https://github.com/SDHANA768/vscode-project-scaffolder.git
```

### Step 2 — Set up VS Code Task (one time only)

`Ctrl+Shift+P` → **"Open User Tasks"** → add:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "🚀 Create New Full Project",
            "type": "shell",
            "command": "python",
            "args": [
                "C:\\YOUR_PATH\\create_project.py",
                "${input:projectName}",
                "${workspaceFolder}"
            ],
            "problemMatcher": []
        }
    ],
    "inputs": [
        {
            "id": "projectName",
            "type": "promptString",
            "description": "Enter project name"
        }
    ]
}
```

Change `YOUR_PATH` to where you saved `create_project.py`.

### Step 3 — Run!

```
Ctrl+Shift+P → Run Task → 🚀 Create New Full Project
```

---

## 📦 Smart Package Manager Wrappers

Every generated project gets **install and uninstall wrappers** that auto-update the dependency file:

| Language | Install | Uninstall | Updates |
|---|---|---|---|
| ![Python](https://img.shields.io/badge/Python-FastAPI-3776AB?style=flat&logo=python&logoColor=white) | `pip_install.bat` | `pip_uninstall.bat` | `requirements.txt` |
| ![Node](https://img.shields.io/badge/Node.js-Express-339933?style=flat&logo=nodedotjs&logoColor=white) | `npm_install.bat` | `npm_uninstall.bat` | `package.json` |
| ![Go](https://img.shields.io/badge/Go-1.21-00ADD8?style=flat&logo=go&logoColor=white) | `go_get.bat` | `go_remove.bat` | `go.mod` |
| ![PHP](https://img.shields.io/badge/PHP-8.0+-777BB4?style=flat&logo=php&logoColor=white) | `composer_install.bat` | `composer_uninstall.bat` | `composer.json` |

All wrappers have `.sh` versions for **Linux / Mac** too.

---

## ⚙️ VS Code Tasks Included

Every project gets `.vscode/tasks.json` pre-configured:

| Task | What it does |
|---|---|
| 📂 CD to Current File Folder | Opens CMD in the active file's folder |
| 🏠 CD to Workspace Root | Opens CMD at project root |

---

## 📁 Repo Files

| File | Description |
|---|---|
| `create_project.py` | The main generator script |
| `README.md` | This file |
| `CONTRIBUTING.md` | How to contribute |
| `LICENSE` | MIT license |
| `examples/` | Ready-to-use project templates for all languages |

---

## 🤝 Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) — PRs welcome for new languages and features!

---

## 📄 License

MIT — free to use, modify and distribute. See [LICENSE](LICENSE).

---

<div align="center">

## 👥 Credits

| Role | Person |
|---|---|
| 💡 Idea, Direction & Testing | **Dhanasekar** |
| 🤖 Code & Implementation | **Claude (Anthropic AI)** |
| 📁 GitHub Repository & Docs | **Claude (Anthropic AI)** |

---

> *"Every line of code, the folder structure, the documentation,*
> *and this GitHub repository — all created by Claude AI*
> *through a conversation with Dhanasekar.*
> *Dhanasekar directed every feature. Claude wrote the code.*
> *Together we built something useful."*

---

**Made with ❤️ — Dhanasekar's first open source project**

⭐ Star this repo if it helped you!

</div>
