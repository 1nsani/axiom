from .inclined_plane import solve_inclined_plane
from .collision import solve_collision

REGISTRY = {
    "bidang_miring": solve_inclined_plane,
    "collision": solve_collision,
}

def solve(scene_type, known):
    if scene_type not in REGISTRY:
        raise ValueError(f"Tidak ada solver untuk scene_type '{scene_type}'.")
    return REGISTRY[scene_type](known)
