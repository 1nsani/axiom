import json
import os
import sys
import math

# --- 1. PUSTAKA RUMUS FISIKA (DETERMINISTIK) ---
def kalkulasi_bidang_miring(params):
    # Logika Fisika murni. a = g * sin(theta)
    g = params.get("gravitasi", 10)
    sudut = params.get("sudut", 0)
    sudut_rad = math.radians(sudut)
    percepatan = g * math.sin(sudut_rad)
    
    # Generate array koordinat untuk 60 frame (2 detik simulasi)
    lintasan = []
    for frame in range(60):
        t = frame / 30.0
        x = 0.5 * percepatan * (t**2) * math.cos(sudut_rad)
        y = -0.5 * percepatan * (t**2) * math.sin(sudut_rad)
        lintasan.append([x, y, 0])
        
    return {"percepatan": percepatan, "koordinat_animasi": lintasan}

def kalkulasi_bandul(params):
    # Logika bandul akan kamu tulis menggunakan persamaan diferensial nanti
    return {"koordinat_animasi": []}

def kalkulasi_parabola(params):
    # Logika kinematika 2D
    return {"koordinat_animasi": []}


# --- 2. THE ROUTER (MESIN PENGARAH UNIVERSAL) ---
UNIVERSAL_ROUTER = {
    "dinamika_bidang_miring": kalkulasi_bidang_miring,
    "osilasi_bandul": kalkulasi_bandul,
    "kinematika_parabola": kalkulasi_parabola
}

# --- 3. PIPELINE UTAMA SOLVER ---
def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "output.json")
    output_file = os.path.join(base_dir, "trajectory.json")
    
    if not os.path.exists(input_file):
        print("[-] FATAL: output.json dari extractor tidak ada.")
        sys.exit(1)
        
    with open(input_file, 'r') as f:
        data_ekstraksi = json.load(f)
        
    kategori = data_ekstraksi.get("kategori_fisika", "unknown")
    params = data_ekstraksi.get("parameter", {})
    
    # 4. PENCOCOKAN RUTE (ADAPTASI DINAMIS)
    if kategori in UNIVERSAL_ROUTER:
        fungsi_kalkulasi = UNIVERSAL_ROUTER[kategori]
        hasil_fisika = fungsi_kalkulasi(params)
        
        # Simpan struktur final beserta perintah visual
        state_akhir = {
            "objek_visual": data_ekstraksi.get("objek_visual", []),
            "hasil_fisika": hasil_fisika
        }
        
        with open(output_file, 'w') as f:
            json.dump(state_akhir, f, indent=2)
            
        print(f"[+] SOLVER BERHASIL: Rute [{kategori}] dieksekusi. Trajektori ditulis ke trajectory.json")
    else:
        print(f"[-] FATAL: Mesin belum diajari rumus untuk kategori '{kategori}'. Tambahkan fungsi baru di solver.py.")
        sys.exit(1)

if __name__ == "__main__":
    main()
  
