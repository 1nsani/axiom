import json, os, sys, glob, shutil

ANIM_INPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "anim_input.json")

def process_one(scene_type, known, visual_hooks, nama_file):
    from solvers import solve
    try:
        physics_result = solve(scene_type, known)
    except Exception as e:
        return "gagal_solver", str(e)

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

    # Tulis ke path ABSOLUT yang sama dengan yang dibaca renderer
    with open(ANIM_INPUT_PATH, "w") as f:
        json.dump(anim_data, f, indent=4)
    print(f"[DEBUG] anim_input.json ditulis ke {ANIM_INPUT_PATH}")

    from render_runner import MOTION_TO_SCENE, run_render
    motion_type = physics_result["motion_type"]
    if motion_type not in MOTION_TO_SCENE:
        return "gagal_render", f"Motion type '{motion_type}' tidak terdaftar"

    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        video_path = run_render(MOTION_TO_SCENE[motion_type], project_root)
        # Salin video ke nama spesifik
        dest_dir = os.path.dirname(video_path)
        dest_name = f"{MOTION_TO_SCENE[motion_type]}_{nama_file}.mp4"
        dest_path = os.path.join(dest_dir, dest_name)
        shutil.copy(video_path, dest_path)
        print(f"[BATCH] Video disalin ke {dest_path}")

        from caption_exporter import export_caption
        export_caption(anim_data, dest_path)
        return "berhasil", dest_path
    except Exception as e:
        return "gagal_render", str(e)

def main():
    print("[ORCH] Axiom Engine — MODE BATCH")
    shared_dir = "/tmp/axiom_shared"

    pattern = os.path.join(shared_dir, "known_parameters_*.json")
    files = sorted(glob.glob(pattern))
    if not files:
        old = os.path.join(shared_dir, "known_parameters.json")
        if os.path.exists(old):
            files = [old]
        else:
            sys.exit("[-] Tidak ada known_parameters di " + shared_dir)

    print(f"[+] Ditemukan {len(files)} file")
    ringkasan = []
    for filepath in files:
        nama_file = os.path.basename(filepath).replace("known_parameters_", "").replace(".json", "")
        if nama_file == "known_parameters":
            nama_file = "default"
        print(f"\n[PROSES] {nama_file}")
        with open(filepath) as f:
            data = json.load(f)
        status, info = process_one(data["scene_type"], data["known"], data.get("visual_hooks", {}), nama_file)
        ringkasan.append({"nama": nama_file, "status": status, "info": info})

    print("\n" + "="*60)
    print("RINGKASAN BATCH ENGINE")
    berhasil = [r for r in ringkasan if r["status"] == "berhasil"]
    gagal = [r for r in ringkasan if r["status"] != "berhasil"]
    print(f"Total: {len(ringkasan)}, Berhasil: {len(berhasil)}, Gagal: {len(gagal)}")
    for r in gagal:
        print(f"  - {r['nama']}: {r['status']} ({r['info']})")
    print("="*60)

if __name__ == "__main__":
    main()
