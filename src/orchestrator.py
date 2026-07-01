import subprocess
import sys
import os

def run_module(module_path):
    print(f"\n{'='*50}\n[>] Mengeksekusi: {module_path}\n{'='*50}")
    result = subprocess.run([sys.executable, module_path])
    if result.returncode != 0:
        print(f"\n[!] ERROR FATAL: {module_path} gagal (Exit code {result.returncode}).")
        print("[!] Rantai eksekusi dihentikan paksa untuk mencegah kerusakan data.")
        sys.exit(1)

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Rantai pipa mutlak
    modules = [
        os.path.join(base_dir, "src", "extractor.py"),
        os.path.join(base_dir, "src", "solver.py"),
        os.path.join(base_dir, "src", "renderer.py")
    ]
    
    for mod in modules:
        if not os.path.exists(mod):
            print(f"[!] ERROR: Modul {mod} tidak ditemukan!")
            sys.exit(1)
        run_module(mod)
        
    print(f"\n{'='*50}")
    print("[+] SELURUH RANTAI KOMPILASI BERHASIL DIEKSEKUSI.")
    print("[+] Sistem siap untuk tahap rendering Manim.")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
  
