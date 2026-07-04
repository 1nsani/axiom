import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from solvers.collision import solve_collision

def test_elastic_equal_mass_velocity_swap():
    result = solve_collision({"massa_1": 2, "massa_2": 2, "v1_awal": 5, "v2_awal": 0, "koefisien_restitusi": 1.0})
    assert abs(result["hasil"]["v1_akhir"] - 0) < 1e-3
    assert abs(result["hasil"]["v2_akhir"] - 5) < 1e-3

def test_perfectly_inelastic_merge():
    result = solve_collision({"massa_1": 3, "massa_2": 5, "v1_awal": 4, "v2_awal": -2, "koefisien_restitusi": 0.0})
    assert abs(result["hasil"]["v1_akhir"] - result["hasil"]["v2_akhir"]) < 1e-3

def test_invalid_approach_velocity_raises():
    with pytest.raises(ValueError):
        solve_collision({"massa_1": 2, "massa_2": 2, "v1_awal": 0, "v2_awal": 5, "koefisien_restitusi": 1.0})
