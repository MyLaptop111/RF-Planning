import math

def fspl_db(f_mhz: float, d_km: float) -> float:
    if f_mhz <= 0 or d_km <= 0:
        raise ValueError("Frequency and distance must be > 0.")
    return 32.44 + 20*math.log10(f_mhz) + 20*math.log10(d_km)

def mobile_antenna_correction(hm_m: float, f_mhz: float) -> float:
    # Small/medium city Hata correction.
    return (1.1*math.log10(f_mhz) - 0.7)*hm_m - (1.56*math.log10(f_mhz) - 0.8)

def okumura_hata_db(f_mhz: float, hb_m: float, hm_m: float, d_km: float) -> float:
    if not (150 <= f_mhz <= 1500):
        raise ValueError("Classic Hata is normally used for 150–1500 MHz.")
    if hb_m <= 0 or hm_m <= 0 or d_km <= 0:
        raise ValueError("Heights and distance must be > 0.")
    a_hm = mobile_antenna_correction(hm_m, f_mhz)
    return (69.55 + 26.16*math.log10(f_mhz) - 13.82*math.log10(hb_m)
            - a_hm + (44.9 - 6.55*math.log10(hb_m))*math.log10(d_km))

def cost231_hata_db(f_mhz: float, hb_m: float, hm_m: float, d_km: float, cm_db: float = 3.0) -> float:
    if not (1500 <= f_mhz <= 2000):
        raise ValueError("COST-231 Hata is normally used around 1500–2000 MHz.")
    if hb_m <= 0 or hm_m <= 0 or d_km <= 0:
        raise ValueError("Heights and distance must be > 0.")
    a_hm = mobile_antenna_correction(hm_m, f_mhz)
    return (46.3 + 33.9*math.log10(f_mhz) - 13.82*math.log10(hb_m)
            - a_hm + (44.9 - 6.55*math.log10(hb_m))*math.log10(d_km) + cm_db)
