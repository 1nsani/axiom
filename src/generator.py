import json
import os

def generate_manim_code():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    storyboard_file = os.path.join(base_dir, "storyboard.json")
    output_code_file = os.path.join(base_dir, "render.py")

    # 1. Baca cetak biru adegan
    if not os.path.exists(storyboard_file):
        print("[-] Error: storyboard.json tidak ditemukan. Jalankan storyboard.py dulu.")
        return

    with open(storyboard_file, 'r', encoding='utf-8') as f:
        storyboard = json.load(f)

    # 2. Template dasar kode Manim
    manim_code = [
        "from manim import *",
        "",
        "class PhysicsScene(Scene):",
        "    def construct(self):"
    ]

    # 3. Transpilasi adegan JSON ke Python Manim
    for scene in storyboard.get("scenes", []):
        title = scene.get("title", "")
        
        # Dokumentasi internal di dalam file render
        manim_code.append(f"        # --- Scene: {title} ---")
        
        if title == "Introduce Object":
            # Hardcode bentuk awal untuk MVP
            manim_code.append("        obj = Square(color=BLUE)")
            manim_code.append("        self.play(FadeIn(obj))")
            manim_code.append("        self.wait(1)")
            
        elif title == "Apply Force":
            manim_code.append("        force_arrow = Arrow(start=LEFT, end=RIGHT, color=RED).next_to(obj, RIGHT)")
            manim_code.append("        self.play(GrowArrow(force_arrow))")
            manim_code.append("        self.wait(1)")
            
        elif title == "Show Formula":
            # Menggunakan string mentah (raw string) untuk LaTeX Manim
            manim_code.append(r"        formula = MathTex(r'F = m \cdot a').to_edge(UP)")
            manim_code.append("        self.play(Write(formula))")
            manim_code.append("        self.wait(2)")
            
        else:
            manim_code.append(f"        # Lewati aksi tidak terpetakan")

    # 4. Tulis hasil akhir ke file render.py
    with open(output_code_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(manim_code))

    print(f"[*] Translasi selesai. File kode render.py berhasil diciptakan!")

if __name__ == "__main__":
    generate_manim_code()
  
