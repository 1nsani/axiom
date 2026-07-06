import os

def export_caption(anim_data: dict, video_path: str) -> str:
    """Tulis caption sebagai file .md di folder yang sama dengan video."""
    caption = anim_data.get("caption", "")
    if not caption:
        print("[CAPTION] Tidak ada caption untuk diekspor.")
        return ""
    md_path = video_path.replace(".mp4", ".md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(caption)
    print(f"[CAPTION] Caption diekspor ke {md_path}")
    return md_path
