from __future__ import annotations

from math import asin, cos, radians, sin, sqrt

from src.sources import fetch_open_charge_map_stations, fetch_overpass_stations, load_fallback_stations
from src.tariffs import infer_tariff


MAINZ_CENTER = (49.9929, 8.2473)


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * r * asin(sqrt(a))


def _merge_deduplicate(stations: list[dict]) -> list[dict]:
    merged: list[dict] = []
    for station in stations:
        found = None
        for existing in merged:
            d = _haversine_km(station["lat"], station["lon"], existing["lat"], existing["lon"])
            if d <= 0.05:  # 50m
                found = existing
                break
        if found:
            if station.get("source") not in found["sources"]:
                found["sources"].append(station.get("source"))
            if not found.get("operator") and station.get("operator"):
                found["operator"] = station["operator"]
            if not found.get("address") and station.get("address"):
                found["address"] = station["address"]
        else:
            merged.append(
                {
                    **station,
                    "sources": [station.get("source")],
                }
            )
    return merged


def aggregate_stations(center_lat: float | None, center_lon: float | None, radius_km: float = 12) -> dict:
    center_lat = center_lat if center_lat is not None else MAINZ_CENTER[0]
    center_lon = center_lon if center_lon is not None else MAINZ_CENTER[1]

    raw = fetch_overpass_stations() + fetch_open_charge_map_stations()
    if not raw:
        raw = load_fallback_stations()
    merged = _merge_deduplicate(raw)

    filtered = []
    for station in merged:
        distance = _haversine_km(center_lat, center_lon, station["lat"], station["lon"])
        if distance <= radius_km:
            tariff = infer_tariff(station.get("operator"))
            station["distance_km"] = round(distance, 2)
            station["tariff"] = (
                {
                    "provider": tariff.provider,
                    "ac_eur_kwh": tariff.ac_eur_kwh,
                    "dc_eur_kwh": tariff.dc_eur_kwh,
                    "source_url": tariff.source_url,
                    "note": tariff.note,
                }
                if tariff
                else None
            )
            filtered.append(station)

    filtered.sort(key=lambda x: x["distance_km"])

    return {
        "city": "Mainz",
        "count": len(filtered),
        "sources_used": sorted({src for st in filtered for src in st.get("sources", [])}) or ["Lokaler Fallback-Datensatz"],
        "stations": filtered,
        "disclaimer": "Preise sind öffentliche Richtwerte und können je nach App, Vertrag und Zeit variieren.",
    }
