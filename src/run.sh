%%writefile run.sh
#!/bin/bash

# Pindah ke direktori utama (tempat run.sh berada)
cd "$(dirname "$0")"

echo "[+] Memulai proses otonom..."

# 1. Jalankan translator dari dalam folder src
echo "[+] Mengolah 'problem.md' via src/main.py..."
python3 src/main.py

# 2. Validasi output
if [ ! -f "anim_input.json" ]; then
    echo "[-] FATAL: 'anim_input.json' tidak dihasilkan. Periksa src/main.py."
    exit 1
fi

# 3. Eksekusi Render
# Renderer berada di src/renderer.py, jalankan langsung dari root
echo "[+] Rendering visual..."
rm -rf media/
manim -ql src/renderer.py DinamikaTranslasiScene

echo "[+] Selesai."
