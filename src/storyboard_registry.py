import numpy as np
from manim import *

def _gambar_bidang_miring(params, sumber):
    sudut = params.get('sudut', 30)
    theta = np.radians(sudut)
    bidang = Line(ORIGIN, 7*RIGHT).rotate(theta, about_point=ORIGIN).shift(LEFT*3 + DOWN*1)
    alas = Line(bidang.get_start(), bidang.get_start() + 7*RIGHT)
    return [alas, bidang]

def _gambar_balok(params, sumber):
    warna_map = {'BLUE': BLUE, 'RED': RED, 'GREEN': GREEN, 'YELLOW': YELLOW, 'WHITE': WHITE}
    warna = warna_map.get(params.get('warna', 'BLUE'), BLUE)
    ukuran = params.get('ukuran', 0.8)
    return [Square(side_length=ukuran, fill_opacity=0.6, color=warna)]

def _tampilkan_vektor(params, sumber):
    arah_map = {'UP': UP, 'DOWN': DOWN, 'LEFT': LEFT, 'RIGHT': RIGHT}
    arah = arah_map.get(params.get('arah', 'UP'), UP)
    warna_map = {'WHITE': WHITE, 'YELLOW': YELLOW, 'RED': RED, 'GREEN': GREEN, 'BLUE': BLUE}
    warna = warna_map.get(params.get('warna', 'WHITE'), WHITE)
    panjang = params.get('panjang', 1.5)
    return [Arrow(ORIGIN, panjang * arah, buff=0, color=warna)]

def _animasikan_pergerakan(params, sumber):
    return []

def _highlight_teks(params, sumber):
    return []

SUPPORTED_AKSI = {
    "gambar_bidang_miring": _gambar_bidang_miring,
    "gambar_balok": _gambar_balok,
    "tampilkan_vektor": _tampilkan_vektor,
    "animasikan_pergerakan": _animasikan_pergerakan,
    "highlight_teks": _highlight_teks,
}
SUPPORTED_AKSI_KEYS = set(SUPPORTED_AKSI.keys())
