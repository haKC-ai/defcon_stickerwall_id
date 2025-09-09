#!/usr/bin/env bash
set -euo pipefail

PYVER="${PYVER:-3.11}"
VENV_DIR="${VENV_DIR:-.venv_stickers}"
REQS_FILE="requirements.txt"

if command -v python${PYVER} >/dev/null 2>&1; then
  PYBIN="$(command -v python${PYVER})"
elif command -v python3 >/dev/null 2>&1; then
  PYBIN="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PYBIN="$(command -v python)"
else
  echo "Python not found" >&2
  exit 1
fi

"$PYBIN" -c "import sys; print(sys.version)"
"$PYBIN" -m venv "$VENV_DIR"
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip >/dev/null
python -m pip install -r "$REQS_FILE" >/dev/null
echo "[*] Ready. Activate with: source $VENV_DIR/bin/activate"
echo "[*] Run: python stickerwall.py --help"
