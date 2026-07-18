import json, os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from mechanics_builder import bangun_sistem_kanes
from mechanics_solver import turunkan_percepatan_simbolik, substitusi_numerik

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

def load_fixture(name):
    with open(os.path.join(FIXTURES_DIR, name), "r") as f:
        return json.load(f)

def test_bidang_miring_numerik():
    """Bidang miring: m=4, theta=30°, g=10, mu=0 → a = 5.0"""
    skema = load_fixture("bidang_miring_gesekan.json")
    KM, ctx = bangun_sistem_kanes(skema)
    a_simbolik = turunkan_percepatan_simbolik(KM)
    
    nilai = {'m': 4, 'theta': math.radians(30), 'g': 10, 'mu': 0}
    a = substitusi_numerik(a_simbolik, nilai, simbol_map=ctx['simbol'])
    
    assert a == pytest.approx(5.0, abs=1e-6)

def test_katrol_diam():
    """Katrol: m1=5, m2=5 → a = 0"""
    skema = load_fixture("katrol_atwood.json")
    KM, ctx = bangun_sistem_kanes(skema)
    a_simbolik = turunkan_percepatan_simbolik(KM)
    
    nilai = {'m1': 5, 'm2': 5, 'g': 10}
    a = substitusi_numerik(a_simbolik, nilai, simbol_map=ctx['simbol'])
    
    assert a == pytest.approx(0.0, abs=1e-6)

def test_katrol_bergerak():
    """Katrol: m1=3, m2=5 → a = (5-3)*10/(3+5) = 2.5"""
    skema = load_fixture("katrol_atwood.json")
    KM, ctx = bangun_sistem_kanes(skema)
    a_simbolik = turunkan_percepatan_simbolik(KM)
    
    nilai = {'m1': 3, 'm2': 5, 'g': 10}
    a = substitusi_numerik(a_simbolik, nilai, simbol_map=ctx['simbol'])
    
    assert a == pytest.approx(2.5, abs=1e-6)

def test_gabungan_numerik():
    """
    Gabungan bidang miring + katrol:
    m1=2, theta=30°, m2=5, g=10, mu=0
    a = g*(m2 - m1*sin(theta)) / (m1 + m2) = 10*(5 - 2*0.5)/(2+5) = 10*4/7 = 5.7142857...
    """
    skema = load_fixture("gabungan_bidang_katrol.json")
    KM, ctx = bangun_sistem_kanes(skema)
    a_simbolik = turunkan_percepatan_simbolik(KM)
    
    nilai = {'m1': 2, 'm2': 5, 'theta': math.radians(30), 'g': 10, 'mu': 0}
    a = substitusi_numerik(a_simbolik, nilai, simbol_map=ctx['simbol'])
    
    expected = 5.714285714285714
    assert a == pytest.approx(expected, abs=1e-6)
