"""
Translator dari skema JSON ke sistem sympy.physics.mechanics (Kane's Method).
"""

from sympy.physics.mechanics import dynamicsymbols, ReferenceFrame, Point, Particle, KanesMethod
from sympy import symbols
from mechanics_registry import SUPPORTED_ARAH_GERAK, SUPPORTED_GAYA, validate_system_def

def bangun_sistem_kanes(skema: dict):
    """
    Membangun sistem Kane's Method dari skema JSON.
    
    Returns:
        tuple: (KanesMethod, dict) dengan kunci:
            - q, u, qd: generalized coordinate/speed/derivative
            - particles: list of Particle
            - titik_map: dict mapping id benda ke Point
            - simbol: dict simbol-simbol yang dipakai
            - fr, frstar: generalized forces
    """
    validate_system_def(skema)
    
    N = ReferenceFrame('N')
    O = Point('O')
    O.set_vel(N, 0)
    
    q = dynamicsymbols('q')
    u = dynamicsymbols('u')
    qd = dynamicsymbols('q', 1)
    kd = [qd - u]
    
    particles = []
    titik_map = {}
    all_symbols = {}
    
    # Tambahkan simbol standar
    g = symbols('g', positive=True)
    mu = symbols('mu', positive=True)
    all_symbols['g'] = g
    all_symbols['mu'] = mu
    
    # Proses setiap benda
    for benda in skema["benda"]:
        benda_id = benda["id"]
        massa_simbol = benda["massa_simbol"]
        m = symbols(massa_simbol, positive=True)
        all_symbols[massa_simbol] = m
        
        tipe_arah = benda["arah_gerak"]["tipe"]
        tanda = benda["arah_gerak"].get("tanda", 1)
        
        # Dapatkan unit vector arah (sympy)
        arah_unit = SUPPORTED_ARAH_GERAK[tipe_arah](N)
        arah_gerak = tanda * arah_unit
        
        titik = O.locatenew(benda_id, q * arah_gerak)
        titik.set_vel(N, u * arah_gerak)
        titik_map[benda_id] = titik
        
        P = Particle(benda_id, titik, m)
        particles.append(P)
    
    # Proses setiap gaya
    loads = []
    for gaya in skema["gaya"]:
        tipe_gaya = gaya["tipe"]
        benda_id = gaya["benda"]
        benda_def = next(b for b in skema["benda"] if b["id"] == benda_id)
        load = SUPPORTED_GAYA[tipe_gaya](benda_def, skema, N, titik_map)
        loads.append(load)
    
    q_ind = [q]
    u_ind = [u]
    KM = KanesMethod(N, q_ind=q_ind, u_ind=u_ind, kd_eqs=kd)
    fr, frstar = KM.kanes_equations(particles, loads=loads)
    
    return KM, {
        'q': q, 'u': u, 'qd': qd,
        'particles': particles,
        'titik_map': titik_map,
        'simbol': all_symbols,
        'N': N, 'O': O,
        'fr': fr, 'frstar': frstar,
    }
