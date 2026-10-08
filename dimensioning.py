import math

def hex_cell_area_km2(radius_km: float) -> float:
    return 3*math.sqrt(3)/2 * radius_km**2

def sites_from_area(area_km2: float, cell_radius_km: float) -> int:
    if area_km2 <= 0 or cell_radius_km <= 0:
        raise ValueError("Area and radius must be > 0.")
    return math.ceil(area_km2 / hex_cell_area_km2(cell_radius_km))

def sites_from_capacity(total_traffic_erl, site_capacity_erl) -> int:
    if total_traffic_erl <= 0 or site_capacity_erl <= 0:
        raise ValueError("Traffic and site capacity must be > 0.")
    return math.ceil(total_traffic_erl / site_capacity_erl)

def required_sites(n_coverage: int, n_capacity: int, n_traffic: int = 0) -> int:
    return max(n_coverage, n_capacity, n_traffic)
