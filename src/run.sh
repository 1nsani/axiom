#!/bin/bash

# 1. Konversi MD ke JSON
echo "[+] Mengolah 'problem.md'..."
python3 main.py

# 2. Validasi keberadaan file
if [ ! -f "anim_input.json" ]; then
    echo "[-] FATAL: 'main.py' gagal menghasilkan 'anim_input.json'"
    exit 1
fi

# 3. Sinkronisasi (Otomatis)
echo "[+] Sinkronisasi ke Tubuh (Axiom)..."
cp anim_input.json axiom/anim_input.json

# 4. Eksekusi Render
echo "[+] Rendering visual..."
cd axiom
rm -rf media/  # Bersihkan residu agar selalu fresh
manim -ql src/renderer.py DinamikaTranslasiScene
cd ..

echo "[+] Selesai. Hasil ada di 'axiom/media/videos/renderer/480p15/'"
