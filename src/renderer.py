import json
import os
import sys

def main():
    print("[*] Menjalankan Renderer (Phase 3: Transpilasi Visual Buta)...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "trajectory.json")
    output_code_file = os.path.join(base_dir, "render.py")
    
    if not os.path.exists(input_file):
        print("[-] FATAL: trajectory.json tidak ditemukan. Solver gagal berjalan.")
        sys.exit(1)
        
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    objek_visual = data.get("objek_visual", [])
    hasil_fisika = data.get("hasil_fisika", {})
    lintasan = hasil_fisika.get("koordinat_animasi", [])
    
    if not lintasan:
        print("[-] FATAL: Data lintasan kosong. Tidak ada yang bisa dianimasikan.")
        sys.exit(1)

    # Ambil titik awal dan akhir dari perhitungan deterministik solver
    titik_awal = lintasan[0]
    titik_akhir = lintasan[-1]
    waktu_tempuh = len(lintasan) / 30.0  # Asumsi 30 FPS dari solver

    manim_code = [
        "from manim import *",
        "",
        "class PhysicsScene(Scene):",
        "    def construct(self):",
        "        # --- SET UP OBJEK ---"
    ]
    indent = "        "
    
    # 1. Gambar Objek Statis (Environment)
    if "bidang_miring" in objek_visual:
        # Gambar garis miring sederhana sebagai pijakan
        manim_code.append(f"{indent}bidang = Line(start={titik_awal}, end=[{titik_akhir[0]}, {titik_akhir[1]-1}, 0], color=WHITE)")
        manim_code.append(f"{indent}self.play(Create(bidang))")
        
    # 2. Gambar Objek Dinamis (Aktor Utama)
    if "balok" in objek_visual:
        manim_code.append(f"{indent}aktor = Square(color=BLUE, side_length=0.5)")
        manim_code.append(f"{indent}aktor.move_to({titik_awal})")
        manim_code.append(f"{indent}self.play(FadeIn(aktor))")
        manim_code.append(f"{indent}self.wait(0.5)")
        
        # 3. Eksekusi Gerakan Berdasarkan Data Solver
        manim_code.append(f"{indent}# Gerakan deterministik dari koordinat solver")
        manim_code.append(f"{indent}self.play(aktor.animate.move_to({titik_akhir}), run_time={waktu_tempuh}, rate_func=rate_functions.ease_in_quad)")
        
    manim_code.append(f"{indent}self.wait(2)")
    
    with open(output_code_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(manim_code))
        
    print(f"[+] RENDERER SUKSES: Skrip render.py berhasil diciptakan berdasarkan data deterministik.")

if __name__ == "__main__":
    main()
  
