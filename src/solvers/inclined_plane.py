import math

def solve_inclined_plane(known: dict) -> dict:
    m = known.get("massa")
    theta_deg = known.get("sudut_permukaan")
    if m is None or theta_deg is None:
        raise ValueError("Parameter wajib 'massa' atau 'sudut_permukaan' tidak ada.")

    g = known.get("gravitasi", 10.0)
    mu = known.get("koefisien_gesek", 0.0)
    F_ext = known.get("gaya_eksternal", 0.0)   # positif = ke atas bidang

    theta = math.radians(theta_deg)
    W_paralel = m * g * math.sin(theta)        # gaya berat sejajar ke bawah
    N = m * g * math.cos(theta)                # gaya normal
    f_gesek_max = mu * N                       # gaya gesek maksimum

    # Gaya penggerak tanpa gesek: positif = ke bawah
    F_penggerak = W_paralel - F_ext

    # Tentukan arah dan percepatan
    if abs(F_penggerak) <= f_gesek_max:
        # Benda diam karena gaya penggerak tidak cukup mengatasi gesekan
        a = 0.0
        arah_gerak = "diam"
        f_gesek_aktual = F_penggerak   # gesek statis menyesuaikan
    else:
        # Benda bergerak
        if F_penggerak > 0:
            # Bergerak ke bawah, gesek ke atas
            a = (F_penggerak - f_gesek_max) / m
            arah_gerak = "ke_bawah"
        else:
            # Bergerak ke atas, gesek ke bawah
            a = (F_penggerak + f_gesek_max) / m  # F_penggerak negatif
            arah_gerak = "ke_atas"
        f_gesek_aktual = f_gesek_max  # kinetis

    return {
        "motion_type": "static_incline",
        "hasil": {
            "percepatan": round(a, 4),
            "arah_gerak": arah_gerak,
            "gaya_normal": round(N, 2),
            "gaya_gesek": round(f_gesek_aktual, 2),
        },
        "duration": 4.0,
    }
