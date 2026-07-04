import json
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
storyboard_file = os.path.join(base_dir, "storyboard.json")
output_code_file = os.path.join(base_dir, "render.py")

# Baca data dengan proteksi fallback ke dictionary kosong jika file rusak/tidak ada
data = {}
if os.path.exists(storyboard_file):
    try:
        with open(storyboard_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        print("[-] Warning: storyboard.json korup.")

manim_code = [
    "from manim import *",
    "",
    "class PhysicsScene(Scene):",
    "    def construct(self):"
]
indent = "        "

has_content = False

# 1. GENERATE OBJEK
for obj in data.get("setup_objects", []):
    has_content = True
    obj_id = obj["id"]
    obj_type = obj["type"]
    color = obj["color"]
    if obj_type == "Square":
        manim_code.append(f"{indent}{obj_id} = Square(color={color})")
    elif obj_type == "Circle":
        radius = obj.get("radius", 0.5)
        manim_code.append(f"{indent}{obj_id} = Circle(radius={radius}, color={color})")
    elif obj_type == "Line":
        manim_code.append(f"{indent}{obj_id} = Line(start={obj['start']}, end={obj['end']}, color={color})")
    if "position" in obj:
        manim_code.append(f"{indent}{obj_id}.move_to({obj['position']})")

# 2. GENERATE ANIMASI
for anim in data.get("animations", []):
    has_content = True
    action = anim["action"]
    target = anim["target_id"]
    if action == "FadeIn":
        manim_code.append(f"{indent}self.play(FadeIn({target}))")
    elif action == "Create":
        manim_code.append(f"{indent}self.play(Create({target}))")
    elif action == "Rotate":
        manim_code.append(f"{indent}self.play(Rotate({target}, angle={anim['angle']}, about_point={anim['about_point']}))")

# PENYELAMAT: Jika data kosong, tulis 'pass' agar tidak IndentationError
if not has_content:
    manim_code.append(f"{indent}pass")

with open(output_code_file, 'w', encoding='utf-8') as f:
    f.write("\n".join(manim_code))

print("[*] Transpiler Defensif Selesai Diperbarui!")
