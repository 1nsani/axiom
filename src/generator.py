import json
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
storyboard_file = os.path.join(base_dir, "storyboard.json")
output_code_file = os.path.join(base_dir, "render.py")

if not os.path.exists(storyboard_file):
    print("[-] Error: storyboard.json tidak ditemukan!")
    exit()

with open(storyboard_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

manim_code = [
    "from manim import *",
    "",
    "class PhysicsScene(Scene):",
    "    def construct(self):"
]
indent = "        "

# 1. GENERATE OBJEK SECARA DINAMIS
for obj in data.get("setup_objects", []):
    obj_id = obj["id"]
    obj_type = obj["type"]
    color = obj["color"]
    
    if obj_type == "Square":
        manim_code.append(f"{indent}{obj_id} = Square(color={color})")
    elif obj_type == "Circle":
        radius = obj.get("radius", 0.5)
        manim_code.append(f"{indent}{obj_id} = Circle(radius={radius}, color={color})")
    elif obj_type == "Line":
        start = obj["start"]
        end = obj["end"]
        manim_code.append(f"{indent}{obj_id} = Line(start={start}, end={end}, color={color})")
    
    # Atur posisi jika ada
    if "position" in obj:
        manim_code.append(f"{indent}{obj_id}.move_to({obj['position']})")

# 2. GENERATE ANIMASI SECARA DINAMIS
for anim in data.get("animations", []):
    action = anim["action"]
    target = anim["target_id"]
    
    if action == "FadeIn":
        manim_code.append(f"{indent}self.play(FadeIn({target}))")
    elif action == "Create":
        manim_code.append(f"{indent}self.play(Create({target}))")
    elif action == "Rotate":
        angle = anim["angle"]
        point = anim["about_point"]
        manim_code.append(f"{indent}self.play(Rotate({target}, angle={angle}, about_point={point}))")

with open(output_code_file, 'w', encoding='utf-8') as f:
    f.write("\n".join(manim_code))

print("[*] Transpiler Universal Selesai Ditulis!")
