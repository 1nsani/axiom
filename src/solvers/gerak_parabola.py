import math

def solve_gerak_parabola(known: dict) -> dict:
    v0 = known.get("v0")
    theta_deg = known.get("sudut_elevasi")
    if v0 is None or theta_deg is None:
        raise ValueError("Parameter 'v0' dan 'sudut_elevasi' wajib diisi.")
    
    g = known.get("gravitasi", 10.0)
    h0 = known.get("tinggi_awal", 0.0)
    
    theta = math.radians(theta_deg)
    v0x = v0 * math.cos(theta)
    v0y = v0 * math.sin(theta)
    
    # Waktu di udara (persamaan kuadrat lengkap)
    diskriminan = v0y**2 + 2 * g * h0
    t_total = (v0y + math.sqrt(diskriminan)) / g
    
    # Jarak horizontal maksimum
    R = v0x * t_total
    
    # Tinggi maksimum
    h_max = h0 + (v0y**2) / (2 * g)
    
    # Titik lintasan (setiap 0.1 detik)
    titik_lintasan = []
    t = 0.0
    dt = 0.1
    while t <= t_total + dt:
        x = v0x * t
        y = h0 + v0y * t - 0.5 * g * t**2
        titik_lintasan.append([x, y, 0.0])
        t += dt
    
    # Tambahkan titik akhir tepat
    if abs(t - t_total) > 0.01:
        x_end = v0x * t_total
        y_end = 0.0  # seharusnya mendekati 0
        titik_lintasan.append([x_end, y_end, 0.0])
    
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
