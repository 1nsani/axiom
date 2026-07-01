import os
import json
from google import genai
from google.genai import types

def generate_autonomous_storyboard():
    print("[*] Menjalankan Autonomous Storyboard Engine...")
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("[-] GAGAL: GOOGLE_API_KEY tidak ditemukan!")
        return
        
    client = genai.Client(api_key=api_key)
    
    # CONTOH UMPAN: Kamu bisa ganti teks ini dengan soal bandul atau balok, AI akan beradaptasi!
    problem_text = (
        "Sebuah bandul matematis dengan panjang tali 3 meter dan beban 1 kg "
        "disimpangkan sehingga membentuk sudut kecil lalu dilepaskan hingga berosilasi."
    )
    
    # PROMPT ARSITEK: Memaksa AI menjadi sutradara animasi yang mengeluarkan perintah primitif (DSL)
    prompt = f"""
    Kamu adalah mesin penerjemah visual untuk Manim. Tugasmu adalah membaca soal fisika dan mengubahnya menjadi instruksi visual primitif.
    
    Soal: '{problem_text}'
    
    Keluarkan JSON dengan struktur seperti ini, sesuaikan objeknya dengan soal (jika bandul buat tali dan lingkaran, jika balok buat kotak):
    {{
        "setup_objects": [
            {{"id": "tali", "type": "Line", "color": "WHITE", "start": [0, 2, 0], "end": [1, -1, 0]}},
            {{"id": "beban", "type": "Circle", "color": "RED", "radius": 0.4, "position": [1, -1, 0]}}
        ],
        "animations": [
            {{"action": "Create", "target_id": "tali", "duration": 1}},
            {{"action": "FadeIn", "target_id": "beban", "duration": 1}},
            {{"action": "Rotate", "target_id": "tali", "angle": -2, "about_point": [0, 2, 0], "duration": 2}}
        ]
    }}
    
    Jawab HANYA dengan JSON murni. Jangan berikan penjelasan teks biasa.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_file = os.path.join(base_dir, "storyboard.json")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print(f"[+] BERHASIL: AI menciptakan cetak biru otonom di {output_file}")
        
    except Exception as e:
        print(f"[-] GAGAL pada AI Engine: {e}")

if __name__ == "__main__":
    generate_autonomous_storyboard()
  
