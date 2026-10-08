import math

def haversine_km(lat1, lon1, lat2, lon2):
    R=6371.0088
    p1,p2=math.radians(lat1),math.radians(lat2)
    dp=math.radians(lat2-lat1); dl=math.radians(lon2-lon1)
    a=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(a))

def polygon_area_m2(points):
    if len(points)<3: return 0.0
    lat0=math.radians(sum(p[0] for p in points)/len(points))
    R=6371008.8
    xy=[(math.radians(lon)*R*math.cos(lat0), math.radians(lat)*R) for lat,lon in points]
    return abs(sum(xy[i][0]*xy[(i+1)%len(xy)][1]-xy[(i+1)%len(xy)][0]*xy[i][1] for i in range(len(xy)))/2)
