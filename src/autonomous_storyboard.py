import os
import json
from google import genai
from google.genai import types
from reader import read_problem_file

print("[*] Menjalankan Autonomous Storyboard Engine (Mode PRO Maksimal)...")

# 1. AUTENTIKASI KUNCI API
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("[-] GAGAL: GOOGLE_API_KEY tidak ditemukan di environment Colab!")
    exit()

client = genai.Client(api_key=api_key)

# 2. BACA INPUT DARI DOKUMEN OBSIDIAN
problem_text = read_problem_file()
print(f"[*] Menyuplai data soal ke Gemini Pro: {problem_text}")

# 3. PROMPT ARSITEKTUR KOGNITIF TINGKAT TINGGI (MAKSIMAL)
prompt = f"""
Kamu adalah mesin kompilator visual senior untuk Manim Community. Tugasmu adalah menganalisis soal fisika secara mekanis dan menerjemahkannya menjadi representasi koordinat 2D (Sumbu X dan Y) yang akurat.

Soal yang harus dieksekusi: '{problem_text}'

Aturan Mutlak Output JSON:
1. Setiap objek tipe 'Line' WAJIB memiliki array 'start' dan 'end' berupa koordinat [x, y, z].
2. Setiap objek tipe 'Square' atau 'Circle' WAJIB memiliki array 'position' berupa koordinat [x, y, z].
3. Jika soal menyebutkan 'bidang miring', objek 'Line' harus memanjang miring membentuk sudut dari kiri-atas ke kanan-bawah, dan objek 'Square' (balok) harus ditempatkan tepat di atas garis miring tersebut.
4. Nilai warna yang diizinkan hanya: 'WHITE', 'BLUE', 'RED', 'GREEN', 'YELLOW'.

Format struktur JSON yang wajib kamu muntahkan tanpa teks basa-basi:
{{
    "setup_objects": [
        {{
            "id": "bidang_miring",
            "type": "Line",
            "color": "WHITE",
            "start": [-3, 2, 0],
            "end": [3, -1, 0]
        }},
        {{
            "id": "balok",
            "type": "Square",
            "color": "BLUE",
            "position": [-1, 1, 0]
        }}
    ],
    "animations": [
        {{
            "action": "Create",
            "target_id": "bidang_miring",
            "duration": 1
        }},
        {{
            "action": "FadeIn",
            "target_id": "balok",
            "duration": 1
        }},
        {{
            "action": "Rotate",
            "target_id": "balok",
            "angle": -0.5,
            "about_point": [-1, 1, 0],
            "duration": 1
        }}
    ]
}}
"""

# 4. EKSEKUSI PANGGILAN MODEL PRO
try:
    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1 # Dikunci rendah agar AI konsisten dan tidak berhalusinasi kreatif
        ),
    )
    
    # 5. SIMPAN KE STORYBOARD.JSON
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_file = os.path.join(base_dir, "storyboard.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(response.text)
        
    print(f"[+] EVOLUSI PRO SUKSES: Cetak biru kognitif berhasil ditulis di {output_file}")

except Exception as e:
    print(f"[-] GAGAL pada Mesin Gemini Pro: {e}")
    
