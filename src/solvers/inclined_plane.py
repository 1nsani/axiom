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
    W = m * g
    W_paralel = m * g * math.sin(theta)
    N = m * g * math.cos(theta)
    f_max = mu * N
    F_net = W_paralel - F_ext
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
            "W": round(W, 2),          # baru
        },
        "duration": 4.0,
    }

def generate_caption(known: dict, hasil: dict) -> str:
    a = hasil.get("percepatan", 0)
    arah = hasil.get("arah_gerak", "diam")
    f_gesek = hasil.get("gaya_gesek", 0)
    N = hasil.get("gaya_normal", 0)
    if arah == "diam":
        return (f"Balok diam karena resultan gaya sejajar bidang tidak cukup "
                f"untuk mengatasi gesekan (gaya gesek = {f_gesek:.2f} N, "
                f"gaya normal = {N:.2f} N).")
    else:
        return (f"Balok bergerak {arah} dengan percepatan {a:.2f} m/s². "
                f"Gaya gesek kinetis = {f_gesek:.2f} N, gaya normal = {N:.2f} N.")
