import numpy as np

SUPPORTED_DIRECTIONS = {
    "parallel_up":       lambda theta: np.array([np.cos(theta),  np.sin(theta), 0.0]),
    "parallel_down":     lambda theta: np.array([-np.cos(theta), -np.sin(theta), 0.0]),
    "perpendicular_up":  lambda theta: np.array([-np.sin(theta), np.cos(theta), 0.0]),
    "perpendicular_down":lambda theta: np.array([np.sin(theta),  -np.cos(theta), 0.0]),
    "absolute_up":       lambda theta: np.array([0.0, 1.0, 0.0]),
    "absolute_down":     lambda theta: np.array([0.0, -1.0, 0.0]),
}

SUPPORTED_COLORS = {
    "GREEN", "YELLOW", "RED", "BLUE", "WHITE", "ORANGE", "PURPLE"
}

def vektor_normal(theta: float) -> np.ndarray:
    return np.array([-np.sin(theta), np.cos(theta), 0.0])

def vektor_paralel(theta: float) -> np.ndarray:
    return np.array([np.cos(theta), np.sin(theta), 0.0])
