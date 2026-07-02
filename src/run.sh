%%writefile run.sh
#!/bin/bash

# Pastikan kita di root /content/axiom
echo "[+] Menjalankan sistem di: $(pwd)"

# 1. Jalankan translator (main.py di dalam src/)
echo "[+] Mengolah 'Docs/Problem.md' via src/main.py..."
python3 src/main.py

# 2. Validasi apakah main.py menghasilkan anim_input.json di root
if [ ! -f "anim_input.json" ]; then
    echo "[-] FATAL: 'anim_input.json' tidak ditemukan di $(pwd). Periksa src/main.py."
    exit 1
fi

# 3. Eksekusi Render (renderer.py di dalam src/)
# Kita jalankan langsung dari root agar Manim membaca config dari sini
echo "[+] Rendering visual..."
rm -rf media/
manim -ql src/renderer.py DinamikaTranslasiScene

echo "[+] Selesai. Video tersimpan di media/videos/renderer/480p15/"
