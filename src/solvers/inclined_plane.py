import math

def solve_inclined_plane(known: dict) -> dict:
    m = known.get("massa")
    theta_deg = known.get("sudut_permukaan")
    if m is None or theta_deg is None:
        raise ValueError("Parameter wajib 'massa' atau 'sudut_permukaan' tidak ada.")

    g = known.get("gravitasi", 10.0)
    mu = known.get("koefisien_gesek", 0.0)
    F_ext = known.get("gaya_eksternal", 0.0)

    theta = math.radians(theta_deg)
    W_paralel = m * g * math.sin(theta)
    N = m * g * math.cos(theta)
    f_max = mu * N

    F_net = W_paralel - F_ext   # positif = ke bawah

    # Toleransi untuk mengatasi floating point (contoh: F_net = -2e-16)
    epsilon = 1e-9
    if abs(F_net) <= f_max + epsilon:
        a = 0.0
        f_aktual = F_net if abs(F_net) <= f_max else f_max
        arah = "diam"
    else:
        f_aktual = f_max
        if F_net > 0:
            a = (F_net - f_max) / m
            arah = "ke_bawah"
        else:
            a = (F_net + f_max) / m
            arah = "ke_atas"

    return {
        "motion_type": "static_incline",
        "hasil": {
            "percepatan": round(a, 4),
            "arah_gerak": arah,
            "gaya_normal": round(N, 2),
            "gaya_gesek": round(f_aktual, 2),
            "gaya_eksternal": F_ext,
        },
        "duration": 4.0,
    }
