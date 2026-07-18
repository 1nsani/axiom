import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from sympy import symbols, sin, cos, simplify
from mechanics_builder import bangun_sistem_kanes

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

def load_fixture(name):
    with open(os.path.join(FIXTURES_DIR, name), "r") as f:
        return json.load(f)

def test_bidang_miring():
    skema = load_fixture("bidang_miring_gesekan.json")
    KM, ctx = bangun_sistem_kanes(skema)
    assert len(ctx['fr']) == 1
    assert len(ctx['frstar']) == 1

def test_katrol_atwood():
    skema = load_fixture("katrol_atwood.json")
    KM, ctx = bangun_sistem_kanes(skema)
    assert len(ctx['fr']) == 1
    assert len(ctx['frstar']) == 1

def test_gabungan():
    skema = load_fixture("gabungan_bidang_katrol.json")
    KM, ctx = bangun_sistem_kanes(skema)
    assert len(ctx['fr']) == 1
    assert len(ctx['frstar']) == 1

def test_semua_benda_masuk_particles():
    for fname in ["bidang_miring_gesekan.json", "katrol_atwood.json", "gabungan_bidang_katrol.json"]:
        skema = load_fixture(fname)
        KM, ctx = bangun_sistem_kanes(skema)
        assert len(ctx['particles']) == len(skema['benda'])

def test_semua_benda_punya_titik():
    for fname in ["bidang_miring_gesekan.json", "katrol_atwood.json", "gabungan_bidang_katrol.json"]:
        skema = load_fixture(fname)
        KM, ctx = bangun_sistem_kanes(skema)
        for benda in skema['benda']:
            assert benda['id'] in ctx['titik_map']
