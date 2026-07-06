from .inclined_plane import solve_inclined_plane
from .collision import solve_collision
from .katrol import solve_katrol
from .gerak_parabola import solve_gerak_parabola

REGISTRY = {
    "bidang_miring": solve_inclined_plane,
    "collision": solve_collision,
    "katrol": solve_katrol,
    "gerak_parabola": solve_gerak_parabola,
}

def solve(scene_type: str, known: dict) -> dict:
    if scene_type not in REGISTRY:
        raise ValueError(
            f"[ANTI-HALUSINASI] Tidak ada solver untuk scene_type '{scene_type}'. "
            f"Solver tersedia: {list(REGISTRY.keys())}. "
            f"Pipeline dihentikan — tidak menebak jawaban untuk domain yang belum diimplementasi."
        )
    return REGISTRY[scene_type](known)
