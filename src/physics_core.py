def elastic_collision_1d(m1, v1, m2, v2):
    """
    Rumus tumbukan elastis 1D standar.
    Bekerja untuk float MAUPUN sympy.Symbol — tidak ada operasi spesifik numpy.
    """
    v1_akhir = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
    v2_akhir = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
    return v1_akhir, v2_akhir
