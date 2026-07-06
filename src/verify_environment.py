import os, sys, shutil, importlib

AXIOM_PATH = os.environ.get("AXIOM_PATH", "/tmp/axiom")
AXIOM_KNOWLEDGE_PATH = os.environ.get("AXIOM_KNOWLEDGE_PATH", "/tmp/Axiom-knowledge")

def check(condition, name):
    if condition:
        print(f"[✅] {name}")
        return True
    else:
        print(f"[❌] {name}")
        return False

def main():
    all_ok = True
    all_ok &= check(os.path.isdir(AXIOM_PATH) and os.path.isfile(os.path.join(AXIOM_PATH, "src", "renderer.py")),
                    "Repo axiom ditemukan di path yang benar")
    all_ok &= check(os.path.isdir(AXIOM_KNOWLEDGE_PATH) and os.path.isfile(os.path.join(AXIOM_KNOWLEDGE_PATH, "main.py")),
                    "Repo axiom_knowledge ditemukan di path yang benar")
    all_ok &= check(os.getenv("GEMINI_API_KEY") is not None, "GEMINI_API_KEY ada di environment")
    all_ok &= check(shutil.which("latex") and shutil.which("dvisvgm"), "LaTeX/dvisvgm tersedia")
    try:
        importlib.import_module("manim")
        all_ok &= check(True, "Manim importable")
    except ImportError:
        all_ok &= check(False, "Manim importable")
    all_ok &= check(os.path.isdir("/tmp/axiom_shared"), "Folder /tmp/axiom_shared tersedia")
    if not all_ok:
        print("\n[ERROR] Perbaiki masalah di atas sebelum melanjutkan.")
        sys.exit(1)
    else:
        print("\n[OK] Semua komponen siap.")

if __name__ == "__main__":
    main()
