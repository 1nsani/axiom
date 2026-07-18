import sympy as sp
from physics_core import elastic_collision_1d

def solve_alpha_kritis(target_jumlah_tumbukan: int) -> dict:
    alpha = sp.Symbol('alpha', positive=True)
    v = sp.Symbol('v', positive=True)

    v_kiri = sp.Integer(0)
    v_tengah = v
    v_kanan = sp.Integer(0)

    for langkah in range(target_jumlah_tumbukan):
        if langkah % 2 == 0:
            v_tengah, v_kanan = elastic_collision_1d(1, v_tengah, alpha, v_kanan)
        else:
            v_kiri, v_tengah = elastic_collision_1d(alpha, v_kiri, 1, v_tengah)

    if target_jumlah_tumbukan % 2 == 1:
        persamaan_batas = sp.Eq(v_tengah, v_kiri)
    else:
        persamaan_batas = sp.Eq(v_tengah, v_kanan)

    # Hilangkan v (cancel dari kedua sisi) dengan substitusi v=1
    persamaan_numerik = sp.Eq(
        persamaan_batas.lhs.subs(v, 1),
        persamaan_batas.rhs.subs(v, 1)
    )

    # Coba solve analitik dulu
    akar = sp.solve(persamaan_numerik, alpha)
    
    candidates = []
    if isinstance(akar, list):
        candidates = akar
    elif hasattr(akar, '__iter__'):
        try:
            candidates = list(akar)
        except:
            candidates = []
    else:
        candidates = [akar]
    
    akar_valid = []
    for a in candidates:
        try:
            val = float(a.evalf())
            if val >= 1:
                akar_valid.append((a, val))
        except:
            pass

    # Jika solve analitik gagal, gunakan nsolve numerik
    if not akar_valid:
        # Coba beberapa tebakan
        for tebakan in [2.0, 3.0, 5.0, 10.0, 20.0, 50.0, 100.0]:
            try:
                solusi_num = sp.nsolve(persamaan_numerik, alpha, tebakan, tol=1e-14, maxsteps=200)
                val = float(solusi_num)
                if val >= 1:
                    akar_valid.append((solusi_num, val))
                    break
            except:
                continue

    if akar_valid:
        akar_valid.sort(key=lambda x: x[1])
        alpha_simbolik, alpha_desimal = akar_valid[0]
    else:
        alpha_simbolik = None
        alpha_desimal = None

    return {
        "target_jumlah_tumbukan": target_jumlah_tumbukan,
        "alpha_maksimum_simbolik": alpha_simbolik,
        "alpha_maksimum_desimal": alpha_desimal,
    }
