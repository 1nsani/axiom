import numpy as np

def estimate_label_size(text: str, font_size: int) -> tuple:
    """Taksiran ukuran bounding box label (lebar, tinggi) dalam unit Manim."""
    lebar = 0.09 * font_size * len(text)
    tinggi = 0.15 * font_size
    return (lebar, tinggi)

def resolve_label_positions(
    label_anchors: dict,
    label_sizes: dict,
    min_separation: float = 0.3,
    max_iterasi: int = 100,
    kekuatan_pegas_kembali: float = 0.1
) -> dict:
    """
    Kembalikan posisi label yang sudah dikoreksi agar tidak bertumpuk.
    """
    posisi = {k: np.array(v, dtype=float) for k, v in label_anchors.items()}
    ids = list(posisi.keys())
    n = len(ids)
    if n < 2:
        return posisi

    for iterasi in range(max_iterasi):
        ada_tumpukan = False
        for i in range(n):
            for j in range(i+1, n):
                a = ids[i]
                b = ids[j]
                delta = posisi[a] - posisi[b]
                jarak = np.linalg.norm(delta)
                if jarak < 1e-6:
                    delta = np.array([0.001, 0.001, 0.0])
                    jarak = np.linalg.norm(delta)
                lebar_a, _ = label_sizes.get(a, (0.5, 0.3))
                lebar_b, _ = label_sizes.get(b, (0.5, 0.3))
                min_jarak = (lebar_a + lebar_b)/2 + min_separation
                if jarak < min_jarak:
                    ada_tumpukan = True
                    arah = delta / jarak
                    overlap = min_jarak - jarak
                    # Faktor skala yang menurun seiring iterasi (cooling)
                    skala = 0.5 * (1 - iterasi / max_iterasi) + 0.1
                    posisi[a] += arah * overlap * skala
                    posisi[b] -= arah * overlap * skala

        # Gaya pegas kembali ke anchor asli
        for k in ids:
            anchor = np.array(label_anchors[k], dtype=float)
            posisi[k] += (anchor - posisi[k]) * kekuatan_pegas_kembali

        if not ada_tumpukan:
            break

    return posisi
