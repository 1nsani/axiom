from manim import *
import json
import numpy as np
import os

class InclinedPlaneScene(Scene):
    def construct(self):
        # Baca data
        input_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "anim_input.json"
        )
        if not os.path.exists(input_path):
            raise FileNotFoundError("anim_input.json tidak ditemukan")

        with open(input_path, "r") as f:
            data = json.load(f)

        params = data.get("parameters", {})
        hasil_fisika = data.get("hasil_fisika", {})
        vectors = data.get("vectors_to_render", [])

        massa = params.get("massa", 1)
        theta_deg = params.get("sudut_permukaan", 30)
        percepatan = hasil_fisika.get("percepatan", 0)
        arah_gerak = hasil_fisika.get("arah_gerak", "diam")
        gaya_gesek = hasil_fisika.get("gaya_gesek", 0)

        print(f"[DEBUG] massa={massa}, sudut={theta_deg}°, a={percepatan}, arah={arah_gerak}")

        theta_rad = np.radians(theta_deg)

        # Bidang miring
        bidang = Line(ORIGIN, 7 * RIGHT).rotate(theta_rad, about_point=ORIGIN).shift(LEFT*3 + DOWN*1)
        alas = Line(bidang.get_start(), bidang.get_start() + 7 * RIGHT)
        sudut = Angle(alas, bidang, radius=0.8)
        label_sudut = Text(f"{theta_deg}°", font_size=24).next_to(sudut, RIGHT, buff=0.1)
        self.play(Create(alas), Create(bidang), run_time=1)
        self.play(Create(sudut), Write(label_sudut), run_time=0.5)

        # Balok
        v_norm = np.array([-np.sin(theta_rad), np.cos(theta_rad), 0.0])
        v_par = np.array([np.cos(theta_rad), np.sin(theta_rad), 0.0])
        balok = Square(side_length=0.8, fill_opacity=0.6, color=BLUE)
        balok.rotate(theta_rad)
        start = bidang.point_from_proportion(0.15) + 0.4 * v_norm
        balok.move_to(start)

        # HUD
        info = VGroup(
            Text(f"Massa: {massa} kg", font_size=20),
            Text(f"Percepatan: {percepatan:.2f} m/s²", font_size=20),
            Text("Status: DIAM" if arah_gerak == "diam" else "Bergerak", font_size=20, color=YELLOW if arah_gerak == "diam" else GREEN)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)
        self.play(FadeIn(balok, shift=DOWN*0.5), Write(info))

        # Gambar vektor sederhana (tanpa LaTeX)
        def simple_vector(arah, warna, teks, offset_f=0.75):
            arr = Arrow(ORIGIN, 1.5 * arah, buff=0, color=warna, stroke_width=4)
            arr.move_to(balok.get_center() + offset_f * arah)
            lbl = Text(teks, font_size=18, color=warna)
            lbl.next_to(arr.get_end(), direction=arah, buff=0.1)
            arr.add_updater(lambda m, o=offset_f, d=arah: m.move_to(balok.get_center() + o * d))
            lbl.add_updater(lambda m, a=arr, d=arah: m.next_to(a.get_end(), direction=d, buff=0.1))
            self.add(arr, lbl)
            self.play(GrowArrow(arr), Write(lbl), run_time=0.3)

        # Mapping arah
        dir_map = {
            "parallel_up": v_par, "parallel_down": -v_par,
            "perpendicular_up": v_norm, "perpendicular_down": -v_norm,
            "absolute_down": DOWN
        }
        col_map = {"GREEN": GREEN, "YELLOW": YELLOW, "RED": RED,
                   "BLUE": BLUE, "WHITE": WHITE, "ORANGE": ORANGE, "PURPLE": PURPLE}

        for v in vectors:
            logic = v.get("direction_logic")
            if logic not in dir_map:
                continue
            if v.get("id") == "F_ext" and params.get("gaya_eksternal", 0) == 0:
                continue
            d = dir_map[logic]
            c = col_map.get(v.get("color", "WHITE"), WHITE)
            label_bersih = v["label"].replace("\\vec", "").replace("{", "").replace("}", "").replace("\\", "")
            # offset disesuaikan
            if logic == "parallel_down":
                off = 0.6
            elif logic == "parallel_up":
                off = 0.8
            elif logic in ("perpendicular_up", "perpendicular_down"):
                off = 0.65
            elif logic == "absolute_down":
                off = 0.7
            else:
                off = 0.75
            simple_vector(d, c, label_bersih, offset_f=off)

        # Gaya gesek
        if gaya_gesek > 1e-6:
            if arah_gerak == "ke_atas":
                g_dir = -v_par
            elif arah_gerak == "ke_bawah":
                g_dir = v_par
            else:
                g_dir = -v_par  # default ke bawah jika diam
            simple_vector(g_dir, PURPLE, "f_gesek", offset_f=0.9)

        # Balok tetap di tempat (karena diam)
        self.wait(2)
        print("[DEBUG] Scene selesai (benda diam)")


class Collision1DScene(Scene):
    # ... tetap sama seperti sebelumnya (sudah stabil)
    def construct(self):
        input_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "anim_input.json"
        )
        with open(input_path, "r") as f:
            data = json.load(f)

        params = data["parameters"]
        hasil = data["hasil_fisika"]

        m1 = params["massa_1"]
        m2 = params["massa_2"]
        v1_awal = params["v1_awal"]
        v2_awal = params["v2_awal"]
        v1_akhir = hasil["v1_akhir"]
        v2_akhir = hasil["v2_akhir"]

        max_mass = max(m1, m2)
        size1 = 0.6 + 0.3 * (m1 / max_mass)
        size2 = 0.6 + 0.3 * (m2 / max_mass)

        balok1 = Square(side_length=size1, fill_opacity=0.6, color=BLUE).shift(LEFT * 3)
        balok2 = Square(side_length=size2, fill_opacity=0.6, color=RED).shift(RIGHT * 3)
        self.play(FadeIn(balok1), FadeIn(balok2))

        label1 = Text(f"m1={m1} kg", font_size=20).next_to(balok1, DOWN)
        label2 = Text(f"m2={m2} kg", font_size=20).next_to(balok2, DOWN)
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

        half1 = size1 / 2
        half2 = size2 / 2
        jarak_awal = 6
        jarak_sentuh = jarak_awal - (half1 + half2)
        v_rel = v1_awal - v2_awal
        if v_rel <= 0:
            raise ValueError("Kecepatan relatif tidak positif.")
        t_collision = min(jarak_sentuh / v_rel, 5)

        pos1_coll = balok1.get_center() + v1_awal * t_collision * RIGHT
        pos2_coll = balok2.get_center() + v2_awal * t_collision * RIGHT

        self.play(
            balok1.animate.move_to(pos1_coll),
            balok2.animate.move_to(pos2_coll),
            run_time=t_collision,
            rate_func=linear
        )

        self.wait(0.5)
        self.remove(v1_arrow, v1_lbl, v2_arrow, v2_lbl)

        t_after = 2
        pos1_setelah = pos1_coll + v1_akhir * t_after * RIGHT
        pos2_setelah = pos2_coll + v2_akhir * t_after * RIGHT
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
