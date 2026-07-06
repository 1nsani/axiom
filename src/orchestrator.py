import json, os, sys

def main():
    print("[ORCH] Axiom Engine - Orchestrator")
    shared_path = "/tmp/axiom_shared/known_parameters.json"
    if not os.path.exists(shared_path):
        sys.exit(f"[-] FATAL: {shared_path} tidak ditemukan.")
    with open(shared_path, "r") as f:
        known_data = json.load(f)
    scene_type = known_data.get("scene_type")
    known = known_data.get("known", {})
    visual_hooks = known_data.get("visual_hooks", {})
    if not scene_type:
        sys.exit("[-] FATAL: scene_type tidak ada di known_parameters.json.")
    from solvers import solve
    try:
        physics_result = solve(scene_type, known)
        print(f"[ORCH] physics_result: {json.dumps(physics_result, indent=2)}")
    except Exception as e:
        sys.exit(f"[-] Solver gagal: {e}")

    # Generate caption
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
    except Exception as e:
        print(f"[WARN] Tidak dapat membuat caption: {e}")

    anim_data = {
        "motion_type": physics_result["motion_type"],
        "parameters": known,
        "hasil_fisika": physics_result["hasil"],
        "vectors_to_render": visual_hooks.get("vectors_template", []),
        "caption": caption,
    }
    with open("anim_input.json", "w") as f:
        json.dump(anim_data, f, indent=4)
    print("[ORCH] anim_input.json ditulis.")

    from render_runner import MOTION_TO_SCENE, run_render
    motion_type = physics_result["motion_type"]
    if motion_type not in MOTION_TO_SCENE:
        sys.exit(f"[-] Tidak ada Scene terdaftar untuk motion_type '{motion_type}'.")
    scene_class = MOTION_TO_SCENE[motion_type]
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        video_path = run_render(scene_class, project_root)
        print(f"[ORCH] Selesai. Video: {video_path}")
        # Ekspor caption ke file .md di samping video
        from caption_exporter import export_caption
        export_caption(anim_data, video_path)
    except Exception as e:
        sys.exit(f"[-] Render gagal: {e}")

if __name__ == "__main__":
    main()
