import json, os, sys, glob, shutil

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
        
        from mode_dispatch import dispatch_solve
        try:
            physics_result = dispatch_solve(scene_type, known, problem_mode)
        except Exception as e:
            ringkasan.append({"nama": nama_file, "status": "gagal_solver", "info": str(e)})
            continue
        
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
