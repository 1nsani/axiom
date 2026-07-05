import os
import sys
import shutil
import importlib

def check(condition, name):
    """Cetak status dan kembalikan True jika kondisi terpenuhi."""
    if condition:
        print(f"[✅] {name}")
        return True
    else:
        print(f"[❌] {name}")
        return False

def main():
    all_ok = True

    # 1. Repo Engine
    engine_path = "/tmp/axiom"
    engine_ok = check(
        os.path.isdir(engine_path) and os.path.isfile(os.path.join(engine_path, "src", "renderer.py")),
        "Repo axiom ditemukan di path yang benar"
    )
    all_ok &= engine_ok

    # 2. Repo Brain
    brain_path = "/tmp/Axiom-knowledge"
    brain_ok = check(
        os.path.isdir(brain_path) and os.path.isfile(os.path.join(brain_path, "main.py")),
        "Repo axiom_knowledge ditemukan di path yang benar"
    )
    all_ok &= brain_ok

    # 3. Gemini API key
    gemini_ok = check(
        os.getenv("GEMINI_API_KEY") is not None,
        "GEMINI_API_KEY ada di environment"
    )
    all_ok &= gemini_ok

    # 4. LaTeX dan dvisvgm
    latex_ok = check(
        shutil.which("latex") is not None and shutil.which("dvisvgm") is not None,
        "LaTeX/dvisvgm tersedia"
    )
    all_ok &= latex_ok

    # 5. Manim dapat diimpor
    try:
        importlib.import_module("manim")
        manim_ok = check(True, "Manim importable")
    except ImportError:
        manim_ok = check(False, "Manim importable")
    all_ok &= manim_ok

    # 6. Folder shared
    shared_ok = check(
        os.path.isdir("/tmp/axiom_shared"),
        "Folder /tmp/axiom_shared tersedia"
    )
    all_ok &= shared_ok

    if not all_ok:
        print("\n[ERROR] Ada komponen yang belum siap. Perbaiki masalah di atas sebelum melanjutkan.")
        sys.exit(1)
    else:
        print("\n[OK] Semua komponen siap. Pipeline dapat dijalankan.")

if __name__ == "__main__":
    main()
