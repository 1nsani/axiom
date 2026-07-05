def solve_katrol(known: dict) -> dict:
    m1 = known.get("massa_1")
    m2 = known.get("massa_2")
    if m1 is None or m2 is None:
        raise ValueError("Parameter 'massa_1' dan 'massa_2' wajib diisi.")
    g = known.get("gravitasi", 10.0)
    total_m = m1 + m2
    a = (m2 - m1) * g / total_m  # positif = m2 turun, m1 naik
    # Tegangan tali (katrol ideal, sama di kedua sisi)
    T = m1 * (g + a)  # atau m2*(g - a), sama saja
    # Arah gerak
    if a > 1e-9:
        arah = "m2_turun"
    elif a < -1e-9:
        arah = "m1_turun"
    else:
        arah = "diam"
    return {
        "motion_type": "katrol_atwood",
        "hasil": {
            "percepatan": round(a, 4),
            "tegangan": round(T, 2),
            "arah_gerak": arah,
        },
        "duration": 4.0,
    }
