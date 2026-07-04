from manim import *
import json
import numpy as np
import os
import sys

class InclinedPlaneScene(Scene):
    def construct(self):
        print("[DEBUG] InclinedPlaneScene mulai")
        try:
            with open("anim_input.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("FATAL: anim_input.json tidak ditemukan.")
        print("[DEBUG] anim_input.json terbaca")

        params = data.get("parameters", {})
        hasil = data.get("hasil_fisika", {})
        vectors = data.get("vectors_to_render", [])

        massa = params.get("massa", 1)
        theta_deg = params.get("sudut_permukaan", 30)
        percepatan = hasil.get("percepatan", 0)
        arah = params.get("arah_gerak", "diam")

        print(f"[DEBUG] massa={massa}, theta={theta_deg}, a={percepatan}, arah={arah}")

        theta_rad = np.radians(theta_deg)

        # 1. Gambar bidang miring
        bidang_miring = Line(ORIGIN, 7 * RIGHT).rotate(theta_rad, about_point=ORIGIN).shift(LEFT*3 + DOWN*1)
        base_line = Line(bidang_miring.get_start(), bidang_miring.get_start() + 7 * RIGHT)
        angle_arc = Angle(base_line, bidang_miring, radius=0.8)
        angle_label = Text(f"{theta_deg}°", font_size=24).next_to(angle_arc, RIGHT, buff=0.1)

        self.play(Create(base_line), Create(bidang_miring), run_time=1)
        self.play(Create(angle_arc), Write(angle_label), run_time=0.5)

        # 2. Balok
        vektor_normal = np.array([-np.sin(theta_rad), np.cos(theta_rad), 0.0])
        vektor_paralel = np.array([np.cos(theta_rad), np.sin(theta_rad), 0.0])

        balok = Square(side_length=0.8, fill_opacity=0.6, color=BLUE)
        balok.rotate(theta_rad)
        start_point = bidang_miring.point_from_proportion(0.15) + (0.4 * vektor_normal)
        balok.move_to(start_point)

        hud_text = VGroup(
            Text(f"Massa: {massa} kg", font_size=20),
            Text(f"Percepatan: {percepatan:.2f} m/s²", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)

        self.play(FadeIn(balok, shift=DOWN*0.5), Write(hud_text))

        # 3. Vektor (pakai Text, bukan MathTex)
        color_map = {"GREEN": GREEN, "YELLOW": YELLOW, "RED": RED, "BLUE": BLUE, "WHITE": WHITE}
        for v in vectors:
            v_logic = v.get("direction_logic", "")
            v_color = color_map.get(v.get("color", "WHITE"), WHITE)
            v_label = v.get("label", "")
            # Bersihkan label dari escape LaTeX
            v_label_clean = v_label.replace("\\", "").replace("vec", "").replace("{", "").replace("}", "")
            if v_logic == "parallel_up": arah_v = vektor_paralel
            elif v_logic == "parallel_down": arah_v = -vektor_paralel
            elif v_logic == "perpendicular_up": arah_v = vektor_normal
            elif v_logic == "absolute_down": arah_v = DOWN
            else: arah_v = UP

            panah = Arrow(ORIGIN, 1.5 * arah_v, buff=0, color=v_color, stroke_width=4)
            offset = 0.75 * arah_v
            panah.move_to(balok.get_center() + offset)
            label = Text(v_label_clean, font_size=20, color=v_color)
            label.move_to(panah.get_end() + 0.3 * arah_v)

            panah.add_updater(lambda m, o=offset: m.move_to(balok.get_center() + o))
            label.add_updater(lambda m, p=panah, av=arah_v: m.move_to(p.get_end() + 0.3 * av))

            self.add(panah, label)
            self.play(GrowArrow(panah), Write(label), run_time=0.4)

        # 4. Gerakan (jika ada)
        if arah == "ke_atas":
            target_pos = bidang_miring.point_from_proportion(0.85) + (0.4 * vektor_normal)
        elif arah == "ke_bawah":
            target_pos = bidang_miring.point_from_proportion(0.0) + (0.4 * vektor_normal)
        else:
            target_pos = balok.get_center()

        if arah != "diam" and percepatan != 0:
            run_time = max(1.0, 6.0 / (abs(percepatan) + 1))
            self.play(balok.animate.move_to(target_pos), run_time=run_time, rate_func=linear)
        else:
            # Jika tidak ada gerakan, tetap tampilkan balok diam
            self.wait(1)

        self.wait(1.5)
        print("[DEBUG] Scene selesai")

class Collision1DScene(Scene):
    def construct(self):
        print("[DEBUG] Collision1DScene mulai")
        with open("anim_input.json", "r") as f:
            data = json.load(f)
        params = data.get("parameters", {})
        hasil = data.get("hasil_fisika", {})
        m1 = params.get("massa_1", 1)
        m2 = params.get("massa_2", 1)
        v1_awal = params.get("v1_awal", 2)
        v2_awal = params.get("v2_awal", -1)
        v1_akhir = hasil.get("v1_akhir", 0)
        v2_akhir = hasil.get("v2_akhir", 0)

        print(f"[DEBUG] m1={m1}, m2={m2}, v1={v1_awal}, v2={v2_awal}, v1'={v1_akhir}, v2'={v2_akhir}")

        size1 = 0.6 + 0.3 * (m1 / max(m1, m2))
        size2 = 0.6 + 0.3 * (m2 / max(m1, m2))
        balok1 = Square(side_length=size1, fill_opacity=0.6, color=BLUE)
        balok2 = Square(side_length=size2, fill_opacity=0.6, color=RED)
        balok1.shift(LEFT * 3)
        balok2.shift(RIGHT * 3)

        self.play(FadeIn(balok1), FadeIn(balok2))

        label1 = Text(f"m1={m1}kg", font_size=20).next_to(balok1, DOWN)
        label2 = Text(f"m2={m2}kg", font_size=20).next_to(balok2, DOWN)
        self.play(Write(label1), Write(label2))

        # Kecepatan awal dengan Text
        v1_arrow = Arrow(ORIGIN, v1_awal * RIGHT * 0.5, color=GREEN, buff=0)
        v1_arrow.next_to(balok1, UP, buff=0.2)
        v1_label = Text(f"v1={v1_awal:.1f}", font_size=16).next_to(v1_arrow, UP)
        v2_arrow = Arrow(ORIGIN, v2_awal * RIGHT * 0.5, color=RED, buff=0)
        v2_arrow.next_to(balok2, UP, buff=0.2)
        v2_label = Text(f"v2={v2_awal:.1f}", font_size=16).next_to(v2_arrow, UP)
        self.play(GrowArrow(v1_arrow), Write(v1_label), GrowArrow(v2_arrow), Write(v2_label))

        if v1_awal - v2_awal <= 0:
            raise ValueError("Kecepatan relatif tidak positif, tumbukan tidak terjadi.")
        t_collision = 6.0 / (v1_awal - v2_awal)
        t_collision = min(t_collision, 5)

        pos1_akhir = balok1.get_center() + v1_awal * t_collision * RIGHT
        pos2_akhir = balok2.get_center() + v2_awal * t_collision * RIGHT

        self.play(
            balok1.animate.move_to(pos1_akhir),
            balok2.animate.move_to(pos2_akhir),
            run_time=t_collision,
            rate_func=linear
        )

        t_after = 2
        pos1_setelah = balok1.get_center() + v1_akhir * t_after * RIGHT
        pos2_setelah = balok2.get_center() + v2_akhir * t_after * RIGHT

        self.play(
            balok1.animate.move_to(pos1_setelah),
            balok2.animate.move_to(pos2_setelah),
            run_time=t_after,
            rate_func=linear
        )

        # Kecepatan akhir
        v1f_arrow = Arrow(ORIGIN, v1_akhir * RIGHT * 0.5, color=GREEN, buff=0)
        v1f_arrow.next_to(balok1, UP, buff=0.2)
        v1f_label = Text(f"v1'={v1_akhir:.1f}", font_size=16).next_to(v1f_arrow, UP)
        v2f_arrow = Arrow(ORIGIN, v2_akhir * RIGHT * 0.5, color=RED, buff=0)
        v2f_arrow.next_to(balok2, UP, buff=0.2)
        v2f_label = Text(f"v2'={v2_akhir:.1f}", font_size=16).next_to(v2f_arrow, UP)
        self.play(GrowArrow(v1f_arrow), Write(v1f_label), GrowArrow(v2f_arrow), Write(v2f_label))

        self.wait(1)
        print("[DEBUG] Scene selesai")

def render_scene(input_file="anim_input.json"):
    with open(input_file, "r") as f:
        data = json.load(f)
    motion_type = data.get("motion_type")
    if motion_type == "static_incline":
        scene_class = "InclinedPlaneScene"
    elif motion_type == "collision_1d":
        scene_class = "Collision1DScene"
    else:
        raise ValueError(f"Motion type '{motion_type}' tidak dikenali.")
    import subprocess
    cmd = ["manim", "-ql", "src/renderer.py", scene_class]
    print(f"[+] Menjalankan: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=os.getcwd())
    if result.returncode != 0:
        raise RuntimeError(f"manim gagal dengan kode {result.returncode}")
    return True
