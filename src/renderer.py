from manim import *
import json
import numpy as np
import os

class InclinedPlaneScene(Scene):
    def construct(self):
        input_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "anim_input.json"
        )
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"anim_input.json tidak ditemukan di {input_path}")

        with open(input_path, "r") as f:
            data = json.load(f)

        params = data.get("parameters", {})
        hasil_fisika = data.get("hasil_fisika", {})
        vectors = data.get("vectors_to_render", [])

        massa = params.get("massa", 1)
        theta_deg = params.get("sudut_permukaan", 30)
        percepatan = hasil_fisika.get("percepatan", 0)
        arah_gerak = hasil_fisika.get("arah_gerak", "diam")

        print(f"[DEBUG] Scene: massa={massa}, sudut={theta_deg}°, a={percepatan}, arah={arah_gerak}")

        theta_rad = np.radians(theta_deg)

        # Bidang miring
        bidang_miring = Line(ORIGIN, 7 * RIGHT).rotate(theta_rad, about_point=ORIGIN).shift(LEFT*3 + DOWN*1)
        base_line = Line(bidang_miring.get_start(), bidang_miring.get_start() + 7 * RIGHT)
        angle_arc = Angle(base_line, bidang_miring, radius=0.8)
        angle_label = Text(f"{theta_deg}°", font_size=24).next_to(angle_arc, RIGHT, buff=0.1)
        self.play(Create(base_line), Create(bidang_miring), run_time=1)
        self.play(Create(angle_arc), Write(angle_label), run_time=0.5)

        # Vektor basis
        vektor_normal = np.array([-np.sin(theta_rad), np.cos(theta_rad), 0.0])
        vektor_paralel = np.array([np.cos(theta_rad), np.sin(theta_rad), 0.0])

        # Balok
        balok = Square(side_length=0.8, fill_opacity=0.6, color=BLUE)
        balok.rotate(theta_rad)
        start_prop = 0.15
        start_point = bidang_miring.point_from_proportion(start_prop) + (0.4 * vektor_normal)
        balok.move_to(start_point)

        # HUD
        hud = VGroup(
            Text(f"Massa: {massa} kg", font_size=20),
            Text(f"Percepatan: {percepatan:.2f} m/s²", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)
        self.play(FadeIn(balok, shift=DOWN*0.5), Write(hud))

        def _draw_vector(direction, color, label_text, offset_factor=0.75):
            arah = direction
            panjang = 1.5
            arrow = Arrow(ORIGIN, panjang * arah, buff=0, color=color, stroke_width=4)
            offset = offset_factor * arah
            arrow.move_to(balok.get_center() + offset)
            label = Text(label_text, font_size=20, color=color)
            label.move_to(arrow.get_end() + 0.3 * arah)

            arrow.add_updater(lambda m, o=offset: m.move_to(balok.get_center() + o))
            label.add_updater(lambda m, p=arrow, av=arah: m.move_to(p.get_end() + 0.3 * av))

            self.add(arrow, label)
            self.play(GrowArrow(arrow), Write(label), run_time=0.4)

        direction_map = {
            "parallel_up": vektor_paralel,
            "parallel_down": -vektor_paralel,
            "perpendicular_up": vektor_normal,
            "absolute_down": DOWN,
        }
        color_map = {
            "GREEN": GREEN, "YELLOW": YELLOW, "RED": RED,
            "BLUE": BLUE, "WHITE": WHITE,
        }

        for vec in vectors:
            logic = vec.get("direction_logic")
            if logic not in direction_map:
                continue
            dir_vec = direction_map[logic]
            col = color_map.get(vec.get("color", "WHITE"), WHITE)
            label = vec.get("label", "").replace("\\", "").replace("vec", "").replace("{", "").replace("}", "")
            _draw_vector(dir_vec, col, label)

        # Gerakan balok
        if arah_gerak == "ke_bawah":
            target_prop = 0.0
        elif arah_gerak == "ke_atas":
            target_prop = 0.85
        else:
            target_prop = start_prop

        target_pos = bidang_miring.point_from_proportion(target_prop) + (0.4 * vektor_normal)

        if arah_gerak != "diam" and abs(percepatan) > 1e-6:
            run_time = max(1.0, 6.0 / (abs(percepatan) + 1))
            self.play(balok.animate.move_to(target_pos), run_time=run_time, rate_func=linear)
        else:
            self.wait(1)

        self.wait(1.5)


class Collision1DScene(Scene):
    def construct(self):
        input_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "anim_input.json"
        )
        with open(input_path, "r") as f:
            data = json.load(f)

        params = data["parameters"]
        hasil = data["hasil_fisika"]
        vectors = data.get("vectors_to_render", [])

        m1 = params["massa_1"]
        m2 = params["massa_2"]
        v1_awal = params["v1_awal"]
        v2_awal = params["v2_awal"]
        v1_akhir = hasil["v1_akhir"]
        v2_akhir = hasil["v2_akhir"]

        size1 = 0.6 + 0.3 * (m1 / max(m1, m2))
        size2 = 0.6 + 0.3 * (m2 / max(m1, m2))
        balok1 = Square(side_length=size1, fill_opacity=0.6, color=BLUE).shift(LEFT * 3)
        balok2 = Square(side_length=size2, fill_opacity=0.6, color=RED).shift(RIGHT * 3)
        self.play(FadeIn(balok1), FadeIn(balok2))

        label1 = Text(f"m1={m1}kg", font_size=20).next_to(balok1, DOWN)
        label2 = Text(f"m2={m2}kg", font_size=20).next_to(balok2, DOWN)
        self.play(Write(label1), Write(label2))

        def make_velocity_arrow(value, obj, color, label_text):
            arah = RIGHT if value >= 0 else LEFT
            panjang = abs(value) * 0.5
            arrow = Arrow(ORIGIN, arah * panjang, buff=0, color=color, stroke_width=4)
            arrow.next_to(obj, UP, buff=0.2)
            lbl = Text(f"{label_text}={value:.1f}", font_size=16, color=color).next_to(arrow, UP, buff=0.05)
            arrow.add_updater(lambda m, o=obj: m.next_to(o, UP, buff=0.2))
            lbl.add_updater(lambda m, a=arrow: m.next_to(a, UP, buff=0.05))
            return arrow, lbl

        v1_arrow, v1_lbl = make_velocity_arrow(v1_awal, balok1, GREEN, "v1")
        v2_arrow, v2_lbl = make_velocity_arrow(v2_awal, balok2, RED, "v2")
        self.play(GrowArrow(v1_arrow), Write(v1_lbl), GrowArrow(v2_arrow), Write(v2_lbl))

        if v1_awal - v2_awal <= 0:
            raise ValueError("Kecepatan relatif tidak positif.")
        t_collision = min(6.0 / (v1_awal - v2_awal), 5)
        pos1_coll = balok1.get_center() + v1_awal * t_collision * RIGHT
        pos2_coll = balok2.get_center() + v2_awal * t_collision * RIGHT
        self.play(
            balok1.animate.move_to(pos1_coll),
            balok2.animate.move_to(pos2_coll),
            run_time=t_collision,
            rate_func=linear
        )

        self.remove(v1_arrow, v1_lbl, v2_arrow, v2_lbl)

        t_after = 2
        pos1_setelah = balok1.get_center() + v1_akhir * t_after * RIGHT
        pos2_setelah = balok2.get_center() + v2_akhir * t_after * RIGHT
        self.play(
            balok1.animate.move_to(pos1_setelah),
            balok2.animate.move_to(pos2_setelah),
            run_time=t_after,
            rate_func=linear
        )

        v1f_arrow, v1f_lbl = make_velocity_arrow(v1_akhir, balok1, GREEN, "v1'")
        v2f_arrow, v2f_lbl = make_velocity_arrow(v2_akhir, balok2, RED, "v2'")
        self.play(GrowArrow(v1f_arrow), Write(v1f_lbl), GrowArrow(v2f_arrow), Write(v2f_lbl))

        self.wait(1)
