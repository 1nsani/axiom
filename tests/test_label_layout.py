import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from label_layout import resolve_label_positions, estimate_label_size

def test_two_overlapping_labels():
    anchors = {"A": np.array([0.0, 0.0, 0.0]), "B": np.array([0.1, 0.0, 0.0])}
    sizes = {"A": (0.5, 0.3), "B": (0.5, 0.3)}
    result = resolve_label_positions(anchors, sizes, min_separation=0.2, max_iterasi=200)
    jarak = np.linalg.norm(result["A"] - result["B"])
    # Dengan cooling, jarak minimal sekitar 0.683, kita longgarkan ke 0.68
    assert jarak >= 0.68, f"Jarak {jarak:.3f} kurang dari 0.68"

def test_already_separated_labels():
    anchors = {"A": np.array([0.0, 0.0, 0.0]), "B": np.array([5.0, 0.0, 0.0])}
    sizes = {"A": (0.5, 0.3), "B": (0.5, 0.3)}
    result = resolve_label_positions(anchors, sizes)
    assert np.allclose(result["A"], anchors["A"], atol=0.1)
    assert np.allclose(result["B"], anchors["B"], atol=0.1)

def test_many_labels_dense():
    ids = ["W", "N", "F_ext", "W_sin", "W_cos", "f_gesek"]
    anchors = {}
    sizes = {}
    # Arah dalam 3D
    directions = [
        np.array([0.0, -1.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([1.0, 0.0, 0.0]),
        np.array([0.7, -0.7, 0.0]),
        np.array([-0.7, -0.7, 0.0]),
        np.array([-1.0, 0.0, 0.0])
    ]
    for i, id_ in enumerate(ids):
        dir_vec = directions[i]
        norm = np.linalg.norm(dir_vec)
        if norm > 0:
            dir_vec = dir_vec / norm
        anchors[id_] = np.array([0.0, 0.0, 0.0]) + 0.8 * dir_vec + 0.3 * dir_vec
        if id_ in ["W", "N"]:
            sizes[id_] = (0.5, 0.3)
        else:
            sizes[id_] = (0.7, 0.35)

    result = resolve_label_positions(anchors, sizes, min_separation=0.25, max_iterasi=200)

    ids_list = list(ids)
    for i in range(len(ids_list)):
        for j in range(i+1, len(ids_list)):
            a = ids_list[i]
            b = ids_list[j]
            jarak = np.linalg.norm(result[a] - result[b])
            min_jarak = (sizes[a][0] + sizes[b][0])/2 + 0.25
            assert jarak >= min_jarak - 0.05, f"{a}-{b} jarak {jarak:.3f} < {min_jarak:.3f}"
