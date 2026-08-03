from manim import *

def make_label(t, c, fs=20):
    try:
        return MathTex(t, color=c).scale(fs/24)
    except:
        return Text(t, font_size=fs, color=c)

class StoryboardScene(MovingCameraScene):
    def construct(self):
        import json, os
        sp = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "storyboard_approved.json")
        if not os.path.exists(sp):
            self.add(Text("storyboard_approved.json tidak ditemukan", font_size=24, color=RED))
            self.wait(2)
            return
        with open(sp) as f:
            sb = json.load(f)
        sumber = sb.get('sumber_data', {})
        semua = {**sumber.get('known', {}), **sumber.get('hasil_fisika', {})}
        from storyboard_registry import SUPPORTED_AKSI
        from scene_bounds import apply_auto_framing
        apply_auto_framing(self, sb.get('domain_asal', 'static_incline'), sumber.get('known', {}), sumber.get('hasil_fisika', {}))
        for fase in sb.get('fase', []):
            dur = fase.get('durasi_detik', 2.0)
            cap = fase.get('caption_template', '')
            try:
                cap = cap.format(**semua)
            except:
                pass
            mobs = []
            for aksi in fase.get('aksi', []):
                tipe = aksi.get('tipe')
                if tipe in SUPPORTED_AKSI:
                    mobs.extend(SUPPORTED_AKSI[tipe](aksi.get('parameter', {}), sumber))
            cap_mob = Text(cap, font_size=24, color=WHITE).to_edge(DOWN) if cap else None
            anims = [FadeIn(m) for m in mobs]
            if cap_mob:
                anims.append(Write(cap_mob))
            if anims:
                self.play(*anims, run_time=dur)
            self.wait(0.3)
        self.wait(1)
