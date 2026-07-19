"""
Registry untuk tipe arah gerak dan gaya dalam sistem mekanika.
Semua fungsi mengembalikan sympy vector.
"""

def _arah_sepanjang_bidang_miring(N):
    from sympy import symbols, sin, cos
    theta = symbols('theta', positive=True)
    return cos(theta) * N.x - sin(theta) * N.y

def _arah_vertikal(N):
    return -N.y

SUPPORTED_ARAH_GERAK = {
    "sepanjang_bidang_miring": _arah_sepanjang_bidang_miring,
    "vertikal": _arah_vertikal,
}

def _gaya_gravitasi(benda_def, sistem_def, N, titik_map):
    from sympy import symbols
    g = symbols('g', positive=True)
    m = symbols(benda_def.get("massa_simbol", "m"), positive=True)
    titik = titik_map[benda_def["id"]]
    return (titik, -m * g * N.y)

def _gaya_gesekan_kinetis(benda_def, sistem_def, N, titik_map):
    from sympy import symbols, cos
    mu = symbols('mu', positive=True)
    m = symbols(benda_def.get("massa_simbol", "m"), positive=True)
    g = symbols('g', positive=True)

    tipe_arah = benda_def["arah_gerak"]["tipe"]
    arah_gerak = SUPPORTED_ARAH_GERAK[tipe_arah](N)
    
    # BUG 1 FIX: kalikan dengan tanda dari skema agar arah gesekan melawan gerak SEBENARNYA
    tanda = benda_def["arah_gerak"].get("tanda", 1)
    arah_gerak_bertanda = tanda * arah_gerak

    param = benda_def["arah_gerak"].get("parameter", {})
    if "sudut" in param:
        theta = symbols('theta', positive=True)
        normal = m * g * cos(theta)
    else:
        normal = m * g

    titik = titik_map[benda_def["id"]]
    return (titik, -mu * normal * arah_gerak_bertanda)

SUPPORTED_GAYA = {
    "gravitasi": _gaya_gravitasi,
    "gesekan_kinetis": _gaya_gesekan_kinetis,
}

def validate_system_def(sistem_def: dict) -> None:
    for benda in sistem_def.get("benda", []):
        tipe_arah = benda.get("arah_gerak", {}).get("tipe")
        if tipe_arah not in SUPPORTED_ARAH_GERAK:
            raise ValueError(f"[ANTI-HALUSINASI] tipe arah_gerak '{tipe_arah}' belum terdaftar.")
    for gaya in sistem_def.get("gaya", []):
        tipe_gaya = gaya.get("tipe")
        if tipe_gaya not in SUPPORTED_GAYA:
            raise ValueError(f"[ANTI-HALUSINASI] tipe gaya '{tipe_gaya}' belum terdaftar.")
