#!/bin/bash
# ─────────────────────────────────────────────
# pip_install.sh
# Usage  : ./pip_install.sh <package>
# Example: ./pip_install.sh requests
# Example: ./pip_install.sh numpy pandas flask
#
# Installs into venv AND auto-updates requirements.txt
# ─────────────────────────────────────────────

VENV_PIP="$(dirname "$0")/backend/venv/bin/pip"
REQ="$(dirname "$0")/backend/requirements.txt"

if [ -z "$1" ]; then
    echo "No package specified!"
    exit 1
fi

echo "Installing $@ ..."
"$VENV_PIP" install "$@"

if [ $? -ne 0 ]; then
    echo "Install failed!"
    exit 1
fi

echo ""
echo "Updating requirements.txt ..."
"$VENV_PIP" freeze > "$REQ"
echo "Done! requirements.txt updated."
