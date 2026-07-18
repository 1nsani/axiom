"""
Lapisan ekstraksi numerik dari KanesMethod.
"""

from sympy import simplify, symbols
from sympy.physics.mechanics import KanesMethod

def turunkan_percepatan_simbolik(KM: KanesMethod):
    """
    Ekstrak percepatan simbolik (u_dot) dari KanesMethod.
    """
    mass_matrix = KM.mass_matrix_full
    forcing = KM.forcing_full
    sol = mass_matrix.inv() * forcing
    percepatan = simplify(sol[1])
    return percepatan


def substitusi_numerik(ekspresi_simbolik, nilai_parameter: dict, simbol_map: dict = None) -> float:
    """
    Substitusi nilai numerik ke ekspresi simbolik.
    """
    subs_dict = {}
    for k, v in nilai_parameter.items():
        if simbol_map and k in simbol_map:
            subs_dict[simbol_map[k]] = v
        else:
            subs_dict[symbols(k)] = v
    hasil = ekspresi_simbolik.subs(subs_dict).evalf()
    return float(hasil)


def hitung_gaya_constraint(skema: dict, KM: KanesMethod, a: float, nilai_param: dict) -> dict:
    result = {}
    sistem_id = skema.get("sistem_id", "")
    
    if "katrol" in sistem_id:
        g = nilai_param.get('g', 10.0)
        for benda in skema['benda']:
            massa = nilai_param.get(benda['massa_simbol'], 1.0)
            if benda['arah_gerak']['tanda'] == 1:
                T = massa * (g - a)
            else:
                T = massa * (g + a)
            result['tegangan'] = round(T, 4)
            break
    
    if "bidang_miring" in sistem_id:
        g = nilai_param.get('g', 10.0)
        for benda in skema['benda']:
            if benda['arah_gerak']['tipe'] == 'sepanjang_bidang_miring':
                massa = nilai_param.get(benda['massa_simbol'], 1.0)
                from math import cos, radians
                sudut = benda['arah_gerak']['parameter'].get('sudut', 30)
                normal = massa * g * cos(radians(sudut))
                result['gaya_normal'] = round(normal, 4)
                mu = nilai_param.get('mu', 0)
                if mu > 0:
                    result['gaya_gesek'] = round(mu * normal, 4)
    
    return result
