def dispatch_solve(scene_type: str, known: dict, problem_mode: str = None) -> dict:
    """
    Panggil solver yang sesuai berdasarkan scene_type dan problem_mode.
    """
    if scene_type == "tumbukan_beruntun" and problem_mode == "cari_kritis":
        # Panggil solver simbolik untuk mencari alpha kritis
        from solvers.symbolic_collision import solve_alpha_kritis
        target = known.get("target_jumlah_tumbukan", 2)
        result = solve_alpha_kritis(target)
        alpha_kritis = result.get("alpha_maksimum_desimal")
        
        if alpha_kritis is None:
            raise ValueError(f"Tidak dapat menemukan alpha kritis untuk N={target}")
        
        # Panggil state machine dengan alpha sedikit di bawah kritis
        from solvers.collision_chain import simulate_collision_chain
        alpha_render = alpha_kritis - 0.05  # sedikit di bawah batas
        m = {"kiri": alpha_render, "tengah": 1, "kanan": alpha_render}
        v = {"kiri": 0, "tengah": 1, "kanan": 0}
        urut = ["kiri", "tengah", "kanan"]
        sim_result = simulate_collision_chain(v, m, urut, max_tumbukan=100)
        
        return {
            "motion_type": "tumbukan_beruntun",
            "hasil": {
                "log_tumbukan": sim_result["log_tumbukan"],
                "jumlah_tumbukan": sim_result["jumlah_tumbukan"],
                "kecepatan_akhir": sim_result["kecepatan_akhir"],
                "alpha_kritis": alpha_kritis,
                "alpha_kritis_simbolik": str(result.get("alpha_maksimum_simbolik", "")),
                "alpha_render": alpha_render,
                "massa": m,
                "kecepatan_awal": v,
                "urutan": urut,
            },
            "duration": 6.0,
        }
    elif scene_type == "tumbukan_beruntun" and problem_mode == "simulasi":
        # Mode simulasi langsung
        from solvers.collision_chain import simulate_collision_chain
        m = {
            "kiri": known.get("massa_kiri", 1),
            "tengah": known.get("massa_tengah", 1),
            "kanan": known.get("massa_kanan", 1),
        }
        v = {
            "kiri": 0,
            "tengah": known.get("kecepatan_tengah", 1),
            "kanan": 0,
        }
        urut = ["kiri", "tengah", "kanan"]
        sim_result = simulate_collision_chain(v, m, urut, max_tumbukan=100)
        
        return {
            "motion_type": "tumbukan_beruntun",
            "hasil": {
                "log_tumbukan": sim_result["log_tumbukan"],
                "jumlah_tumbukan": sim_result["jumlah_tumbukan"],
                "kecepatan_akhir": sim_result["kecepatan_akhir"],
                "massa": m,
                "kecepatan_awal": v,
                "urutan": urut,
            },
            "duration": 6.0,
        }
    else:
        # Domain lain: gunakan solver biasa
        from solvers import solve
        return solve(scene_type, known)
