import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from mechanics_registry import validate_system_def, SUPPORTED_ARAH_GERAK, SUPPORTED_GAYA

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

def load_fixture(name):
    with open(os.path.join(FIXTURES_DIR, name), "r") as f:
        return json.load(f)

def test_fixtures_are_valid_json():
    """Semua fixture bisa dibaca sebagai JSON."""
    for fname in ["bidang_miring_gesekan.json", "katrol_atwood.json", "gabungan_bidang_katrol.json"]:
        data = load_fixture(fname)
        assert isinstance(data, dict)
        assert "sistem_id" in data
        assert "koordinat_umum" in data
        assert "benda" in data
        assert "gaya" in data

def test_fixtures_pass_registry_validation():
    """Semua fixture memiliki tipe yang terdaftar di registry."""
    for fname in ["bidang_miring_gesekan.json", "katrol_atwood.json", "gabungan_bidang_katrol.json"]:
        data = load_fixture(fname)
        # Seharusnya tidak raise ValueError
        validate_system_def(data)

def test_registry_raises_on_unknown_type():
    """Registry harus raise ValueError untuk tipe tidak dikenal."""
    invalid = {
        "sistem_id": "test",
        "koordinat_umum": ["q1"],
        "benda": [
            {
                "id": "x",
                "massa_simbol": "m",
                "massa": 1,
                "arah_gerak": {"tipe": "diagonal_ajaib", "parameter": {}, "tanda": 1},
                "koefisien_koordinat": "q1"
            }
        ],
        "gaya": []
    }
    try:
        validate_system_def(invalid)
        assert False, "Seharusnya raise ValueError"
    except ValueError as e:
        assert "diagonal_ajaib" in str(e)

def test_koordinat_umum_selalu_satu():
    """Pastikan semua fixture hanya memiliki 1 DOF."""
    for fname in ["bidang_miring_gesekan.json", "katrol_atwood.json", "gabungan_bidang_katrol.json"]:
        data = load_fixture(fname)
        assert len(data["koordinat_umum"]) == 1, f"{fname}: koordinat_umum harus tepat 1 elemen"
