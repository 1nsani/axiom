import json
import numpy as np
from renderer_registry import SUPPORTED_DIRECTIONS, SUPPORTED_COLORS, vektor_normal, vektor_paralel

def describe_scene(anim_input_path: str) -> list:
    with open(anim_input_path, "r") as f:
        data = json.load(f)

    params = data.get("parameters", {})
    vectors = data.get("vectors_to_render", [])
    hasil = data.get("hasil_fisika", {})
    theta_deg = params.get("sudut_permukaan", 30)
    theta_rad = np.radians(theta_deg)
    gaya_gesek = hasil.get("gaya_gesek", 0)
    arah_gerak = hasil.get("arah_gerak", "diam")

    storyboard = []

    for vec in vectors:
        logic = vec.get("direction_logic")
        color_name = vec.get("color", "WHITE")
        if logic not in SUPPORTED_DIRECTIONS or color_name not in SUPPORTED_COLORS:
            continue
        if vec.get("id") == "F_ext" and params.get("gaya_eksternal", 0) == 0:
            continue
        dir_array = SUPPORTED_DIRECTIONS[logic](theta_rad)
        storyboard.append({
            "id": vec["id"],
            "direction_logic": logic,
            "color": color_name,
            "direction_array": dir_array.tolist(),
            "label": vec["label"],
            "offset_factor": 0.75,
        })

    if gaya_gesek > 1e-6:
        if arah_gerak == "ke_atas":
            g_logic = "parallel_down"
        elif arah_gerak == "ke_bawah":
            g_logic = "parallel_up"
        else:
            g_logic = "parallel_down"
        dir_g = SUPPORTED_DIRECTIONS[g_logic](theta_rad)
        storyboard.append({
            "id": "f_gesek",
            "direction_logic": g_logic,
            "color": "PURPLE",
            "direction_array": dir_g.tolist(),
            "label": "f_{\\text{gesek}}",
            "offset_factor": 0.9,
        })

    return storyboard
