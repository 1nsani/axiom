import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

def test_inclined_plane_caption_diam():
    from solvers.inclined_plane import generate_caption
    known = {"massa": 5, "sudut_permukaan": 30, "gaya_eksternal": 0, "koefisien_gesek": 0.5}
    hasil = {"percepatan": 0.0, "arah_gerak": "diam", "gaya_gesek": 0.09, "gaya_normal": 39.93}
    caption = generate_caption(known, hasil)
    assert "diam" in caption
    assert "0.09" in caption  # gaya gesek
    assert "39.93" in caption

def test_inclined_plane_caption_bergerak():
    from solvers.inclined_plane import generate_caption
    known = {"massa": 4, "sudut_permukaan": 30, "gaya_eksternal": 0, "koefisien_gesek": 0.2}
    hasil = {"percepatan": 3.2, "arah_gerak": "ke_bawah", "gaya_gesek": 2.8, "gaya_normal": 34.64}
    caption = generate_caption(known, hasil)
    assert "bergerak" in caption.lower()
    assert "3.2" in caption
    assert "2.8" in caption
    assert "34.64" in caption

def test_collision_caption():
    from solvers.collision import generate_caption
    known = {"massa_1": 2, "massa_2": 2, "v1_awal": 5, "v2_awal": 0, "koefisien_restitusi": 1.0}
    hasil = {"v1_akhir": 0.0, "v2_akhir": 5.0, "energi_hilang": 0.0}
    caption = generate_caption(known, hasil)
    assert "5.0" in caption
    assert "0.0" in caption
    assert "elastis" in caption.lower()

def test_katrol_caption():
    from solvers.katrol import generate_caption
    known = {"massa_1": 3, "massa_2": 5}
    hasil = {"percepatan": 2.5, "tegangan": 37.5, "arah_gerak": "m2_turun"}
    caption = generate_caption(known, hasil)
    assert "2.5" in caption
    assert "37.5" in caption
    assert "m2_turun" in caption

def test_gerak_parabola_caption():
    from solvers.gerak_parabola import generate_caption
    known = {"v0": 20, "sudut_elevasi": 45}
    hasil = {"jarak_horizontal_maks": 40.0, "tinggi_maksimum": 10.0, "waktu_di_udara": 2.83}
    caption = generate_caption(known, hasil)
    assert "40.0" in caption
    assert "10.0" in caption
    assert "2.83" in caption
