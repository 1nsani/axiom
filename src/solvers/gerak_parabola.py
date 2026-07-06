import math

def solve_gerak_parabola(known: dict) -> dict:
    v0 = known.get("v0")
    theta_deg = known.get("sudut_elevasi")
    if v0 is None or theta_deg is None:
        raise ValueError("Parameter 'v0' dan 'sudut_elevasi' wajib diisi.")
    g = known.get("gravitasi", 10.0)
    h0 = known.get("tinggi_awal", 0.0)
    theta = math.radians(theta_deg)
    v0x, v0y = v0 * math.cos(theta), v0 * math.sin(theta)
    diskriminan = v0y**2 + 2 * g * h0
    t_total = (v0y + math.sqrt(diskriminan)) / g
    R = v0x * t_total
    h_max = h0 + (v0y**2) / (2 * g)
    titik_lintasan = []
    t, dt = 0.0, 0.1
    while t <= t_total + dt:
        titik_lintasan.append([v0x * t, h0 + v0y * t - 0.5 * g * t**2, 0.0])
        t += dt
    if abs(t - t_total) > 0.01:
        titik_lintasan.append([v0x * t_total, 0.0, 0.0])
    return {
        "motion_type": "trajectory_2d",
        "hasil": {
            "waktu_di_udara": round(t_total, 4),
            "jarak_horizontal_maks": round(R, 2),
            "tinggi_maksimum": round(h_max, 2),
            "titik_lintasan": titik_lintasan,
        },
        "duration": 4.0,
    }

def generate_caption(known: dict, hasil: dict) -> str:
    v0 = known.get("v0")
    theta = known.get("sudut_elevasi")
    R = hasil["jarak_horizontal_maks"]
    H = hasil["tinggi_maksimum"]
    t = hasil["waktu_di_udara"]
    return (f"Proyektil ditembakkan dengan kecepatan awal {v0} m/s pada sudut {theta}°. "
            f"Jarak mendatar maksimum = {R:.2f} m, tinggi maksimum = {H:.2f} m, "
            f"waktu di udara = {t:.2f} s.")
