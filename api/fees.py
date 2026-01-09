import math


def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(
        math.radians, [float(lat1), float(lon1), float(lat2), float(lon2)]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )

    return 6371 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def delivery_fee_inr(distance_km):
    BASE = 20
    FREE_KM = 2
    PER_KM = 8

    chargeable = max(0, distance_km - FREE_KM)
    return round(BASE + chargeable * PER_KM, 2)
