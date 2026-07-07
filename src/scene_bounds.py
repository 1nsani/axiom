def estimate_scene_bounds(motion_type, params, hasil):
    if motion_type == "static_incline":
        return {"x_min": -6, "x_max": 4, "y_min": -4, "y_max": 4}
    elif motion_type == "collision_1d":
        m1 = params.get("massa_1", 1)
        m2 = params.get("massa_2", 1)
        v1_akhir = hasil.get("v1_akhir", 0)
        v2_akhir = hasil.get("v2_akhir", 0)
        t_after = 2
        x1_awal, x2_awal = -3, 3
        size1 = 0.6 + 0.3 * (m1 / max(m1, m2))
        size2 = 0.6 + 0.3 * (m2 / max(m1, m2))
        half1, half2 = size1 / 2, size2 / 2
        x1_akhir = x1_awal + v1_akhir * t_after
        x2_akhir = x2_awal + v2_akhir * t_after
        points = [
            x1_awal - half1, x1_awal + half1,
            x2_awal - half2, x2_awal + half2,
            x1_akhir - half1, x1_akhir + half1,
            x2_akhir - half2, x2_akhir + half2,
        ]
        x_min = min(points) - 1.0
        x_max = max(points) + 1.0
        lebar = x_max - x_min
        tinggi = max(lebar * 9/16, 3.0)
        y_min = -tinggi/2
        y_max = tinggi/2
        return {"x_min": x_min, "x_max": x_max, "y_min": y_min, "y_max": y_max}
    elif motion_type == "katrol_atwood":
        T_animasi = 3.0
        a = hasil.get("percepatan", 0)
        displacement = min(0.5 * abs(a) * T_animasi**2, 2.5)
        y_m1_akhir = -1.0 + displacement
        y_m2_akhir = -1.0 - displacement
        ys = [-1.0, y_m1_akhir, y_m2_akhir, 2.5]
        y_min = min(ys) - 1.0
        y_max = max(ys) + 1.0
        x_min = -4.0
        x_max = 4.0
        return {"x_min": x_min, "x_max": x_max, "y_min": y_min, "y_max": y_max}
    elif motion_type == "trajectory_2d":
        return {"x_min": -6, "x_max": 6, "y_min": -3, "y_max": 5}
    else:
        return {"x_min": -7, "x_max": 7, "y_min": -4, "y_max": 4}

def apply_auto_framing(scene, motion_type, params, hasil):
    bounds = estimate_scene_bounds(motion_type, params, hasil)
    lebar = bounds["x_max"] - bounds["x_min"]
    tinggi = bounds["y_max"] - bounds["y_min"]
    margin = 1.5
    if lebar / max(tinggi, 0.1) > 16/9:
        tinggi = lebar * 9/16
    elif tinggi / max(lebar, 0.1) > 16/9:
        lebar = tinggi * 16/9
    scene.camera.frame.set(width=lebar + margin*2, height=tinggi + margin*2)
    scene.camera.frame.move_to([(bounds["x_max"]+bounds["x_min"])/2,
                                 (bounds["y_max"]+bounds["y_min"])/2, 0])
