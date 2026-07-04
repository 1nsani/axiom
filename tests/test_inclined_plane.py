import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pytest
from solvers.inclined_plane import solve_inclined_plane

def test_regresi_tanpa_gaya_eksternal():
    """Pastikan hasil sama dengan rumus lama jika tidak ada gaya eksternal."""
    known = {"massa": 5, "sudut_permukaan": 37, "koefisien_gesek": 0.2}
    res = solve_inclined_plane(known)
    # g=10, sin37≈0.6018, cos37≈0.7986 → a = 10*(0.6018 - 0.2*0.7986) = 4.421
    assert abs(res["hasil"]["percepatan"] - 4.421) < 0.01
    assert res["hasil"]["arah_gerak"] == "ke_bawah"
    assert res["hasil"]["gaya_eksternal"] == 0.0

def test_gaya_eksternal_seimbangkan_berat():
    """Gaya eksternal 20 N persis menahan W sin 20 N pada benda 4 kg sudut 30° → diam."""
    known = {"massa": 4, "sudut_permukaan": 30, "gaya_eksternal": 20, "koefisien_gesek": 0.0}
    res = solve_inclined_plane(known)
    assert res["hasil"]["percepatan"] == 0.0
    assert res["hasil"]["arah_gerak"] == "diam"
    assert res["hasil"]["gaya_eksternal"] == 20.0
    assert res["hasil"]["gaya_gesek"] == 0.0

def test_gaya_eksternal_tarik_ke_atas():
    """Gaya 30 N > W sin 20 N → benda bergerak ke atas dengan a = (20-30)/4 = -2.5 m/s²."""
    known = {"massa": 4, "sudut_permukaan": 30, "gaya_eksternal": 30, "koefisien_gesek": 0.0}
    res = solve_inclined_plane(known)
    assert abs(res["hasil"]["percepatan"] - (-2.5)) < 0.01
    assert res["hasil"]["arah_gerak"] == "ke_atas"
