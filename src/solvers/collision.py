def solve_collision(known: dict) -> dict:
    m1 = known.get("massa_1")
    m2 = known.get("massa_2")
    v1 = known.get("v1_awal")
    v2 = known.get("v2_awal")
    e = known.get("koefisien_restitusi", 0.0)
    if any(x is None for x in (m1, m2, v1, v2)):
        raise ValueError("Parameter massa_1, massa_2, v1_awal, v2_awal wajib diisi.")
    if v1 <= v2:
        raise ValueError("Tumbukan tidak valid: v1_awal harus > v2_awal (benda 1 mendekati benda 2).")
    total_m = m1 + m2
    v1_akhir = ((m1 - e*m2)*v1 + (1+e)*m2*v2) / total_m
    v2_akhir = ((m2 - e*m1)*v2 + (1+e)*m1*v1) / total_m
    ek_awal = 0.5*m1*v1**2 + 0.5*m2*v2**2
    ek_akhir = 0.5*m1*v1_akhir**2 + 0.5*m2*v2_akhir**2
    energi_hilang = ek_awal - ek_akhir
    return {
        "motion_type": "collision_1d",
        "hasil": {
            "v1_akhir": round(v1_akhir, 4),
            "v2_akhir": round(v2_akhir, 4),
            "energi_hilang": round(energi_hilang, 4),
        },
        "duration": 4.0,
    }

def generate_caption(known: dict, hasil: dict) -> str:
    v1, v2 = known.get("v1_awal", 0), known.get("v2_awal", 0)
    v1f, v2f = hasil["v1_akhir"], hasil["v2_akhir"]
    e_loss = hasil["energi_hilang"]
    e = known.get("koefisien_restitusi", 0)
    tipe = "elastis sempurna" if e == 1 else ("inelastis sempurna" if e == 0 else f"dengan koefisien restitusi {e}")
    return (f"Tumbukan {tipe}: benda 1 (v = {v1:.1f} m/s) dan benda 2 (v = {v2:.1f} m/s) "
            f"bertumbukan. Kecepatan akhir: v1' = {v1f:.2f} m/s, v2' = {v2f:.2f} m/s. "
            f"Energi yang hilang = {e_loss:.2f} J.")
