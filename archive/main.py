import json
import os
import re

def main():
    print("[*] Memulai Sistem Axiom: Pemrosesan Aktif")
    
    # Lokasi file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "docs", "Problem.md")
    output_file = os.path.join(base_dir, "anim_input.json")

    # Baca file markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Ekstraksi Blok JSON dari Markdown (menggunakan regex)
    # Ini mencari teks di antara { ... }
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    
    if json_match:
        data = json.loads(json_match.group(0))
        print(f"[*] Berhasil memproses: {data['parameters']['sudut_kemiringan']} derajat")
    else:
        raise ValueError("Blok JSON tidak ditemukan dalam Problem.md!")

    # Tulis ke file JSON tujuan (anim_input.json agar terbaca oleh renderer)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    print("[*] Selesai. Data telah terupdate.")

if __name__ == "__main__":
    main()
    
