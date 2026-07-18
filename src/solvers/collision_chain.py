from physics_core import elastic_collision_1d

def simulate_collision_chain(kecepatan_awal: dict, massa: dict,
                              urutan: list, max_tumbukan: int = 50) -> dict:
    """
    Simulasi tumbukan berantai 1D untuk N benda tersusun berjajar.
    ASUMSI: tepat SATU benda bergerak di awal, sisanya diam.
    """
    v = dict(kecepatan_awal)
    m = dict(massa)
    urut = list(urutan)
    n = len(urut)

    log = []
    jumlah = 0

    # Cari indeks benda yang bergerak
    aktif_idx = next((i for i, id_ in enumerate(urut) if v[id_] != 0), None)
    if aktif_idx is None:
        return {"jumlah_tumbukan": 0, "log_tumbukan": [], "kecepatan_akhir": v, "status": "stabil"}

    while jumlah < max_tumbukan:
        id_aktif = urut[aktif_idx]
        v_aktif = v[id_aktif]
        bertumbukan = False

        # Cek tetangga kanan
        if v_aktif > 0 and aktif_idx < n - 1:
            id_kanan = urut[aktif_idx + 1]
            if v[id_kanan] < v_aktif:  # benda aktif mendekati dari kiri
                v1_new, v2_new = elastic_collision_1d(
                    m[id_aktif], v_aktif,
                    m[id_kanan], v[id_kanan]
                )
                log.append({
                    "pasangan": (id_aktif, id_kanan),
                    "v_sebelum": (v_aktif, v[id_kanan]),
                    "v_sesudah": (v1_new, v2_new)
                })
                v[id_aktif] = v1_new
                v[id_kanan] = v2_new
                jumlah += 1
                bertumbukan = True

                # Setelah tumbukan, benda aktif bisa:
                # 1. Berhenti (v1_new == 0) -> benda kanan jadi aktif baru
                # 2. Tetap bergerak ke kanan (v1_new > 0) -> tetap di indeks yang sama
                # 3. Berbalik arah (v1_new < 0) -> harus dicek di cabang kiri di iterasi berikutnya
                if v1_new > 0:
                    continue  # tetap di indeks yang sama, cek tetangga kanan lagi
                elif v1_new < 0:
                    continue  # berbalik, akan dicek di cabang kiri nanti
                else:
                    # v1_new == 0, benda aktif berhenti
                    if v2_new != 0:
                        aktif_idx += 1  # benda kanan menjadi aktif baru
                        continue
                    else:
                        # Keduanya diam, cari benda bergerak lain
                        aktif_idx = next((i for i, id_ in enumerate(urut) if v[id_] != 0), None)
                        if aktif_idx is None:
                            break
                        continue

        # Cek tetangga kiri
        if v_aktif < 0 and aktif_idx > 0:
            id_kiri = urut[aktif_idx - 1]
            if v[id_kiri] > v_aktif:  # benda aktif mendekati dari kanan
                v1_new, v2_new = elastic_collision_1d(
                    m[id_kiri], v[id_kiri],
                    m[id_aktif], v_aktif
                )
                log.append({
                    "pasangan": (id_kiri, id_aktif),
                    "v_sebelum": (v[id_kiri], v_aktif),
                    "v_sesudah": (v1_new, v2_new)
                })
                v[id_kiri] = v1_new
                v[id_aktif] = v2_new
                jumlah += 1
                bertumbukan = True

                if v2_new < 0:
                    continue  # tetap di indeks yang sama
                elif v2_new > 0:
                    continue
                else:
                    # v2_new == 0, benda aktif berhenti
                    if v1_new != 0:
                        aktif_idx -= 1
                        continue
                    else:
                        aktif_idx = next((i for i, id_ in enumerate(urut) if v[id_] != 0), None)
                        if aktif_idx is None:
                            break
                        continue

        if not bertumbukan:
            break

    status = "melebihi_batas_maksimum" if jumlah >= max_tumbukan else "stabil"
    return {
        "jumlah_tumbukan": jumlah,
        "log_tumbukan": log,
        "kecepatan_akhir": v,
        "status": status
    }
