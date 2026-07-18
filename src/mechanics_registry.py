"""
Registry untuk tipe arah gerak dan gaya dalam sistem mekanika.
Pola: registry eksplisit, gagal keras kalau tipe tidak terdaftar.
"""

import numpy as np

# --- Arah Gerak ---
def _arah_sepanjang_bidang_miring(theta_deg: float):
    """Unit vector sepanjang bidang miring (ke atas bidang)."""
    theta = np.radians(theta_deg)
    return np.array([np.cos(theta), np.sin(theta), 0.0])

def _arah_vertikal():
    """Unit vector vertikal ke atas."""
    return np.array([0.0, 1.0, 0.0])

SUPPORTED_ARAH_GERAK = {
    "sepanjang_bidang_miring": _arah_sepanjang_bidang_miring,
    "vertikal": _arah_vertikal,
}

# --- Gaya ---
def _gaya_gravitasi(benda_def: dict, sistem_def: dict) -> dict:
    """Return gaya gravitasi untuk suatu benda."""
    g = benda_def.get("parameter", {}).get("g", 10.0)
    massa = benda_def.get("massa", 1.0)
    return {
        "magnitude": massa * g,
        "arah": "absolute_down",
        "label": f"W_{benda_def['id']}",
    }

def _gaya_gesekan_kinetis(benda_def: dict, sistem_def: dict) -> dict:
    """Return gaya gesek kinetis untuk benda pada bidang miring."""
    mu = benda_def.get("parameter", {}).get("mu", 0.0)
    N = benda_def.get("parameter", {}).get("N", 0.0)
    return {
        "magnitude": mu * N,
        "arah": "parallel_down",  # berlawanan arah gerak
        "label": f"f_{benda_def['id']}",
    }

SUPPORTED_GAYA = {
    "gravitasi": _gaya_gravitasi,
    "gesekan_kinetis": _gaya_gesekan_kinetis,
}


def validate_system_def(sistem_def: dict) -> None:
    """
    Validasi sistem_def terhadap registry.
    Raise ValueError jika ada tipe yang tidak terdaftar.
    """
    for benda in sistem_def.get("benda", []):
        tipe_arah = benda.get("arah_gerak", {}).get("tipe")
        if tipe_arah not in SUPPORTED_ARAH_GERAK:
            raise ValueError(
                f"[ANTI-HALUSINASI] tipe arah_gerak '{tipe_arah}' belum terdaftar di SUPPORTED_ARAH_GERAK. "
                f"Tersedia: {list(SUPPORTED_ARAH_GERAK.keys())}"
            )

    for gaya in sistem_def.get("gaya", []):
        tipe_gaya = gaya.get("tipe")
        if tipe_gaya not in SUPPORTED_GAYA:
            raise ValueError(
                f"[ANTI-HALUSINASI] tipe gaya '{tipe_gaya}' belum terdaftar di SUPPORTED_GAYA. "
                f"Tersedia: {list(SUPPORTED_GAYA.keys())}"
            )
