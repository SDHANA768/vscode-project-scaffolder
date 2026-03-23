# 📂 Examples — Ready-to-Use Project Templates

These are the **exact outputs** of `create_project.py` for all 4 supported languages.
Copy any folder and start coding immediately — everything is pre-configured!

---

## 📋 Available Templates

| Folder | Language | Port | Dependency File |
|---|---|---|---|
| [`python_project/`](python_project/) | ![Python](https://img.shields.io/badge/Python-FastAPI-3776AB?style=flat&logo=python&logoColor=white) | `8000` | `requirements.txt` |
| [`nodejs_project/`](nodejs_project/) | ![Node](https://img.shields.io/badge/Node.js-Express-339933?style=flat&logo=nodedotjs&logoColor=white) | `3000` | `package.json` |
| [`go_project/`](go_project/) | ![Go](https://img.shields.io/badge/Go-1.21-00ADD8?style=flat&logo=go&logoColor=white) | `8080` | `go.mod` |
| [`php_project/`](php_project/) | ![PHP](https://img.shields.io/badge/PHP-8.0+-777BB4?style=flat&logo=php&logoColor=white) | `8000` | `composer.json` |


---

## ![Python](https://img.shields.io/badge/Python-FastAPI-3776AB?style=flat&logo=python&logoColor=white) &nbsp; [`python_project/`](python_project/)

**Backend:** Python (FastAPI) &nbsp;|&nbsp; **Port:** `8000` &nbsp;|&nbsp; **Deps:** `requirements.txt`

```
python_project/
├── backend/
│           ├── routes/
│       ├── core/
│           ├── custom_nodes/
│       ├── models/
│       ├── services/
│       ├── utils/
│   ├── tests/
├── frontend/
├── data/
├── docs/
├── scripts/
├── .vscode/
├── pip_install.bat / pip_uninstall.bat
└── README.md
```

**Run:**
```cmd
uvicorn app.main:app --reload
```

**Install / Uninstall packages:**
```cmd
pip_install.bat requests numpy
pip_uninstall.bat numpy
```

Activate venv first:
```cmd
backend\\\\venv\\\\Scripts\\\\activate
```

---

## ![Node](https://img.shields.io/badge/Node.js-Express-339933?style=flat&logo=nodedotjs&logoColor=white) &nbsp; [`nodejs_project/`](nodejs_project/)

**Backend:** Node.js (Express) &nbsp;|&nbsp; **Port:** `3000` &nbsp;|&nbsp; **Deps:** `package.json`

```
nodejs_project/
├── backend/
│       ├── routes/
│       ├── controllers/
│       ├── models/
│       ├── services/
│       ├── utils/
│   ├── tests/
├── frontend/
├── data/
├── docs/
├── scripts/
├── .vscode/
├── npm_install.bat / npm_uninstall.bat
└── README.md
```

**Run:**
```cmd
npm install && npm run dev
```

**Install / Uninstall packages:**
```cmd
npm_install.bat express axios
npm_uninstall.bat axios
```

For dev dependencies: `npm_install.bat jest --save-dev`

---

## ![Go](https://img.shields.io/badge/Go-1.21-00ADD8?style=flat&logo=go&logoColor=white) &nbsp; [`go_project/`](go_project/)

**Backend:** Go &nbsp;|&nbsp; **Port:** `8080` &nbsp;|&nbsp; **Deps:** `go.mod`

```
go_project/
├── backend/
│   ├── cmd/
│       ├── api/
│       ├── models/
│       ├── services/
│       ├── utils/
├── frontend/
├── data/
├── docs/
├── scripts/
├── .vscode/
├── go_get.bat / go_remove.bat
└── README.md
```

**Run:**
```cmd
go run cmd/main.go
```

**Install / Uninstall packages:**
```cmd
go_get.bat github.com/gin-gonic/gin
go_remove.bat github.com/gin-gonic/gin
```

Go uses full package paths e.g. `github.com/package/name`

---

## ![PHP](https://img.shields.io/badge/PHP-8.0+-777BB4?style=flat&logo=php&logoColor=white) &nbsp; [`php_project/`](php_project/)

**Backend:** PHP &nbsp;|&nbsp; **Port:** `8000` &nbsp;|&nbsp; **Deps:** `composer.json`

```
php_project/
├── backend/
│   ├── public/
│       ├── Controllers/
│       ├── Models/
│       ├── Routes/
│       ├── Services/
│   ├── tests/
├── frontend/
├── data/
├── docs/
├── scripts/
├── .vscode/
├── composer_install.bat / composer_uninstall.bat
└── README.md
```

**Run:**
```cmd
php -S localhost:8000 public/index.php
```

**Install / Uninstall packages:**
```cmd
composer_install.bat guzzlehttp/guzzle
composer_uninstall.bat guzzlehttp/guzzle
```

Requires [Composer](https://getcomposer.org) installed.


---

## 🔧 Files Common to ALL Languages

| File / Folder | Description |
|---|---|
| `frontend/` | Full UI — NodeGraph, components, store, styles |
| `data/graphs/` | Saved graph JSON files |
| `docs/` | API and node-type documentation |
| `.vscode/settings.json` | Terminal CD mode, formatter, CMD default |
| `.vscode/tasks.json` | Pre-configured CD tasks |
| `scripts/create_project.py` | Copy of the generator script |
| `scripts/user_tasks.json` | Paste into VS Code User Tasks (global) |
| `scripts/workspace_tasks.json` | Paste into `.code-workspace` |
| `scripts/project_tasks.json` | Reference copy of `.vscode/tasks.json` |
| `scripts/HOW_TO_SETUP.md` | Step-by-step VS Code task setup guide |
| `docker-compose.yml` | Docker setup |
| `README.md` | Project documentation |

---

## 📦 Package Manager Wrappers

Every language gets **install AND uninstall** wrappers (`.bat` Windows / `.sh` Linux):

| Language | Install | Uninstall | Updates |
|---|---|---|---|
| ![Python](https://img.shields.io/badge/Python-FastAPI-3776AB?style=flat&logo=python&logoColor=white) | `pip_install.bat` | `pip_uninstall.bat` | `requirements.txt` |
| ![Node](https://img.shields.io/badge/Node.js-Express-339933?style=flat&logo=nodedotjs&logoColor=white) | `npm_install.bat` | `npm_uninstall.bat` | `package.json` |
| ![Go](https://img.shields.io/badge/Go-1.21-00ADD8?style=flat&logo=go&logoColor=white) | `go_get.bat` | `go_remove.bat` | `go.mod` |
| ![PHP](https://img.shields.io/badge/PHP-8.0+-777BB4?style=flat&logo=php&logoColor=white) | `composer_install.bat` | `composer_uninstall.bat` | `composer.json` |

---

> Copy any folder above to use as a ready-made project template.
> To generate with a custom name run `create_project.py` from the repo root.
