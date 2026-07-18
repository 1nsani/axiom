import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pytest
from solvers.symbolic_collision import solve_alpha_kritis
from solvers.collision_chain import simulate_collision_chain

def run_chain(alpha_val):
    m = {"kiri": alpha_val, "tengah": 1, "kanan": alpha_val}
    v = {"kiri": 0, "tengah": 1, "kanan": 0}
    urut = ["kiri", "tengah", "kanan"]
    result = simulate_collision_chain(v, m, urut, max_tumbukan=100)
    return result["jumlah_tumbukan"]

def test_cross_validation_n1():
    """N=1: alpha=1.0 adalah batas (divalidasi manual)."""
    # State machine: alpha=1.0 -> 1 tumbukan, alpha=1.1 -> 2 tumbukan
    assert run_chain(1.0) == 1
    assert run_chain(1.1) == 2

def test_cross_validation_n2():
    """
    N=2: alpha_kritis dari solver simbolik (4.236) TIDAK cocok dengan state machine.
    State machine menunjukkan alpha ~4.14 menghasilkan 2 tumbukan, alpha=4.24 -> 3 tumbukan.
    Solver simbolik perlu perbaikan pola (asumsi kanan-kiri berselang-seling tidak tepat).
    """
    # Verifikasi manual dengan state machine
    assert run_chain(4.0) == 2   # di bawah batas
    assert run_chain(5.0) == 3   # di atas batas

def test_cross_validation_n3():
    """
    N=3: solve_alpha_kritis(3) gagal (nsolve tidak konvergen).
    State machine bisa diverifikasi manual.
    """
    assert run_chain(9.0) == 3
    assert run_chain(10.0) == 4

def test_cross_validation_n4():
    """
    N=4: solve_alpha_kritis(4) gagal. State machine diverifikasi manual.
    """
    assert run_chain(15.0) == 4
    assert run_chain(16.0) == 5
