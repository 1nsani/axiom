# src/storyboard.py
import json
import os

def build_storyboard():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    concept_file = os.path.join(base_dir, "output.json") # Hasil dari extractor.py kamu
    storyboard_file = os.path.join(base_dir, "storyboard.json")

    # 1. Baca hasil dari AI extractor kamu
    with open(concept_file, 'r', encoding='utf-8') as f:
        concept = json.load(f)

    # 2. Aturan Evolusi Primitif: Susun adegan secara otomatis berdasarkan data
    # Kita buat 3 adegan standar untuk fisika
    storyboard = {
        "metadata": {
            "problem_id": "prob_01",
            "total_scenes": 3
        },
        "scenes": [
            {
                "scene_id": 1,
                "title": "Introduce Object",
                "action": f"Spawn {concept.get('objek', 'benda')} dengan properti massa {concept.get('massa', 0)} kg",
                "duration": 2.0
            },
            {
                "scene_id": 2,
                "title": "Apply Force",
                "action": f"Gambarkan panah gaya sebesar {concept.get('gaya', 0)} N ke arah kanan",
                "duration": 3.0
            },
            {
                "scene_id": 3,
                "title": "Show Formula",
                "action": f"Tampilkan rumus {concept.get('hukum_fisika', 'Newton')} untuk menghitung percepatan",
                "duration": 4.0
            }
        ]
    }

    # 3. Simpan sebagai cetak biru adegan
    with open(storyboard_file, 'w', encoding='utf-8') as f:
        json.dump(storyboard, f, indent=4)
    
    print("[*] Storyboard berhasil dibangun secara modular di storyboard.json!")

if __name__ == "__main__":
    build_storyboard()
  
