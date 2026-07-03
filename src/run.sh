#!/bin/bash
cd "$(dirname "$0")"

# Bersihkan output lama
echo "[+] Membersihkan cache..."
rm -rf media/

# Jalankan Translator
python3 src/main.py

# Jalankan Render standar
echo "[+] Rendering visual..."
manim -ql src/renderer.py DinamikaTranslasiScene
