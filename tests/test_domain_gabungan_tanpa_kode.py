import sys, os, json, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from mechanics_builder import bangun_sistem_kanes
from mechanics_solver import turunkan_percepatan_simbolik, substitusi_numerik

def test_tidak_ada_solver_python():
    """Buktikan bahwa tidak ada file solvers/bidang_miring_katrol_gabungan.py"""
    solver_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'solvers', 'bidang_miring_katrol_gabungan.py')
    assert not os.path.exists(solver_path), (
        f"File {solver_path} seharusnya TIDAK ADA. "
        f"Domain ini murni dari skema JSON, bukan kode Python."
    )

def test_percepatan_gabungan():
    """
    m1=2kg di bidang 30°, m2=5kg, licin
    a = g*(m2 - m1*sin(theta)) / (m1 + m2)
      = 10*(5 - 2*0.5) / (2+5)
      = 10*4/7 = 5.714285714...
    """
    skema_path = "/tmp/Axiom-knowledge/metadata/domain/bidang_miring_katrol_gabungan.json"
    with open(skema_path) as f:
        skema = json.load(f)
    
    # Set parameter numerik
    skema["benda"][0]["massa"] = 2   # m1
    skema["benda"][1]["massa"] = 5   # m2
    for gaya in skema["gaya"]:
        if "g" in gaya.get("parameter", {}):
            gaya["parameter"]["g"] = 10
    
    KM, ctx = bangun_sistem_kanes(skema)
    a_simbolik = turunkan_percepatan_simbolik(KM)
    
    nilai = {'m1': 2, 'm2': 5, 'theta': math.radians(30), 'g': 10, 'mu': 0}
    a = substitusi_numerik(a_simbolik, nilai, simbol_map=ctx['simbol'])
    
    expected = 5.714285714285714
    assert a == pytest.approx(expected, abs=1e-6), (
        f"Percepatan: {a}, seharusnya {expected}"
    )
