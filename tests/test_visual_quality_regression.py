import sys
import os
import json
import pytest
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from scene_dryrun import describe_scene

# Fixture: satu contoh per domain yang sudah divalidasi
DOMAIN_FIXTURES = {
    "bidang_miring": {
        "motion_type": "static_incline",
        "parameters": {"massa": 4, "sudut_permukaan": 30, "gaya_eksternal": 200, "koefisien_gesek": 0.2},
        "hasil_fisika": {"percepatan": 0.0, "gaya_normal": 34.64, "gaya_gesek": 6.93, "gaya_eksternal": 200, "W": 40},
        "vectors_to_render": [
            {"id": "W", "direction_logic": "absolute_down", "color": "RED", "label": "W", "value_ref": "W"},
            {"id": "N", "direction_logic": "perpendicular_up", "color": "YELLOW", "label": "N", "value_ref": "gaya_normal"},
            {"id": "F_ext", "direction_logic": "parallel_up", "color": "GREEN", "label": "F_{tarik}", "value_ref": "gaya_eksternal"},
            {"id": "W_sin", "direction_logic": "parallel_down", "color": "ORANGE", "label": "W_sin"},
            {"id": "W_cos", "direction_logic": "perpendicular_down", "color": "ORANGE", "label": "W_cos"},

        ]
    },
    "collision": {
        "motion_type": "collision_1d",
        "parameters": {"massa_1": 2, "massa_2": 2, "v1_awal": 5, "v2_awal": 0, "koefisien_restitusi": 1.0},
        "hasil_fisika": {"v1_akhir": 0, "v2_akhir": 5},
        "vectors_to_render": []  # collision tidak memiliki vektor gaya
    },
    "katrol": {
        "motion_type": "katrol_atwood",
        "parameters": {"massa_1": 3, "massa_2": 5},
        "hasil_fisika": {"percepatan": 2.5, "tegangan": 37.5, "W1": 30, "W2": 50},
        "vectors_to_render": [
            {"id": "T1", "direction_logic": "absolute_up", "color": "PURPLE", "label": "T_1", "value_ref": "tegangan"},
            {"id": "T2", "direction_logic": "absolute_up", "color": "PURPLE", "label": "T_2", "value_ref": "tegangan"},
            {"id": "W1", "direction_logic": "absolute_down", "color": "RED", "label": "W_1", "value_ref": "W1"},
            {"id": "W2", "direction_logic": "absolute_down", "color": "RED", "label": "W_2", "value_ref": "W2"},
        ]
    },
    "gerak_parabola": {
        "motion_type": "trajectory_2d",
        "parameters": {"v0": 20, "sudut_elevasi": 45, "gravitasi": 10, "tinggi_awal": 0},
        "hasil_fisika": {"jarak_horizontal_maks": 40.0, "tinggi_maksimum": 10.0, "waktu_di_udara": 2.83},
        "vectors_to_render": []
    }
}

# Helper: tulis fixture ke file JSON sementara
def write_fixture(domain, data):
    import tempfile
    path = os.path.join("/tmp", f"test_visual_{domain}.json")
    with open(path, "w") as f:
        json.dump(data, f)
    return path

@pytest.mark.parametrize("domain", list(DOMAIN_FIXTURES.keys()))
def test_visual_quality(domain):
    data = DOMAIN_FIXTURES[domain]
    path = write_fixture(domain, data)
    result = describe_scene(path)
    storyboard = result["storyboard"]
    bounds = result["bounds"]

    # a. Label tidak tumpang tindih
    margin = 1.5
    min_sep = 0.3  # dari resolve_label_positions
    ids = [item["id"] for item in storyboard]
    for i in range(len(storyboard)):
        for j in range(i+1, len(storyboard)):
            pos_a = np.array(storyboard[i]["label_position"])
            pos_b = np.array(storyboard[j]["label_position"])
            jarak = np.linalg.norm(pos_a - pos_b)
            assert jarak >= min_sep - 0.05, f"{domain}: label '{ids[i]}' dan '{ids[j]}' terlalu dekat ({jarak:.3f} < {min_sep})"

    # b. Semua label berada di dalam bounds + margin
    for item in storyboard:
        pos = np.array(item["label_position"])
        assert bounds["x_min"] - margin <= pos[0] <= bounds["x_max"] + margin, \
            f"{domain}: label '{item['id']}' x={pos[0]:.2f} di luar bounds ({bounds['x_min']}, {bounds['x_max']})"
        assert bounds["y_min"] - margin <= pos[1] <= bounds["y_max"] + margin, \
            f"{domain}: label '{item['id']}' y={pos[1]:.2f} di luar bounds ({bounds['y_min']}, {bounds['y_max']})"

    # c. Rasio panjang vektor sesuai magnitudo (untuk domain yang memiliki vektor)
    if domain in ("bidang_miring", "katrol"):
        magnitudes = []
        lengths = []
        for item in storyboard:
            if item.get("magnitude") is not None:
                magnitudes.append(item["magnitude"])
                lengths.append(item["arrow_length"])
        if len(magnitudes) >= 2:
            # Ambil pasangan magnitudo maks dan min
            max_idx = np.argmax(magnitudes)
            min_idx = np.argmin(magnitudes)
            # Vektor dengan magnitudo lebih besar harus lebih panjang atau sama
            assert lengths[max_idx] >= lengths[min_idx], \
                f"{domain}: magnitudo {magnitudes[max_idx]} tidak menghasilkan panjang >= {magnitudes[min_idx]}"
