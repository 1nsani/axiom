import json
import os

def main():
    print("[*] Memulai Sistem Axiom Primitif")

    # 1. Tentukan lokasi file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "docs", "Problem.md")
    output_file = os.path.join(base_dir, "output.json")

    # 2. Baca file markdown
    print(f"[*] Membaca dari: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        teks_soal = f.read()

    # 3. Ekstraksi secara bodoh/manual (Tanpa AI)
    # Kita anggap program sudah 'tahu' isinya karena ini versi prototipe
    konsep = {
        "objek": "balok",
        "massa": 5,
        "gaya": 20,
        "hukum_fisika": "Newton II",
        "teks_asli": teks_soal
    }

    # 4. Tulis ke file JSON
    print(f"[*] Menulis hasil ke: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(konsep, f, indent=4)

    print("[*] Selesai! Buka output.json untuk melihat hasil.")

if __name__ == "__main__":
    main()
