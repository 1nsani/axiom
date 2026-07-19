import json, os, sys, glob, shutil

AXIOM_KNOWLEDGE_PATH = os.environ.get("AXIOM_KNOWLEDGE_PATH", "/tmp/Axiom-knowledge")

SCHEMA_DOMAINS = {
    "bidang_miring_katrol_gabungan": os.path.join(AXIOM_KNOWLEDGE_PATH, "metadata/domain/bidang_miring_katrol_gabungan.json"),
}

def map_known_to_nilai(known, skema):
    """Petakan known_parameters ke dict nilai untuk substitusi numerik."""
    import math
    nilai = {}
    for k, v in known.items():
        if k == "sudut_permukaan":
            nilai['theta'] = math.radians(v)
        elif k == "gravitasi":
            nilai['g'] = v
        elif k == "koefisien_gesek":
            nilai['mu'] = v
        else:
            nilai[k] = v
    
    # Petakan massa: "massa" -> m1, "massa_2" -> m2, dst.
    for i, benda in enumerate(skema["benda"], start=1):
        key_massa = "massa" if i == 1 else f"massa_{i}"
        if key_massa in known:
            nilai[benda["massa_simbol"]] = known[key_massa]
    
    return nilai

def main():
    print("[ORCH] Axiom Engine — MODE BATCH")
    shared_dir = "/tmp/axiom_shared"
    
    pattern = os.path.join(shared_dir, "known_parameters_*.json")
    files = sorted(glob.glob(pattern))
    if not files:
        old = os.path.join(shared_dir, "known_parameters.json")
        if os.path.exists(old):
            files = [old]
    
    print(f"[+] Ditemukan {len(files)} file")
    ringkasan = []
    for filepath in files:
        nama_file = os.path.basename(filepath).replace("known_parameters_", "").replace(".json", "")
        if nama_file == "known_parameters": nama_file = "default"
        print(f"\n[PROSES] {nama_file}")
        with open(filepath) as f:
            data = json.load(f)
        
        scene_type = data.get("scene_type")
        known = data.get("known", {})
        visual_hooks = data.get("visual_hooks", {})
        problem_mode = data.get("problem_mode")
        
        if scene_type in SCHEMA_DOMAINS:
            from mechanics_builder import bangun_sistem_kanes
            from mechanics_solver import turunkan_percepatan_simbolik, substitusi_numerik
            from mechanics_bridge import mechanics_result_ke_hasil_fisika, build_vectors_from_skema
            
            skema_path = SCHEMA_DOMAINS[scene_type]
            with open(skema_path) as sf:
                skema = json.load(sf)
            
            # Update skema dengan known parameters (untuk backward compatibility)
            for benda in skema["benda"]:
                if benda["massa_simbol"] in known:
                    benda["massa"] = known[benda["massa_simbol"]]
            for gaya in skema["gaya"]:
                if "mu" in gaya.get("parameter", {}) and "koefisien_gesek" in known:
                    gaya["parameter"]["mu"] = known.get("koefisien_gesek", 0)
                if "g" in gaya.get("parameter", {}) and "gravitasi" in known:
                    gaya["parameter"]["g"] = known.get("gravitasi", 10)
            
            KM, ctx = bangun_sistem_kanes(skema)
            a_simbolik = turunkan_percepatan_simbolik(KM)
            
            nilai = map_known_to_nilai(known, skema)
            a_numerik = substitusi_numerik(a_simbolik, nilai, simbol_map=ctx['simbol'])
            hasil_fisika = mechanics_result_ke_hasil_fisika(skema, a_numerik)
            vectors = build_vectors_from_skema(skema)
            
            # BUG 4: motion_type berdasarkan jumlah benda
            n_benda = len(skema["benda"])
            motion_type = "static_incline" if n_benda == 1 else "sistem_gabungan_2benda"
            
            physics_result = {
                "motion_type": motion_type,
                "hasil": hasil_fisika,
                "duration": 4.0,
            }
            visual_hooks["vectors_template"] = vectors
            
        elif scene_type == "tumbukan_beruntun":
            from mode_dispatch import dispatch_solve
            physics_result = dispatch_solve(scene_type, known, problem_mode)
        else:
            from solvers import solve
            physics_result = solve(scene_type, known)
        
        anim_data = {
            "motion_type": physics_result["motion_type"],
            "parameters": known,
            "hasil_fisika": physics_result["hasil"],
            "vectors_to_render": visual_hooks.get("vectors_template", []),
        }
        with open("anim_input.json", "w") as f:
            json.dump(anim_data, f, indent=4)
        
        from render_runner import MOTION_TO_SCENE, run_render
        motion_type = physics_result["motion_type"]
        if motion_type not in MOTION_TO_SCENE:
            ringkasan.append({"nama": nama_file, "status": "gagal", "info": f"Motion type '{motion_type}' tidak terdaftar"})
            continue
        
        try:
            video_path = run_render(MOTION_TO_SCENE[motion_type], os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            dest_name = f"{MOTION_TO_SCENE[motion_type]}_{nama_file}.mp4"
            dest_path = os.path.join(os.path.dirname(video_path), dest_name)
            shutil.copy(video_path, dest_path)
            ringkasan.append({"nama": nama_file, "status": "berhasil", "info": dest_path})
        except Exception as e:
            ringkasan.append({"nama": nama_file, "status": "gagal_render", "info": str(e)})
    
    print("\n" + "="*60)
    berhasil = [r for r in ringkasan if r["status"] == "berhasil"]
    gagal = [r for r in ringkasan if r["status"] != "berhasil"]
    print(f"Total: {len(ringkasan)}, Berhasil: {len(berhasil)}, Gagal: {len(gagal)}")
    for r in gagal:
        print(f"  - {r['nama']}: {r['status']} ({r['info']})")

if __name__ == "__main__":
    main()
