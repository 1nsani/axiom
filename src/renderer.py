from manim import *
import json
import numpy as np

class DinamikaTranslasiScene(Scene):
    def construct(self):
        # ==========================================
        # FASE 0: INGESTI DATA (OTAK -> TUBUH)
        # ==========================================
        try:
            with open("anim_input.json", "r") as f:
                physics_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("FATAL: anim_input.json tidak ditemukan. Sinkronisasi terputus.")

        params = physics_data.get("parameters", physics_data) 
        massa = params.get("massa", 0)
        theta_deg = params.get("sudut_kemiringan", params.get("theta", 30)) 
        percepatan = float(params.get("percepatan", 0))
        arah = params.get("arah_gerak", "diam")
        
        theta_rad = np.radians(theta_deg)

        # ==========================================
        # FASE 1: PENYUSUNAN LINGKUNGAN STATIS
        # ==========================================
        bidang_miring = Line(ORIGIN, 7 * RIGHT).rotate(theta_rad, about_point=ORIGIN).shift(LEFT*3 + DOWN*1)
        base_line = Line(bidang_miring.get_start(), bidang_miring.get_start() + 7 * RIGHT)
        angle_arc = Angle(base_line, bidang_miring, radius=0.8)
        angle_label = MathTex(rf"{theta_deg}^\circ").next_to(angle_arc, RIGHT, buff=0.1)

        self.play(Create(base_line), Create(bidang_miring), run_time=1)
        self.play(Create(angle_arc), Write(angle_label), run_time=0.5)

        # ==========================================
        # FASE 2: ENTITAS FISIKA & HUD KINEMATIKA
        # ==========================================
        vektor_normal = np.array([-np.sin(theta_rad), np.cos(theta_rad), 0.0])
        vektor_paralel = np.array([np.cos(theta_rad), np.sin(theta_rad), 0.0])
        
        balok = Square(side_length=0.8, fill_opacity=0.6, color=BLUE)
        balok.rotate(theta_rad)
        
        start_point = bidang_miring.point_from_proportion(0.15) + (0.4 * vektor_normal)
        balok.move_to(start_point)

        hud_text = VGroup(
            Tex(f"Massa ($m$): {massa} kg"),
            Tex(f"Percepatan ($a$): {percepatan:.2f} m/s$^2$")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.7).to_corner(UL)

        self.play(FadeIn(balok, shift=DOWN*0.5), Write(hud_text))

        # ==========================================
        # FASE 3: DIAGRAM BENDA BEBAS (TRANSLASI SPASIAL)
        # ==========================================
        vectors_to_render = physics_data.get("vectors_to_render", [])
        color_map = {"GREEN": GREEN, "YELLOW": YELLOW, "RED": RED, "BLUE": BLUE, "WHITE": WHITE}
        
        panah_group = VGroup()
        
        for v in vectors_to_render:
            v_logic = v.get("direction_logic", "")
            v_color = color_map.get(v.get("color", "WHITE"), WHITE)
            v_label_tex = v.get("label", "")
            
            if v_logic == "parallel_up": arah_vektor = vektor_paralel
            elif v_logic == "parallel_down": arah_vektor = -vektor_paralel
            elif v_logic == "perpendicular_up": arah_vektor = vektor_normal
            elif v_logic == "absolute_down": arah_vektor = DOWN
            else: arah_vektor = UP
            
            # Perbaikan Absolut: Hindari put_start_and_end_on. Gunakan shift murni.
            panah = Arrow(ORIGIN, 1.5 * arah_vektor, buff=0, color=v_color, stroke_width=4)
            panah.move_to(balok.get_center() + 0.75 * arah_vektor) # Posisi awal
            
            panah.add_updater(lambda m, av=arah_vektor: m.shift(balok.get_center() - m.get_start()))
            
            label = MathTex(v_label_tex, color=v_color).scale(0.8)
            label.add_updater(lambda m, p=panah, av=arah_vektor: m.move_to(p.get_end() + 0.3 * av))
            
            panah_group.add(panah, label)
            self.play(GrowArrow(panah), Write(label), run_time=0.4)

        self.wait(0.5)

        # ==========================================
        # FASE 4: DYNAMICS EKSEKUSI
        # ==========================================
        if arah == "ke_atas":
            target_posisi = bidang_miring.point_from_proportion(0.85) + (0.4 * vektor_normal)
        elif arah == "ke_bawah":
            target_posisi = bidang_miring.point_from_proportion(0.0) + (0.4 * vektor_normal)
        else:
            target_posisi = balok.get_center()

        # Proteksi pembagian nol absolut
        run_time_calc = 1.5 if percepatan == 0 else max(1.0, 6.0 / (abs(percepatan) + 1))
            
        if arah != "diam" and percepatan != 0:
            self.play(balok.animate.move_to(target_posisi), run_time=run_time_calc, rate_func=linear)
        
        self.wait(1.5)
        
