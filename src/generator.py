import json
import os

# 1. TENTUKAN JALUR FILE SECARA ABSOLUT
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
storyboard_file = os.path.join(base_dir, "storyboard.json")
output_code_file = os.path.join(base_dir, "render.py")

# 2. VALIDASI KEBERADAAN DATA MASUKAN
if not os.path.exists(storyboard_file):
    print("[-] Error: storyboard.json tidak ditemukan!")
    exit()

# 3. BACA DATA STORYBOARD
with open(storyboard_file, 'r', encoding='utf-8') as f:
    storyboard = json.load(f)

# 4. TEMPLATE STRUKTUR UTAMANYA
# Di sini spasi di dalam baris kode Manim diatur secara eksplisit menggunakan '\t' atau 8 spasi
manim_code = [
    "from manim import *",
    "",
    "class PhysicsScene(Scene):",
    "    def construct(self):"
]

# spasi standar untuk blok di dalam fungsi construct() Manim
indent = "        "

# 5. TRANSPILASI LOGIKA DARI JSON KE PYTHON
for scene in storyboard.get("scenes", []):
    title = scene.get("title", "")
    manim_code.append(f"{indent}# --- Scene: {title} ---")
    
    if title == "Introduce Object":
        manim_code.append(f"{indent}obj = Square(color=BLUE)")
        manim_code.append(f"{indent}self.play(FadeIn(obj))")
        manim_code.append(f"{indent}self.wait(1)")
        
    elif title == "Apply Force":
        manim_code.append(f"{indent}force_arrow = Arrow(start=LEFT, end=RIGHT, color=RED).next_to(obj, RIGHT)")
        manim_code.append(f"{indent}self.play(GrowArrow(force_arrow))")
        manim_code.append(f"{indent}self.wait(1)")
        
    elif title == "Show Formula":
        # Menggunakan Text biasa, bukan MathTex agar 100% kebal dari error sistem LaTeX
        manim_code.append(f"{indent}formula = Text('F = m * a').to_edge(UP)")
        manim_code.append(f"{indent}self.play(Write(formula))")
        manim_code.append(f"{indent}self.wait(2)")
        
    else:
        manim_code.append(f"{indent}# No mapping for this scene")

# 6. TULIS HASIL TRANSPILASI SECARA UTUH
with open(output_code_file, 'w', encoding='utf-8') as f:
    f.write("\n".join(manim_code))

print("[*] Translasi Sukses Tanpa Celah Spasi. render.py berhasil diperbarui!")
