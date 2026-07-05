import numpy as np

SUPPORTED_DIRECTIONS = {
    "parallel_up":        lambda bx, by: bx,
    "parallel_down":      lambda bx, by: -bx,
    "perpendicular_up":   lambda bx, by: by,
    "perpendicular_down": lambda bx, by: -by,
    "absolute_up":        lambda bx, by: np.array([0.0, 1.0, 0.0]),
    "absolute_down":      lambda bx, by: np.array([0.0, -1.0, 0.0]),
}

SUPPORTED_COLORS = {
    "GREEN", "YELLOW", "RED", "BLUE", "WHITE", "ORANGE", "PURPLE"
}

def basis_dari_sudut(theta_rad: float):
    """Kembalikan (bx, by) untuk bidang miring dengan sudut theta."""
    bx = np.array([np.cos(theta_rad), np.sin(theta_rad), 0.0])
    by = np.array([-np.sin(theta_rad), np.cos(theta_rad), 0.0])
    return bx, by

def resolve_direction(vec_def: dict, bx: np.array, by: np.array) -> np.array:
    if "angle_deg" in vec_def:
        angle = np.radians(vec_def["angle_deg"])
        return np.cos(angle) * bx + np.sin(angle) * by
    logic = vec_def.get("direction_logic")
    if logic and logic in SUPPORTED_DIRECTIONS:
        return SUPPORTED_DIRECTIONS[logic](bx, by)
    raise ValueError(
        f"[ANTI-HALUSINASI] Definisi vektor tidak valid: {vec_def}. "
        f"Harus punya 'angle_deg' (numerik) atau 'direction_logic' yang dikenal."
    )
