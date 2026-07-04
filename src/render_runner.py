import subprocess
import json
import os
import sys

MOTION_TO_SCENE = {
    "static_incline": "InclinedPlaneScene",
    "collision_1d": "Collision1DScene",
}

def run_render(scene_class_name: str, project_root: str) -> str:
    cmd = [
        sys.executable, "-m", "manim",
        "-ql",
        os.path.join(project_root, "src", "renderer.py"),
        scene_class_name,
    ]
    print(f"[RENDER] Menjalankan: {' '.join(cmd)}")

    result = subprocess.run(
        cmd,
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    log_path = os.path.join(project_root, "manim_log.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=== STDOUT ===\n" + result.stdout + "\n=== STDERR ===\n" + result.stderr)
    print(f"[RENDER] Log manim disimpan ke {log_path}")

    if result.returncode != 0:
        raise RuntimeError(f"Manim gagal (kode {result.returncode}). Cek {log_path}")

    video_dir = os.path.join(project_root, "media", "videos", "renderer", "480p15")
    if not os.path.isdir(video_dir):
        raise RuntimeError(f"Folder video {video_dir} tidak ditemukan.")
    videos = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
    if not videos:
        raise RuntimeError(f"Tidak ada file .mp4 di {video_dir}.")
    video_path = os.path.join(video_dir, sorted(videos)[-1])
    print(f"[RENDER] Video ditemukan: {video_path}")
    return video_path
