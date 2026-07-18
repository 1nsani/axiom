import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from solvers.collision_chain import simulate_collision_chain

def test_alpha_3_di_bawah_kritis():
    """3 benda [3m, m, 3m], tengah v=1 -> 2 tumbukan (benda tengah tidak harus diam)."""
    m = {"kiri": 3, "tengah": 1, "kanan": 3}
    v = {"kiri": 0, "tengah": 1, "kanan": 0}
    urut = ["kiri", "tengah", "kanan"]
    result = simulate_collision_chain(v, m, urut)
    assert result["jumlah_tumbukan"] == 2, f"Jumlah tumbukan = {result['jumlah_tumbukan']}, seharusnya 2"
    assert result["status"] == "stabil"
    # Benda tengah bisa saja masih bergerak setelah tumbukan
    # Yang penting: tumbukan terjadi tepat 2 kali

def test_alpha_5_di_atas_kritis():
    """3 benda [5m, m, 5m], tengah v=1 -> 3 tumbukan."""
    m = {"kiri": 5, "tengah": 1, "kanan": 5}
    v = {"kiri": 0, "tengah": 1, "kanan": 0}
    urut = ["kiri", "tengah", "kanan"]
    result = simulate_collision_chain(v, m, urut)
    assert result["jumlah_tumbukan"] == 3, f"Jumlah tumbukan = {result['jumlah_tumbukan']}, seharusnya 3"
    assert result["status"] == "stabil"

def test_alpha_05_di_bawah_1():
    """3 benda [0.5m, m, 0.5m], tengah v=1 -> 1 tumbukan."""
    m = {"kiri": 0.5, "tengah": 1, "kanan": 0.5}
    v = {"kiri": 0, "tengah": 1, "kanan": 0}
    urut = ["kiri", "tengah", "kanan"]
    result = simulate_collision_chain(v, m, urut)
    assert result["jumlah_tumbukan"] == 1, f"Jumlah tumbukan = {result['jumlah_tumbukan']}, seharusnya 1"
    assert result["status"] == "stabil"

def test_alpha_sangat_besar():
    """alpha = 1000 -> tidak infinite loop, max_tumbukan bekerja."""
    m = {"kiri": 1000, "tengah": 1, "kanan": 1000}
    v = {"kiri": 0, "tengah": 1, "kanan": 0}
    urut = ["kiri", "tengah", "kanan"]
    result = simulate_collision_chain(v, m, urut, max_tumbukan=50)
    assert result["status"] == "stabil"
