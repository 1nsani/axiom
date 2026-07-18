import json, os, sys, glob, shutil

# Daftar domain yang menggunakan skema JSON (mechanics_schema) alih-alih solver Python
SCHEMA_DOMAINS = {
    "bidang_miring_katrol_gabungan": "/tmp/Axiom-knowledge/metadata/domain/bidang_miring_katrol_gabungan.json",
}

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
        if nama_file == "known_parameters":
            nama_file = "default"
        print(f"\n[PROSES] {nama_file}")
        with open(filepath) as f:
            data = json.load(f)
        
        scene_type = data.get("scene_type")
        known = data.get("known", {})
        visual_hooks = data.get("visual_hooks", {})
        problem_mode = data.get("problem_mode")
        
        # Cek apakah domain ini berbasis skema JSON
        if scene_type in SCHEMA_DOMAINS:
            from mechanics_builder import bangun_sistem_kanes
            from mechanics_solver import turunkan_percepatan_simbolik, substitusi_numerik
            import math
            
            skema_path = SCHEMA_DOMAINS[scene_type]
            with open(skema_path) as sf:
                skema = json.load(sf)
            
            # Update skema dengan nilai dari known_parameters
            for benda in skema["benda"]:
                if benda["massa_simbol"] in known:
                    benda["massa"] = known[benda["massa_simbol"]]
            for gaya in skema["gaya"]:
                if "mu" in gaya.get("parameter", {}) and "koefisien_gesek" in known:
                    gaya["parameter"]["mu"] = known["koefisien_gesek"]
                if "g" in gaya.get("parameter", {}) and "gravitasi" in known:
                    gaya["parameter"]["g"] = known["gravitasi"]
            
            # Bangun sistem dan hitung
            KM, ctx = bangun_sistem_kanes(skema)
            a_simbolik = turunkan_percepatan_simbolik(KM)
            
            # Siapkan parameter numerik
            nilai = {}
            for k, v in known.items():
                if k == "sudut_permukaan":
                    nilai['theta'] = math.radians(v)
                elif k == "gravitasi":
                    nilai['g'] = v
                elif k == "koefisien_gesek":
                    nilai['mu'] = v
                elif k == "massa":
                    nilai['m1'] = v
                else:
                    nilai[k] = v
            
            a_numerik = substitusi_numerik(a_simbolik, nilai, simbol_map=ctx['simbol'])
            
            physics_result = {
                "motion_type": "static_incline",
                "hasil": {
                    "percepatan": round(a_numerik, 4),
                    "arah_gerak": "ke_atas" if a_numerik < 0 else ("ke_bawah" if a_numerik > 0 else "diam"),
                },
                "duration": 4.0,
            }
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
