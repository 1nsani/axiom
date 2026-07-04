import subprocess
import sys
import os
import json

def main():
    print("[SYSTEM] Axiom Engine - Orchestrator")
    shared_path = "/content/drive/MyDrive/axiom_shared/known_parameters.json"
    if not os.path.exists(shared_path):
        print(f"[-] FATAL: {shared_path} tidak ditemukan.")
        sys.exit(1)
    with open(shared_path, "r") as f:
        known_data = json.load(f)
    scene_type = known_data.get("scene_type")
    known = known_data.get("known", {})
    visual_hooks = known_data.get("visual_hooks", {})
    if not scene_type or not known:
        print("[-] FATAL: known_parameters.json tidak valid.")
        sys.exit(1)
    from solvers import solve
    try:
        physics_result = solve(scene_type, known)
    except Exception as e:
        print(f"[-] Solver gagal: {e}")
        sys.exit(1)
    from bridge import build_anim_input
    anim_data = build_anim_input(known, physics_result, visual_hooks)
    from renderer import render_scene
    try:
        render_scene("anim_input.json")
        print("[+] Render selesai.")
    except Exception as e:
        print(f"[-] Render gagal: {e}")
        sys.exit(1)
    print("[SYSTEM] Selesai.")

if __name__ == "__main__":
    main()
