%%writefile run.sh
#!/bin/bash

# Pindah ke direktori skrip ini berada
cd "$(dirname "$0")"

echo "[+] Memulai pipeline otonom..."

# 1. Main Processor (Translator)
# Pastikan path folder 'docs' sudah benar (huruf kecil)
python3 src/main.py
if [ ! -f "anim_input.json" ]; then
    echo "[-] FATAL: anim_input.json gagal dibuat."
    exit 1
fi

# 2. Rendering
echo "[+] Merender visual..."
rm -rf media/
manim -ql src/renderer.py DinamikaTranslasiScene

# 3. Auto-Display (Jembatan dari Shell ke IPython Kernel)
echo "[+] Menampilkan hasil..."
python3 -c "
from src.display import display_latest_video
from IPython.display import display
display(display_latest_video())
"
