from manim import *
import json
import os
import numpy as np

class DinamikaTranslasiScene(Scene):
    def construct(self):
        # 1. BACA PAYLOAD JSON UNIVERSAL
        try:
            with open("anim_input.json", "r") as f:
                physics_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("FATAL: anim_input.json tidak ditemukan.")

        # 2. EKSTRAKSI PARAMETER BERSARANG
        # Mengambil dari key "parameters" sesuai standar K-Series
        params = physics_data.get("parameters", physics_data) 
        
        massa = params.get("massa", 0)
        # Tangani kemungkinan nama key sudut yang berbeda dari Gemini
        theta_deg = params.get("sudut_kemiringan", params.get("theta", 30)) 
        percepatan = params.get("percepatan", 0)
        arah = params.get("arah_gerak", "diam")
        
        theta_rad = np.radians(theta_deg)

        # 3. GEOMETRI DASAR
        bidang_miring = Line(ORIGIN, 6 * RIGHT).rotate(theta_rad, about_point=ORIGIN).shift(LEFT*2 + DOWN*1)
        base_line = Line(bidang_miring.get_start(), bidang_miring.get_start() + 6 * RIGHT)
        angle_arc = Angle(base_line, bidang_miring, radius=0.8)
        angle_label = MathTex(rf"{theta_deg}^\circ").next_to(angle_arc, RIGHT, buff=0.1)

        balok = Square(side_length=0.8, fill_opacity=0.6, color=BLUE)
        balok.rotate(theta_rad)
        
        # Kamus Vektor (Logika Matematika)
        vektor_normal = np.array([-np.sin(theta_rad), np.cos(theta_rad), 0.0])
        vektor_paralel = np.array([np.cos(theta_rad), np.sin(theta_rad), 0.0])
        
        start_point = bidang_miring.point_from_proportion(0.15) + (0.4 * vektor_normal)
        balok.move_to(start_point)

        self.play(Create(bidang_miring), Create(base_line), Create(angle_arc), Write(angle_label))
        self.play(FadeIn(balok))

        # 4. PERAKITAN VEKTOR DINAMIS (Berdasarkan Obsidian Visual Hooks)
        vectors_to_render = physics_data.get("vectors_to_render", [])
        panah_group = VGroup()
        
        # Pemetaan warna string ke objek warna Manim
        color_map = {
            "GREEN": GREEN, "YELLOW": YELLOW, "RED": RED, 
            "BLUE": BLUE, "WHITE": WHITE
        }

        for v in vectors_to_render:
            v_logic = v.get("direction_logic", "")
            v_color = color_map.get(v.get("color", "WHITE"), WHITE)
            v_label_tex = v.get("label", "")
            
            # Terjemahkan bahasa Obsidian ke bahasa Numpy
            if v_logic == "parallel_up":
                arah_vektor = vektor_paralel
            elif v_logic == "parallel_down":
                arah_vektor = -vektor_paralel
            elif v_logic == "perpendicular_up":
                arah_vektor = vektor_normal
            elif v_logic == "absolute_down":
                arah_vektor = DOWN
            else:
                arah_vektor = UP
            
            # Buat Panah dengan Updater
            panah = Arrow(max_stroke_width_to_length_ratio=0, color=v_color)
            panah.add_updater(lambda m, av=arah_vektor: m.put_start_and_end_on(
                balok.get_center(), 
                balok.get_center() + 1.5 * av
            ))
            
            label = MathTex(v_label_tex).add_updater(
                lambda m, p=panah, av=arah_vektor: m.next_to(p.get_end(), av, buff=0.1)
            )
            
            panah_group.add(panah, label)

        self.play(Create(panah_group))

        # 5. EKSEKUSI ANIMASI TRANSLASI
        if arah == "ke_atas":
            target_posisi = bidang_miring.point_from_proportion(0.75) + (0.4 * vektor_normal)
        elif arah == "ke_bawah":
            target_posisi = bidang_miring.point_from_proportion(0.15) + (0.4 * vektor_normal)
        else:
            target_posisi = balok.get_center()

        # Proteksi run_time agar tidak error saat percepatan 0 atau string aneh
        try:
            run_time_calc = max(1.5, 6.0 / (float(abs(percepatan)) + 1))
        except (ValueError, TypeError):
            run_time_calc = 2.0
            
        if arah != "diam" and arah != "":
            self.play(balok.animate.move_to(target_posisi), run_time=run_time_calc, rate_func=linear)
        
        self.wait(1)
        
