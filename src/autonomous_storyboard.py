import os
import json
from google import genai
from google.genai import types
# IMPORT MODUL PEMBACA DOKUMEN BARU
from reader import read_problem_file

def generate_autonomous_storyboard():
    print("[*] Menjalankan Autonomous Storyboard Engine...")
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("[-] GAGAL: GOOGLE_API_KEY tidak ditemukan!")
        return
        
    client = genai.Client(api_key=api_key)
    
    # SEKARANG INPUT NYA DINAMIS DARI OBSIDIAN MD FILE!
    problem_text = read_problem_file()
    print(f"[*] AI sedang memproses soal: {problem_text[:50]}...")
    
    prompt = f"""
    Kamu adalah mesin penerjemah visual untuk Manim. Tugasmu adalah membaca soal fisika dan mengubahnya menjadi instruksi visual primitif.
    
    Soal: '{problem_text}'
    
    Keluarkan JSON dengan struktur seperti ini, sesuaikan objeknya secara otonom dengan konten soal:
    {{
        "setup_objects": [
            {{"id": "obj", "type": "Square", "color": "BLUE", "position": [0,0,0]}}
        ],
        "animations": [
            {{"action": "FadeIn", "target_id": "obj", "duration": 1}}
        ]
    }}
    Jawab HANYA dengan JSON murni.
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
    
