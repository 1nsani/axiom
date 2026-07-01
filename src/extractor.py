import os
import json
import google.generativeai as genai

def extract_concept():
    print("[*] Menjalankan Extractor...")
    
    # 1. Ambil API Key dari lingkungan sistem
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("[-] GAGAL: Variabel lingkungan GOOGLE_API_KEY tidak ditemukan!")
        return
        
    genai.configure(api_key=api_key)
    
    # 2. Inisiasi model yang tepat
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # 3. Definisikan umpan soal (Problem)
    # Di fase awal, kita gunakan string teks ini sebagai simulasi isi Problem.md
    problem_text = (
        "Sebuah balok bermassa 5 kg berada di atas meja datar yang licin. "
        "Balok ditarik dengan gaya konstan 20 N ke kanan. Hitung percepatan balok menggunakan Newton II."
    )
    
    # 4. Prompt instruksi kaku
    prompt = (
        f"Ekstrak data dari soal fisika berikut ini: '{problem_text}'. "
        "Buatlah sebuah JSON dengan key wajib berikut: 'objek', 'massa', 'gaya', 'hukum_fisika'. "
        "Isi nilainya sesuai data yang ada di dalam soal."
    )
    
    try:
        # 5. Panggil API dengan konfigurasi JSON yang benar (Mencegah Error 400)
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # 6. Tentukan jalur penyimpanan absolut ke folder utama (/content/axiom/output.json)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_file = os.path.join(base_dir, "output.json")
        
        # 7. Tulis data teks JSON dari AI langsung ke file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print(f"[+] BERHASIL: File JSON sukses diciptakan di {output_file}")
        
    except Exception as e:
        print(f"[-] GAGAL saat memanggil API Gemini: {e}")

if __name__ == "__main__":
    extract_concept()
    
