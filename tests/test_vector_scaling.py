import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from renderer_registry import scale_vector_length

def test_proportional_scaling():
    """Gaya 2x lebih besar menghasilkan panjang yang lebih panjang."""
    mags = [10, 20, 30]
    len1 = scale_vector_length(10, mags)
    len2 = scale_vector_length(20, mags)
    len3 = scale_vector_length(30, mags)
    assert len2 > len1, f"{len2} harus > {len1}"
    assert len3 > len2

def test_min_length_floor():
    """Gaya sangat kecil tetap >= min_len."""
    len_tiny = scale_vector_length(0.01, [100, 200])
    assert len_tiny >= 0.4, f"Panjang vektor kecil harus >= 0.4, tapi {len_tiny}"

def test_zero_magnitude_returns_min():
    """Magnitudo nol mengembalikan min_len."""
    assert scale_vector_length(0, [10]) == 0.4

def test_all_zero_magnitudes():
    """Jika semua magnitudo nol, tetap dapat min_len."""
    assert scale_vector_length(0, [0, 0]) == 0.4

def test_max_length_bound():
    """Magnitudo maksimum mendapat max_len."""
    max_mag = 100
    len_max = scale_vector_length(max_mag, [10, max_mag])
    assert abs(len_max - 2.0) < 0.01
