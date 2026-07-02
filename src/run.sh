#!/bin/bash
cd "$(dirname "$0")"

# 1. Translate
python3 src/main.py

# 2. Render
rm -rf media/
manim -ql src/renderer.py DinamikaTranslasiScene

echo "[+] Selesai. Silakan jalankan cell display untuk melihat video."
