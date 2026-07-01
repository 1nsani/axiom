import os

# 1. TENTUKAN JALUR ABSOLUT KE DOKUMEN OBSIDIAN
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_file = os.path.join(base_dir, "docs", "Problem.md")

# 2. BACA DENGAN PROTEKSI FALLBACK
def read_problem_file():
    if not os.path.exists(input_file):
        print(f"[-] Warning: {input_file} tidak ditemukan. Memakai prompt cadangan.")
        return "Sebuah balok bermassa 2 kg ditarik gaya 10 N ke kanan di atas lantai licin."
        
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

if __name__ == "__main__":
    text = read_problem_file()
    print(f"[+] Berhasil membaca input:\n{text}")
  
