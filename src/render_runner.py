MOTION_TO_SCENE = {
    "storyboard": "StoryboardScene",
}

def run_render(scene_class_name, project_root):
    import subprocess, os, sys
    cmd = [sys.executable, "-m", "manim", "-ql", os.path.join(project_root, "src", "renderer.py"), scene_class_name]
    result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Manim gagal: {result.stderr}")
    video_dir = os.path.join(project_root, "media", "videos", "renderer", "480p15")
    videos = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
    return os.path.join(video_dir, sorted(videos)[-1])
