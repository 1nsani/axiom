%%writefile run.sh
#!/bin/bash

# Pastikan kita di folder root proyek
# Kita tidak akan berpindah-pindah folder (cd) agar tidak tersesat
echo "[+] Lokasi saat ini: $(pwd)"

# 1. Jalankan main.py (asumsi berada di ./src/main.py)
echo "[+] Mengolah 'problem.md' via src/main.py..."
if [ -f "./src/main.py" ]; then
    python3 ./src/main.py
else
    echo "[-] ERROR: src/main.py tidak ditemukan!"
    exit 1
fi

# 2. Cek apakah anim_input.json terbuat
if [ ! -f "anim_input.json" ]; then
    echo "[-] ERROR: 'anim_input.json' tidak terbuat. Periksa output dari main.py."
    exit 1
fi

# 3. Jalankan Renderer (asumsi ada di ./src/renderer.py)
echo "[+] Rendering visual via src/renderer.py..."
# Hapus folder media jika ada
rm -rf media/ 
manim -ql src/renderer.py DinamikaTranslasiScene

echo "[+] Selesai."
