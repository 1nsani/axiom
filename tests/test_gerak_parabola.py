import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pytest
import math
from solvers.gerak_parabola import solve_gerak_parabola

def test_kasus_baku_tanah_datar():
    """v0=20 m/s, sudut 45°, g=10, h0=0 → R = v0² sin(2θ)/g = 400*1/10 = 40 m"""
    res = solve_gerak_parabola({"v0": 20, "sudut_elevasi": 45, "gravitasi": 10, "tinggi_awal": 0})
    assert abs(res["hasil"]["jarak_horizontal_maks"] - 40.0) < 0.1
    assert res["hasil"]["waktu_di_udara"] > 0
    assert len(res["hasil"]["titik_lintasan"]) > 10

def test_tinggi_awal_bukan_nol():
    """v0=10, sudut 30°, g=10, h0=5 → waktu > 1.0, jarak > 0"""
    res = solve_gerak_parabola({"v0": 10, "sudut_elevasi": 30, "gravitasi": 10, "tinggi_awal": 5})
    assert res["hasil"]["waktu_di_udara"] > 1.0
    assert res["hasil"]["jarak_horizontal_maks"] > 5.0
    assert res["hasil"]["tinggi_maksimum"] > 5.0

def test_tinggi_maksimum():
    """v0=10, sudut 90°, g=10 → H = v0²/(2g) = 5 m"""
    res = solve_gerak_parabola({"v0": 10, "sudut_elevasi": 90, "gravitasi": 10, "tinggi_awal": 0})
    assert abs(res["hasil"]["tinggi_maksimum"] - 5.0) < 0.1
