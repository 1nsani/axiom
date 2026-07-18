import sys, os
# Path ke Brain: /tmp/Axiom-knowledge/src
sys.path.insert(0, "/tmp/Axiom-knowledge/src")
from analyzer import analyze_physics_problem

def test_mode_simulasi_default():
    text = "Tiga benda bermassa 1, 2, 3 bersentuhan. Benda tengah bergerak dengan kecepatan 2 m/s."
    result = analyze_physics_problem(text)
    assert result["domain"] == "tumbukan_beruntun"
    assert result["problem_mode"] == "simulasi"

def test_mode_cari_kritis():
    text = "Tiga benda berjajar. Tentukan nilai maksimum dari variabel alpha agar terjadi tepat 2 tumbukan."
    result = analyze_physics_problem(text)
    assert result["domain"] == "tumbukan_beruntun"
    assert result["problem_mode"] == "cari_kritis"

def test_mode_cari_kritis_keywords():
    text = "Pada sistem tiga benda, cari supaya terjadi tepat 3 kali tumbukan."
    result = analyze_physics_problem(text)
    assert result["domain"] == "tumbukan_beruntun"
    assert result["problem_mode"] == "cari_kritis"
