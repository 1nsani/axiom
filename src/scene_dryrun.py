import json
import numpy as np
from renderer_registry import SUPPORTED_DIRECTIONS, SUPPORTED_COLORS, basis_dari_sudut, resolve_direction, scale_vector_length
from label_layout import estimate_label_size, resolve_label_positions
from scene_bounds import estimate_scene_bounds

def describe_scene(anim_input_path: str) -> dict:
    with open(anim_input_path, "r") as f:
        data = json.load(f)

    params = data.get("parameters", {})
    vectors = data.get("vectors_to_render", [])
    hasil = data.get("hasil_fisika", {})
    motion_type = data.get("motion_type", "static_incline")

    theta_deg = params.get("sudut_permukaan", 30)
    theta_rad = np.radians(theta_deg)
    bx, by = basis_dari_sudut(theta_rad)

    gaya_gesek = hasil.get("gaya_gesek", 0)
    arah_gerak = hasil.get("arah_gerak", "diam")

    all_magnitudes = []
    for vec in vectors:
        ref = vec.get("value_ref")
        if ref:
            val = None
            if ref in params:
                val = params[ref]
            elif ref in hasil:
                val = hasil[ref]
            if val is not None and isinstance(val, (int, float)):
                all_magnitudes.append(abs(val))
    if gaya_gesek > 1e-6:
        all_magnitudes.append(gaya_gesek)

    temp_storyboard = []
    for vec in vectors:
        logic = vec.get("direction_logic")
        color_name = vec.get("color", "WHITE")
        if logic not in SUPPORTED_DIRECTIONS or color_name not in SUPPORTED_COLORS:
            continue
        if vec.get("id") == "F_ext" and params.get("gaya_eksternal", 0) == 0:
            continue
        try:
            dir_array = resolve_direction(vec, bx, by)
        except ValueError:
            continue

        ref = vec.get("value_ref")
        mag = None
        if ref:
            if ref in params:
                mag = abs(params[ref])
            elif ref in hasil:
                mag = abs(hasil[ref])
        if mag is not None and all_magnitudes:
            panjang = scale_vector_length(mag, all_magnitudes)
        else:
            panjang = 1.5

        off = 0.75
        if logic == "parallel_up": off = 0.8
        elif logic == "parallel_down": off = 0.6
        elif logic in ("perpendicular_up", "perpendicular_down"): off = 0.6 if logic == "perpendicular_up" else 0.7
        elif logic == "absolute_down": off = 0.7

        arrow_end = np.array([0.0, 0.0, 0.0]) + off * dir_array + panjang * dir_array
        label_anchor = arrow_end + 0.3 * dir_array

        temp_storyboard.append({
            "id": vec.get("id"),
            "direction_array": dir_array.tolist(),
            "arrow_length": panjang,
            "magnitude": mag,
            "color": color_name,
            "label": vec.get("label", ""),
            "label_anchor": label_anchor.tolist(),
        })

    if gaya_gesek > 1e-6:
        if arah_gerak == "ke_atas":
            g_logic = "parallel_down"
        elif arah_gerak == "ke_bawah":
            g_logic = "parallel_up"
        else:
            g_logic = "parallel_down"
        try:
            dir_g = resolve_direction({"direction_logic": g_logic}, bx, by)
        except ValueError:
            dir_g = -bx
        off_g = 0.9
        panjang_g = scale_vector_length(gaya_gesek, all_magnitudes) if all_magnitudes else 1.5
        arrow_end_g = np.array([0.0, 0.0, 0.0]) + off_g * dir_g + panjang_g * dir_g
        label_anchor_g = arrow_end_g + 0.3 * dir_g
        temp_storyboard.append({
            "id": "f_gesek",
            "direction_array": dir_g.tolist(),
            "arrow_length": panjang_g,
            "magnitude": gaya_gesek,
            "color": "PURPLE",
            "label": "f_{\\text{gesek}}",
            "label_anchor": label_anchor_g.tolist(),
        })

    label_anchors = {item["id"]: np.array(item["label_anchor"]) for item in temp_storyboard}
    label_sizes = {item["id"]: estimate_label_size(item["label"], 18) for item in temp_storyboard}
    final_positions = resolve_label_positions(label_anchors, label_sizes)

    storyboard = []
    xs, ys = [], []
    for item in temp_storyboard:
        pos = final_positions[item["id"]]
        item["label_position"] = pos.tolist()
        storyboard.append(item)
        xs.append(pos[0])
        ys.append(pos[1])

    # Jika ada label, hitung bounds dari posisi label, jika tidak gunakan estimate_scene_bounds
    if xs:
        margin = 1.5
        x_min = min(xs) - margin
        x_max = max(xs) + margin
        y_min = min(ys) - margin
        y_max = max(ys) + margin
        bounds = {"x_min": x_min, "x_max": x_max, "y_min": y_min, "y_max": y_max}
    else:
        bounds = estimate_scene_bounds(motion_type, params, hasil)

    return {
        "storyboard": storyboard,
        "bounds": bounds,
        "motion_type": motion_type,
    }
