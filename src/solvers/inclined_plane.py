import math

def solve_inclined_plane(known: dict) -> dict:
    m = known.get("massa")
    theta_deg = known.get("sudut_permukaan")
    if m is None or theta_deg is None:
        raise ValueError("Parameter wajib 'massa' atau 'sudut_permukaan' tidak ada.")

    g = known.get("gravitasi", 10.0)
    mu = known.get("koefisien_gesek", 0.0)

    theta = math.radians(theta_deg)
    a = g * (math.sin(theta) - mu * math.cos(theta))

    arah_gerak = "ke_bawah" if a > 0 else ("ke_atas" if a < 0 else "diam")

    return {
        "motion_type": "static_incline",
        "hasil": {
            "percepatan": round(a, 4),
            "arah_gerak": arah_gerak,
        },
        "duration": 4.0,
    }
