import sys, os, json, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from orchestrator import map_known_to_nilai
from mechanics_builder import bangun_sistem_kanes
from mechanics_solver import turunkan_percepatan_simbolik, substitusi_numerik

def test_pemetaan_massa_ganda():
    """Verifikasi bahwa massa_2 dipetakan ke m2 dengan benar."""
    skema_path = "/tmp/Axiom-knowledge/metadata/domain/bidang_miring_katrol_gabungan.json"
    with open(skema_path) as f:
        skema = json.load(f)
    
    known = {"massa": 4, "massa_2": 5, "sudut_permukaan": 30, "gravitasi": 10, "koefisien_gesek": 0}
    nilai = map_known_to_nilai(known, skema)
    
    assert 'm1' in nilai, "m1 tidak terpetakan"
    assert 'm2' in nilai, "m2 tidak terpetakan"
    assert nilai['m1'] == 4
    assert nilai['m2'] == 5

def test_substitusi_tidak_menyisakan_simbol():
    """Pastikan setelah substitusi tidak ada simbol yang tersisa."""
    skema_path = "/tmp/Axiom-knowledge/metadata/domain/bidang_miring_katrol_gabungan.json"
    with open(skema_path) as f:
        skema = json.load(f)
    
    KM, ctx = bangun_sistem_kanes(skema)
    a_simbolik = turunkan_percepatan_simbolik(KM)
    
    known = {"massa": 4, "massa_2": 5, "sudut_permukaan": 30, "gravitasi": 10, "koefisien_gesek": 0}
    nilai = map_known_to_nilai(known, skema)
    
    a = substitusi_numerik(a_simbolik, nilai, simbol_map=ctx['simbol'])
    assert isinstance(a, float), f"Hasil harus float, bukan {type(a)}"
