# 🤝 Contributing to VS Code Project Scaffolder

Thank you for considering contributing! This project is open to everyone.

---

## 🐛 Found a Bug?

1. Open an [Issue](../../issues)
2. Describe what happened
3. Paste the error message
4. Tell us your OS and Python version

---

## 💡 Want to Add a New Language?

1. Fork this repo
2. Open `create_project.py`
3. Add to `LANGUAGES` dict:
   ```python
   "5": "Ruby (Rails)"
   ```
4. Add an `elif lang == "5":` block in `get_language_files()`:
   ```python
   elif lang == "5":
       folders = common_folders + [
           "backend/app/controllers",
           "backend/app/models",
           ...
       ]
       files = {
           **common_files,
           "backend/Gemfile": "...",
           ...
       }
       run_hint = "rails server"
       return folders, files, run_hint, "ruby"
   ```
5. Test it
6. Open a Pull Request

---

## 📋 Pull Request Checklist

- [ ] Code tested and working
- [ ] Comments added to new code
- [ ] README updated if needed
- [ ] No breaking changes to existing languages

---

## 💬 Questions?

Open an Issue and tag it as `question`.
