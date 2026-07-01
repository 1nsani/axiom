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
Kamu adalah modul PARSER DATA untuk simulasi fisika tingkat OSK.
Tugas mutlakmu: Ekstraksi variabel fisis dari teks soal menjadi format JSON.

ATURAN MUTLAK:
1. DILARANG menghitung atau menyimpulkan nilai (misal: jangan menebak gravitasi 9.8 jika tidak ditulis).
2. DILARANG membuat koordinat visual, posisi, atau elemen animasi Manim.
3. Nilai bisa berupa ANGKA (float) ATAU SIMBOL ALJABAR (string) seperti '2m', 'theta', atau 'F'. Ini wajib untuk menangani soal analitik OSK.
4. Jika suatu variabel tidak disebutkan, isi dengan null.

FORMAT OUTPUT JSON WAJIB:
{
  "tipe_soal": "bidang_miring",
  "data": {
    "massa": 4,
    "sudut": 30,
    "gravitasi": 10,
    "gaya_tarik": null,
    "koefisien_gesek": null
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
    
