#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
echo "[+] cwd sekarang: $(pwd)"
rm -rf media/
python3 src/orchestrator.py
