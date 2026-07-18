DOMAIN_KEYWORDS = {
    "bidang_miring": ["bidang miring"],
    "collision": ["tumbukan dua benda", "bertumbukan dua", "momentum dua"],
    "katrol": ["katrol", "pulley", "atwood"],
    "gerak_parabola": ["parabola", "peluru", "proyektil", "elevasi"],
    "tumbukan_beruntun": ["tiga benda", "berjajar", "beruntun", "berantai", "tumbukan beruntun"],
}

KRITIS_KEYWORDS = ["nilai maksimum", "nilai minimum", "agar", "supaya terjadi tepat", "tepat", "kritis"]

DEFAULT_DOMAIN = "translasi"

def analyze_physics_problem(problem_text: str) -> dict:
    text = problem_text.lower()
    domain = DEFAULT_DOMAIN
    for domain_name, kw_list in DOMAIN_KEYWORDS.items():
        if any(kw in text for kw in kw_list):
            domain = domain_name
            break

    hukum_terkait = ["Hukum_Newton_2"]
    if domain in ("collision", "tumbukan_beruntun"):
        hukum_terkait.append("Hukum_Kekekalan_Momentum")

    problem_mode = "simulasi"
    if domain == "tumbukan_beruntun":
        if any(kw in text for kw in KRITIS_KEYWORDS):
            problem_mode = "cari_kritis"

    return {
        "domain": domain,
        "problem_mode": problem_mode if domain == "tumbukan_beruntun" else None,
        "hukum_terkait": hukum_terkait,
    }
