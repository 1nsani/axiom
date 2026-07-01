import os
import json
import sys
from google import genai
from google.genai import types

print("[*] Menjalankan Extractor (Phase 1: Ekstraksi Data Murni)...")

# 1. TENTUKAN JALUR ABSOLUT
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_file = os.path.join(base_dir, "docs", "Problem.md")
output_file = os.path.join(base_dir, "output.json")

# 2. VALIDASI INPUT OBSIDIAN
if not os.path.exists(input_file):
    print(f"[-] FATAL: File input tidak ditemukan di {input_file}")
    sys.exit(1)

with open(input_file, 'r', encoding='utf-8') as f:
    problem_text = f.read().strip()

# 3. AUTENTIKASI SDK MODERN
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("[-] FATAL: GOOGLE_API_KEY tidak ditemukan di environment Colab.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

# 4. INSTRUKSI SISTEM ANTI-HALUSINASI & STANDAR OSK
system_instruction = """
Kamu adalah Parser Data Fisika Universal.
Tugas mutlakmu: Ekstraksi variabel fisis ke JSON. 

Kamu WAJIB mengklasifikasikan soal ke dalam SALAH SATU "kategori_fisika" berikut:
1. "dinamika_bidang_miring"
2. "osilasi_bandul"
3. "kinematika_parabola"
4. "hukum_newton_datar"

FORMAT OUTPUT WAJIB:
{
  "kategori_fisika": "<pilih_dari_daftar_di_atas>",
  "objek_visual": ["nama_objek1", "nama_objek2"],
  "parameter": {
     "massa": 4,
     "sudut": 30,
     ... isi null jika tidak disebutkan ...
  }
}
"""


# 5. EKSEKUSI PANGGILAN MODEL
try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=problem_text,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.0,
            system_instruction=system_instruction
        )
    )
    
    # 6. PARSING & VALIDASI DEFENSIF
    data = json.loads(response.text)
    
    # Deteksi kebocoran visual: Jika AI masih mencoba menggambar, matikan paksa.
    if any(bad in str(data).lower() for bad in ["posisi", "koordinat", "warna", "animasi"]):
        print("[-] FATAL: Ekstraktor mencoba menyusupkan data visual. Eksekusi dibatalkan.")
        sys.exit(1)

    # 7. TULIS STATE ANTARA (OUTPUT.JSON)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print(f"[+] EKSTRAKSI SUKSES: Data murni telah diisolasi ke {output_file}")
    
except Exception as e:
    print(f"[-] GAGAL memproses ekstraksi: {e}")
    sys.exit(1)
    
