import sys, os, math, random, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from solvers.katrol import solve_katrol
from mechanics_builder import bangun_sistem_kanes
from mechanics_solver import turunkan_percepatan_simbolik, substitusi_numerik

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

def load_fixture(name):
    with open(os.path.join(FIXTURES_DIR, name), "r") as f:
        return json.load(f)

random.seed(123)
params_list = []
for _ in range(20):
    m1 = round(random.uniform(0.5, 20.0), 2)
    m2 = round(random.uniform(0.5, 20.0), 2)
    g = round(random.uniform(9.5, 10.5), 2)
    params_list.append({'m1': m1, 'm2': m2, 'g': g})

@pytest.mark.parametrize("params", params_list)
def test_migrasi_katrol(params):
    m1 = params['m1']
    m2 = params['m2']
    g = params['g']
    
    known = {"massa_1": m1, "massa_2": m2, "gravitasi": g}
    result_lama = solve_katrol(known)
    a_lama = result_lama["hasil"]["percepatan"]
    T_lama = result_lama["hasil"]["tegangan"]
    
    skema = load_fixture("katrol_atwood.json")
    KM, ctx = bangun_sistem_kanes(skema)
    a_simbolik = turunkan_percepatan_simbolik(KM)
    nilai = {'m1': m1, 'm2': m2, 'g': g}
    a_baru = substitusi_numerik(a_simbolik, nilai, simbol_map=ctx['simbol'])
    
    # Percepatan identik dalam toleransi pembulatan
    assert abs(a_lama - a_baru) < 1e-4, (
        f"m1={m1}, m2={m2}, g={g}: lama={a_lama}, baru={a_baru}"
    )
    
    # Tegangan: T = m1 * (g + a) untuk SEMUA kasus (a bisa positif atau negatif)
    T_baru = m1 * (g + a_baru)
    
    assert abs(T_lama - T_baru) < 1e-2, (
        f"Tegangan: lama={T_lama}, baru={T_baru}, selisih={abs(T_lama - T_baru)}"
    )
