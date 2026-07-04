import math

def solve_inclined_plane(known):
    m = known.get("massa", 1.0)
    theta_deg = known.get("sudut_permukaan", 0.0)
    g = known.get("gravitasi", 10.0)
    mu = known.get("koefisien_gesek", 0.0)
    theta = math.radians(theta_deg)
    a = g * (math.sin(theta) - mu * math.cos(theta))
    return {
        "motion_type": "static_incline",
        "hasil": {"percepatan": a, "kecepatan_akhir": None},
        "duration": 4.0
    }
