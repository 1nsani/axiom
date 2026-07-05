import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pytest
from solvers.katrol import solve_katrol

def test_m2_lebih_berat():
    res = solve_katrol({"massa_1": 3, "massa_2": 5})
    # a = (5-3)*10/(3+5) = 20/8 = 2.5
    assert abs(res["hasil"]["percepatan"] - 2.5) < 0.001
    assert res["hasil"]["arah_gerak"] == "m2_turun"
    # T = m1*(g+a) = 3*(10+2.5)=37.5
    assert abs(res["hasil"]["tegangan"] - 37.5) < 0.01

def test_m1_lebih_berat():
    res = solve_katrol({"massa_1": 6, "massa_2": 4})
    # a = (4-6)*10/10 = -2.0
    assert abs(res["hasil"]["percepatan"] - (-2.0)) < 0.001
    assert res["hasil"]["arah_gerak"] == "m1_turun"
    # T = m1*(g+a) = 6*(10-2)=48
    assert abs(res["hasil"]["tegangan"] - 48) < 0.01

def test_massa_sama_diam():
    res = solve_katrol({"massa_1": 5, "massa_2": 5})
    assert res["hasil"]["percepatan"] == 0.0
    assert res["hasil"]["arah_gerak"] == "diam"
    # T = m1*g = 50
    assert abs(res["hasil"]["tegangan"] - 50) < 0.01
