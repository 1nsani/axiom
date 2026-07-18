import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pytest
import sympy as sp
from solvers.symbolic_collision import solve_alpha_kritis

def test_target_2_alpha_kritis():
    """Untuk target 2 tumbukan, alpha harus 2+sqrt(5) ≈ 4.236067977"""
    result = solve_alpha_kritis(2)
    assert result["alpha_maksimum_desimal"] is not None, "Seharusnya ada solusi"
    # 2 + sqrt(5) = 4.23606797749979
    expected = 2 + sp.sqrt(5)
    assert result["alpha_maksimum_desimal"] == pytest.approx(float(expected), rel=1e-6)
    # Pastikan tidak hardcoded angka
    assert result["alpha_maksimum_desimal"] != 4.236067977  # bukan hasil copy-paste

def test_target_1():
    """Untuk target 1 tumbukan, batas alpha = 1"""
    result = solve_alpha_kritis(1)
    assert result["alpha_maksimum_desimal"] is not None
    # alpha = 1 adalah batas
    assert result["alpha_maksimum_desimal"] == pytest.approx(1.0, rel=1e-6)

def test_target_3():
    """Untuk target 3 tumbukan, pastikan ada solusi (tidak diverifikasi manual)"""
    result = solve_alpha_kritis(3)
    assert result["alpha_maksimum_desimal"] is not None, "Seharusnya ada solusi untuk N=3"
    # Tidak diasumsikan nilainya benar tanpa cross-check, hanya pastikan tidak None
    print(f"Alpha kritis untuk N=3: {result['alpha_maksimum_desimal']}")
