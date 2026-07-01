import json
import os
import sys
import numpy as np

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "trajectory.json")
    output_code_file = os.path.join(base_dir, "render.py")
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    lintasan = data["hasil_fisika"]["koordinat_animasi"]
    sudut_rad = np.deg2rad(30) # Ambil dari data solver nanti

    manim_code = [
        "from manim import *",
        "import numpy as np",
        "",
        "class PhysicsScene(Scene):",
        "    def construct(self):",
        f"        bidang = Line(start=[-3, 1.73, 0], end=[3, -1.73, 0], color=WHITE)",
        "        self.play(Create(bidang))",
        "        balok = Square(color=BLUE, side_length=0.4).rotate(-30*DEGREES)",
        f"        balok.move_to({lintasan[0]})",
        "        self.play(FadeIn(balok))",
        f"        self.play(balok.animate.move_to({lintasan[-1]}), run_time=2, rate_func=linear)",
        "        self.wait(1)"
    ]
    
    with open(output_code_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(manim_code))

if __name__ == "__main__":
    main()
    
