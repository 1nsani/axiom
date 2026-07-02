from manim import *
import json
import os

class DinamikaTranslasiScene(Scene):
    def construct(self):
        # 1. PENCARIAN PAYLOAD JSON (THE BRIDGE)
        # Mencari file anim_input.json yang dilempar oleh Axiom-knowledge
        # Asumsi struktur folder di Colab/Lokal:
        # /content/
        #   ├── Axiom-knowledge/anim_input.json
        #   └── axiom/src/renderer.py
        
        possible_paths = [
            "../Axiom-knowledge/anim_input.json",  # Jika dijalankan dari dalam folder axiom
            "../../Axiom-knowledge/anim_input.json", # Jika dijalankan dari dalam axiom/src
            "anim_input.json",                     # Fallback 1
            "/content/Axiom-knowledge/anim_input.json" # Fallback absolut di Colab
        ]
        
        json_path = None
        for path in possible_paths:
            if os.path.exists(path):
                json_path = path
                break
                
        if not json_path:
            raise FileNotFoundError("FATAL: anim_input.json tidak ditemukan. Jalankan Axiom-knowledge (Otak) terlebih dahulu.")

        # 2. MEMBACA DATA ABSOLUT
        with open(json_path, "r") as f:
            physics_data = json.load(f)

        massa = physics_data["massa"]
        theta_deg = physics_data["sudut_kemiringan"]
        percepatan = physics_data["percepatan"]
        arah = physics_data["arah_gerak"]
        
        theta_rad = np.radians(theta_deg)

        # 3. MERAKIT GEOMETRI VISUAL (TANPA MENGHITUNG FISIKA)
        # Bidang Miring
        bidang_miring = Line(ORIGIN, 5 * RIGHT).rotate(theta_rad, about_point=ORIGIN)
        base_line = Line(ORIGIN, 5 * RIGHT)
        angle_arc = Angle(base_line, bidang_miring, radius=0.8)
        angle_label = MathTex(rf"{theta_deg}^\circ").next_to(angle_arc, RIGHT, buff=0.1)

        # Balok
        balok = Square(side_length=0.8, fill_opacity=0.7, color=BLUE)
        balok.rotate(theta_rad)
        # Posisi awal (0.2 dari panjang bidang miring)
        start_point = bidang_miring.point_from_proportion(0.2) + 0.4 * UP.rotate(theta_rad)
        balok.move_to(start_point)

        # 4. DIREKSI ANIMASI
        if arah == "ke_atas":
            target_posisi = bidang_miring.point_from_proportion(0.8) + 0.4 * UP.rotate(theta_rad)
        elif arah == "ke_bawah":
            target_posisi = bidang_miring.point_from_proportion(0.0) + 0.4 * UP.rotate(theta_rad)
        else:
            target_posisi = balok.get_center()

        # Tampilkan Elemen Statis
        self.play(Create(bidang_miring), Create(base_line), Create(angle_arc), Write(angle_label))
        self.play(FadeIn(balok))
        self.wait(0.5)

        # HUD (Head-Up Display) Parameter
        hud_text = Tex(f"Massa: {massa} kg\\\\Percepatan: {percepatan} m/s$^2$").to_edge(UP + LEFT)
        self.play(Write(hud_text))

        # Eksekusi Vektor Gerak
        # Waktu animasi berbanding terbalik dengan percepatan (skala kasar untuk visual)
        run_time_calc = max(1.0, 5.0 / (abs(percepatan) + 1)) 
        
        if arah != "diam":
            self.play(
                balok.animate.move_to(target_posisi), 
                run_time=run_time_calc, 
                rate_func=linear
            )
        
        self.wait(1)
