def solve_katrol(known: dict) -> dict:
    m1 = known.get("massa_1")
    m2 = known.get("massa_2")
    if m1 is None or m2 is None:
        raise ValueError("Parameter 'massa_1' dan 'massa_2' wajib diisi.")
    g = known.get("gravitasi", 10.0)
    total_m = m1 + m2
    a = (m2 - m1) * g / total_m
    T = m1 * (g + a)
    W1, W2 = m1 * g, m2 * g
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
            "W1": round(W1, 2),
            "W2": round(W2, 2),
        },
        "duration": 4.0,
    }

def generate_caption(known: dict, hasil: dict) -> str:
    m1, m2 = known.get("massa_1"), known.get("massa_2")
    a = hasil["percepatan"]
    T = hasil["tegangan"]
    arah = hasil["arah_gerak"]
    if arah == "diam":
        return f"Sistem katrol seimbang: kedua massa {m1} kg dan {m2} kg sama, percepatan = 0, tegangan tali = {T:.2f} N."
    else:
        return (f"Massa {m2} kg lebih berat, sehingga sistem bergerak dengan {arah} dengan percepatan {a:.2f} m/s². "
                f"Tegangan tali = {T:.2f} N.")
