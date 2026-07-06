from manim import *
import json, numpy as np, os, re
from renderer_registry import (
    SUPPORTED_DIRECTIONS, SUPPORTED_COLORS,
    resolve_direction, basis_dari_sudut
)

MANIM_COLORS = {
    "GREEN": GREEN, "YELLOW": YELLOW, "RED": RED,
    "BLUE": BLUE, "WHITE": WHITE, "ORANGE": ORANGE, "PURPLE": PURPLE,
}

def _latex_to_plain(latex_str: str) -> str:
    s = latex_str.replace("\\vec", "").replace("\\", "")
    return re.sub(r"[{}]", "", s)

def make_label(latex_str: str, color, font_size=20):
    try:
        lbl = MathTex(latex_str, color=color)
        lbl.scale(font_size / 24)
        return lbl
    except Exception as e:
        plain = _latex_to_plain(latex_str)
        print(f"[WARN] MathTex gagal untuk '{latex_str}', fallback Text: '{plain}' ({e})")
        return Text(plain, font_size=font_size, color=color)

class InclinedPlaneScene(Scene):
    def construct(self):
        input_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "anim_input.json")
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"anim_input.json tidak ditemukan di {input_path}")

        with open(input_path, "r") as f:
            data = json.load(f)

        params = data.get("parameters", {})
        hasil_fisika = data.get("hasil_fisika", {})
        vectors = data.get("vectors_to_render", [])

        massa = params.get("massa", 1)
        theta_deg = params.get("sudut_permukaan", 30)
        theta_rad = np.radians(theta_deg)
        percepatan = hasil_fisika.get("percepatan", 0)
        arah_gerak = hasil_fisika.get("arah_gerak", "diam")
        gaya_gesek = hasil_fisika.get("gaya_gesek", 0)

        print(f"[DEBUG] Scene: massa={massa}, sudut={theta_deg}°, a={percepatan}, arah={arah_gerak}")

        # Basis lokal
        bx, by = basis_dari_sudut(theta_rad)

        # Gambar bidang miring
        bidang_miring = Line(ORIGIN, 7 * RIGHT).rotate(theta_rad, about_point=ORIGIN).shift(LEFT*3 + DOWN*1)
        base_line = Line(bidang_miring.get_start(), bidang_miring.get_start() + 7 * RIGHT)
        angle_arc = Angle(base_line, bidang_miring, radius=0.8)
        angle_label = Text(f"{theta_deg}°", font_size=24).next_to(angle_arc, RIGHT, buff=0.1)
        self.play(Create(base_line), Create(bidang_miring), run_time=1)
        self.play(Create(angle_arc), Write(angle_label), run_time=0.5)

        # Balok
        balok = Square(side_length=0.8, fill_opacity=0.6, color=BLUE)
        balok.rotate(theta_rad)
        start_prop = 0.15
        start_point = bidang_miring.point_from_proportion(start_prop) + (0.4 * by)
        balok.move_to(start_point)

        # HUD
        hud = VGroup(
            Text(f"Massa: {massa} kg", font_size=20),
            Text(f"Percepatan: {percepatan:.2f} m/s²", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)
        self.play(FadeIn(balok, shift=DOWN*0.5), Write(hud))

        def _draw_vector(direction, color, tex_label, offset_factor=0.75):
            arah = direction
            panjang = 1.5
            arrow = Arrow(ORIGIN, panjang * arah, buff=0, color=color, stroke_width=4)
            offset = offset_factor * arah
            arrow.move_to(balok.get_center() + offset)
            lbl = make_label(tex_label, color, font_size=18)
            lbl.move_to(arrow.get_end() + 0.3 * arah)

            arrow.add_updater(lambda m, o=offset: m.move_to(balok.get_center() + o))
            lbl.add_updater(lambda m, p=arrow, av=arah: m.move_to(p.get_end() + 0.3 * av))

            self.add(arrow, lbl)
            self.play(GrowArrow(arrow), Write(lbl), run_time=0.4)

        # Gambar vektor dari metadata
        for vec in vectors:
            if vec.get("id") == "F_ext" and params.get("gaya_eksternal", 0) == 0:
                continue
            try:
                dir_vec = resolve_direction(vec, bx, by)
            except ValueError as e:
                print(f"[SKIP] {e}")
                continue

            color_name = vec.get("color", "WHITE")
            if color_name not in SUPPORTED_COLORS:
                print(f"[SKIP] color '{color_name}' tidak didukung")
                continue
            col = MANIM_COLORS[color_name]

            # Atur offset
            off = 0.75
            logic = vec.get("direction_logic")
            if logic == "parallel_up":
                off = 0.8
            elif logic == "parallel_down":
                off = 0.6
            elif logic in ("perpendicular_up", "perpendicular_down"):
                off = 0.6 if logic == "perpendicular_up" else 0.7
            elif logic == "absolute_down":
                off = 0.7

            _draw_vector(dir_vec, col, vec["label"], offset_factor=off)

        # Gaya gesek
        if gaya_gesek > 1e-6:
            if arah_gerak == "ke_atas":
                logic = "parallel_down"
            elif arah_gerak == "ke_bawah":
                logic = "parallel_up"
            else:
                logic = "parallel_down"
            try:
                gesek_dir = resolve_direction({"direction_logic": logic}, bx, by)
            except ValueError:
                gesek_dir = -bx
            _draw_vector(gesek_dir, PURPLE, "f_{\\text{gesek}}", offset_factor=0.9)

        # Gerakan
        if arah_gerak == "ke_bawah":
            target_prop = 0.0
        elif arah_gerak == "ke_atas":
            target_prop = 0.85
        else:
            target_prop = start_prop

        target_pos = bidang_miring.point_from_proportion(target_prop) + (0.4 * by)

        if arah_gerak != "diam" and abs(percepatan) > 1e-6:
            run_time = max(1.0, 6.0 / (abs(percepatan) + 1))
            self.play(balok.animate.move_to(target_pos), run_time=run_time, rate_func=linear)
        else:
            self.wait(1)
        self.wait(1.5)


class Collision1DScene(Scene):
    def construct(self):
        input_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "anim_input.json")
        with open(input_path, "r") as f:
            data = json.load(f)

        params = data["parameters"]
        hasil = data["hasil_fisika"]

        m1, m2 = params["massa_1"], params["massa_2"]
        v1_awal, v2_awal = params["v1_awal"], params["v2_awal"]
        v1_akhir, v2_akhir = hasil["v1_akhir"], hasil["v2_akhir"]

        max_mass = max(m1, m2)
        size1, size2 = 0.6 + 0.3 * (m1 / max_mass), 0.6 + 0.3 * (m2 / max_mass)

        balok1 = Square(side_length=size1, fill_opacity=0.6, color=BLUE).shift(LEFT * 3)
        balok2 = Square(side_length=size2, fill_opacity=0.6, color=RED).shift(RIGHT * 3)
        self.play(FadeIn(balok1), FadeIn(balok2))

        label1 = Text(f"m1={m1} kg", font_size=20).next_to(balok1, DOWN)
        label2 = Text(f"m2={m2} kg", font_size=20).next_to(balok2, DOWN)
        self.play(Write(label1), Write(label2))

        def make_velocity_arrow(value, obj, color, tex_label):
            arah = RIGHT if value >= 0 else LEFT
            panjang = abs(value) * 0.5
            arrow = Arrow(ORIGIN, arah * panjang, buff=0, color=color, stroke_width=4)
            arrow.next_to(obj, UP, buff=0.2)
            lbl = make_label(f"{tex_label}={value:.1f}", color, font_size=16)
            lbl.next_to(arrow, UP, buff=0.05)
            arrow.add_updater(lambda m, o=obj: m.next_to(o, UP, buff=0.2))
            lbl.add_updater(lambda m, a=arrow: m.next_to(a, UP, buff=0.05))
            return arrow, lbl

        v1_arrow, v1_lbl = make_velocity_arrow(v1_awal, balok1, GREEN, "v_1")
        v2_arrow, v2_lbl = make_velocity_arrow(v2_awal, balok2, RED, "v_2")
        self.play(GrowArrow(v1_arrow), Write(v1_lbl), GrowArrow(v2_arrow), Write(v2_lbl))

        half1, half2 = size1 / 2, size2 / 2
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
            run_time=t_collision, rate_func=linear
        )

        self.wait(0.5)
        self.remove(v1_arrow, v1_lbl, v2_arrow, v2_lbl)

        t_after = 2
        pos1_setelah = pos1_coll + v1_akhir * t_after * RIGHT
        pos2_setelah = pos2_coll + v2_akhir * t_after * RIGHT
        self.play(
            balok1.animate.move_to(pos1_setelah),
            balok2.animate.move_to(pos2_setelah),
            run_time=t_after, rate_func=linear
        )

        v1f_arrow, v1f_lbl = make_velocity_arrow(v1_akhir, balok1, GREEN, "v'_1")
        v2f_arrow, v2f_lbl = make_velocity_arrow(v2_akhir, balok2, RED, "v'_2")
        self.play(GrowArrow(v1f_arrow), Write(v1f_lbl), GrowArrow(v2f_arrow), Write(v2f_lbl))

        self.wait(1)
























class AtwoodMachineScene(Scene):
    def construct(self):
        import json, os, numpy as np
        input_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "anim_input.json")
        if not os.path.exists(input_path):
            raise FileNotFoundError("anim_input.json tidak ditemukan")
        with open(input_path, "r") as f:
            data = json.load(f)
        params = data.get("parameters", {})
        hasil = data.get("hasil_fisika", {})
        vectors = data.get("vectors_to_render", [])

        m1 = params.get("massa_1", 1)
        m2 = params.get("massa_2", 1)
        a = hasil.get("percepatan", 0)
        T = hasil.get("tegangan", 0)
        arah = hasil.get("arah_gerak", "diam")

        self.camera.background_color = "#1e1e1e"

        # Katrol
        pulley_center = UP * 2.5
        katrol = Circle(radius=0.6, color=WHITE, stroke_width=4).move_to(pulley_center)
        penyangga = Line(pulley_center + UP*0.4, pulley_center + UP*1.5, color=GREY, stroke_width=4)
        self.play(Create(katrol), Create(penyangga))

        # Titik singgung tali
        left_rope_end = pulley_center + LEFT * 0.6 + DOWN * 0.05
        right_rope_end = pulley_center + RIGHT * 0.6 + DOWN * 0.05

        # Posisi awal balok
        m1_start_y = -1.0
        m2_start_y = -1.0
        m1_start = np.array([left_rope_end[0], m1_start_y, 0])
        m2_start = np.array([right_rope_end[0], m2_start_y, 0])

        # Garis nol (y = -1.0)
        zero_line_y = m1_start_y
        zero_line = DashedLine(LEFT*5 + UP*zero_line_y, RIGHT*5 + UP*zero_line_y, color=GREY, dash_length=0.2)
        zero_label = Text("y = 0", font_size=18, color=GREY).next_to(zero_line, RIGHT, buff=0.2)
        self.add(zero_line, zero_label)

        # Balok
        side_length = 0.8
        m1_sq = Square(side_length=side_length, fill_opacity=0.9, color=BLUE, stroke_color=WHITE, stroke_width=2).move_to(m1_start)
        m2_sq = Square(side_length=side_length, fill_opacity=0.9, color=RED, stroke_color=WHITE, stroke_width=2).move_to(m2_start)

        label_m1 = Text(f"m1={m1}kg", font_size=22, color=WHITE).next_to(m1_sq, LEFT, buff=0.4)
        label_m2 = Text(f"m2={m2}kg", font_size=22, color=WHITE).next_to(m2_sq, RIGHT, buff=0.4)
        self.play(FadeIn(m1_sq), FadeIn(m2_sq), Write(label_m1), Write(label_m2))

        # Tali
        tali_kiri = Line(left_rope_end, m1_sq.get_top(), color=WHITE, stroke_width=3)
        tali_kanan = Line(right_rope_end, m2_sq.get_top(), color=WHITE, stroke_width=3)
        tali_kiri.add_updater(lambda l: l.put_start_and_end_on(left_rope_end, m1_sq.get_top()))
        tali_kanan.add_updater(lambda l: l.put_start_and_end_on(right_rope_end, m2_sq.get_top()))
        self.add(tali_kiri, tali_kanan)

        # FBD (T1, T2, W1, W2)
        from renderer import make_label
        from renderer_registry import resolve_direction, SUPPORTED_COLORS
        bx, by = RIGHT, UP
        for vec in vectors:
            vec_id = vec.get("id")
            logic = vec.get("direction_logic")
            color_name = vec.get("color", "WHITE")
            if logic not in SUPPORTED_DIRECTIONS or color_name not in SUPPORTED_COLORS:
                continue
            dir_vec = resolve_direction({"direction_logic": logic}, bx, by)
            col = MANIM_COLORS[color_name]
            target = m1_sq if vec_id in ("T1", "W1") else m2_sq
            if "up" in logic:
                arrow = Arrow(ORIGIN, 1.8 * dir_vec, buff=0, color=col, stroke_width=5)
                arrow.next_to(target, UP, buff=0.2)
            else:
                arrow = Arrow(ORIGIN, 1.8 * dir_vec, buff=0, color=col, stroke_width=5)
                arrow.next_to(target, DOWN, buff=0.2)
            lbl = make_label(vec["label"], col, font_size=22)
            lbl.next_to(arrow, dir_vec, buff=0.1)
            if "up" in logic:
                arrow.add_updater(lambda m, tgt=target, d=dir_vec: m.next_to(tgt, UP, buff=0.2))
                lbl.add_updater(lambda m, a=arrow, d=dir_vec: m.next_to(a, d, buff=0.1))
            else:
                arrow.add_updater(lambda m, tgt=target, d=dir_vec: m.next_to(tgt, DOWN, buff=0.2))
                lbl.add_updater(lambda m, a=arrow, d=dir_vec: m.next_to(a, d, buff=0.1))
            self.add(arrow, lbl)

        # HUD (a, T, y1, y2) di pojok kiri atas
        hud_a = Text(f"a = {a:.2f} m/s²", font_size=28, color=YELLOW)
        hud_T = Text(f"T = {T:.1f} N", font_size=28, color=YELLOW)
        # y1 dan y2 akan diisi setelah gerakan, tetapi kita siapkan tempatnya
        hud_y1 = Text("y1 = --- m", font_size=24, color=WHITE)
        hud_y2 = Text("y2 = --- m", font_size=24, color=WHITE)

        hud = VGroup(hud_a, hud_T, hud_y1, hud_y2).arrange(DOWN, aligned_edge=LEFT).to_corner(UL, buff=0.5)
        # Tambahkan latar belakang semi‑transparan agar mudah dibaca
        bg_hud = Rectangle(width=3.5, height=2.2, fill_opacity=0.4, fill_color=BLACK, stroke_width=0).move_to(hud)
        self.play(FadeIn(bg_hud), Write(hud_a), Write(hud_T))
        # y1, y2 kita tulis nanti

        # --- Perhitungan batas gerak yang BENAR dengan margin lebih besar ---
        top_m1 = m1_sq.get_center()[1] + side_length/2
        top_m2 = m2_sq.get_center()[1] + side_length/2
        dist_rope_to_top_m1 = left_rope_end[1] - top_m1
        dist_rope_to_top_m2 = right_rope_end[1] - top_m2

        safety_margin = 0.3  # margin lebih besar agar jelas tidak menempel
        max_disp_m1_up = max(0, dist_rope_to_top_m1 - safety_margin)
        max_disp_m2_up = max(0, dist_rope_to_top_m2 - safety_margin)

        max_disp_down = abs(m1_start_y - (-5.0))  # = 4.0

        allowed_disp = 0.0
        if arah != "diam":
            runtime = 4.0
            desired_disp = 0.5 * abs(a) * runtime**2
            if arah == "m2_turun":
                up_disp = min(desired_disp, max_disp_m1_up)
                down_disp = min(desired_disp, max_disp_down)
                allowed_disp = min(up_disp, down_disp)
                self.play(
                    m1_sq.animate.shift(UP * allowed_disp),
                    m2_sq.animate.shift(DOWN * allowed_disp),
                    run_time=runtime,
                    rate_func=linear
                )
            else:
                up_disp = min(desired_disp, max_disp_m2_up)
                down_disp = min(desired_disp, max_disp_down)
                allowed_disp = min(up_disp, down_disp)
                self.play(
                    m1_sq.animate.shift(DOWN * allowed_disp),
                    m2_sq.animate.shift(UP * allowed_disp),
                    run_time=runtime,
                    rate_func=linear
                )

        # Indikator ketinggian (garis putus-putus di SAMPING) — tetap seperti yang sudah oke
        offset_x = 0.6
        def get_vertical_line(obj, color, dx):
            center = obj.get_center()
            start = np.array([center[0] + dx, center[1], 0])
            end = np.array([center[0] + dx, zero_line_y, 0])
            return DashedLine(start, end, color=color, dash_length=0.15)

        vert_m1 = get_vertical_line(m1_sq, BLUE, -offset_x)
        vert_m2 = get_vertical_line(m2_sq, RED, offset_x)
        self.play(Create(vert_m1), Create(vert_m2))

        # Update HUD dengan nilai y1 dan y2
        pos1_y = m1_sq.get_center()[1] - zero_line_y
        pos2_y = m2_sq.get_center()[1] - zero_line_y
        new_y1 = Text(f"y1 = {pos1_y:.2f} m", font_size=24, color=BLUE)
        new_y2 = Text(f"y2 = {pos2_y:.2f} m", font_size=24, color=RED)
        # Tempatkan di posisi yang sama dengan placeholder
        new_y1.move_to(hud_y1)
        new_y2.move_to(hud_y2)
        self.play(Transform(hud_y1, new_y1), Transform(hud_y2, new_y2))

        self.wait(2)
