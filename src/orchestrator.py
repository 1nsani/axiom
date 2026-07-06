import json, os, sys, glob

def process_one(scene_type, known, visual_hooks, nama_file):
    """Proses satu known_parameters, kembalikan (status, alasan)."""
    from solvers import solve
    try:
        physics_result = solve(scene_type, known)
    except Exception as e:
        return "gagal_solver", str(e)
    
    # Buat caption
    caption = ""
    try:
        if scene_type == "bidang_miring":
            from solvers.inclined_plane import generate_caption
            caption = generate_caption(known, physics_result["hasil"])
        elif scene_type == "collision":
            from solvers.collision import generate_caption
            caption = generate_caption(known, physics_result["hasil"])
        elif scene_type == "katrol":
            from solvers.katrol import generate_caption
            caption = generate_caption(known, physics_result["hasil"])
        elif scene_type == "gerak_parabola":
            from solvers.gerak_parabola import generate_caption
            caption = generate_caption(known, physics_result["hasil"])
    except Exception:
        pass
    
    anim_data = {
        "motion_type": physics_result["motion_type"],
        "parameters": known,
        "hasil_fisika": physics_result["hasil"],
        "vectors_to_render": visual_hooks.get("vectors_template", []),
        "caption": caption,
    }
    
    # Tulis anim_input khusus
    anim_path = f"anim_input_{nama_file}.json"
    with open(anim_path, "w") as f:
        json.dump(anim_data, f, indent=4)
    
    # Render
    from render_runner import MOTION_TO_SCENE, run_render
    motion_type = physics_result["motion_type"]
    if motion_type not in MOTION_TO_SCENE:
        return "gagal_render", f"Motion type '{motion_type}' tidak terdaftar"
    
    try:
        video_path = run_render(MOTION_TO_SCENE[motion_type], os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # Ekspor caption
        from caption_exporter import export_caption
        export_caption(anim_data, video_path)
        return "berhasil", video_path
    except Exception as e:
        return "gagal_render", str(e)

def main():
    print("[ORCH] Axiom Engine — MODE BATCH")
    shared_dir = "/tmp/axiom_shared"
    
    # Cari semua file known_parameters_*.json
    pattern = os.path.join(shared_dir, "known_parameters_*.json")
    files = sorted(glob.glob(pattern))
    
    if not files:
        print(f"[-] Tidak ada file known_parameters_*.json di {shared_dir}")
        print("[INFO] Jalankan Brain dulu untuk menghasilkan file.")
        # Fallback ke file lama jika ada
        old_file = os.path.join(shared_dir, "known_parameters.json")
        if os.path.exists(old_file):
            print("[INFO] Menggunakan known_parameters.json sebagai fallback.")
            files = [old_file]
        else:
            sys.exit(1)
    
    print(f"[+] Ditemukan {len(files)} file known_parameters")
    
    ringkasan = []
    for filepath in files:
        nama_file = os.path.basename(filepath).replace("known_parameters_", "").replace(".json", "")
        if nama_file == "known_parameters":  # fallback
            nama_file = "default"
        
        print(f"\n[PROSES] {nama_file}")
        with open(filepath, "r") as f:
            data = json.load(f)
        
        scene_type = data.get("scene_type")
        known = data.get("known", {})
        visual_hooks = data.get("visual_hooks", {})
        
        if not scene_type:
            ringkasan.append({"nama": nama_file, "status": "gagal", "alasan": "scene_type kosong"})
            continue
        
        status, info = process_one(scene_type, known, visual_hooks, nama_file)
        ringkasan.append({"nama": nama_file, "status": status, "info": info})
    
    # Ringkasan akhir
    print("\n" + "="*60)
    print("RINGKASAN BATCH ENGINE")
    print("="*60)
    berhasil = [r for r in ringkasan if r["status"] == "berhasil"]
    gagal = [r for r in ringkasan if r["status"] != "berhasil"]
    print(f"Total: {len(ringkasan)} soal")
    print(f"Berhasil: {len(berhasil)} video")
    print(f"Gagal: {len(gagal)}")
    for r in gagal:
        print(f"  - {r['nama']}: {r['status']} ({r['info']})")
    print("="*60)

if __name__ == "__main__":
    main()
