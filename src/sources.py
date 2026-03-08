from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen

MAINZ_BBOX = {
    "south": 49.93,
    "west": 8.17,
    "north": 50.06,
    "east": 8.34,
}

FALLBACK_DATA = Path(__file__).resolve().parents[1] / "data" / "mainz_fallback_stations.json"


def _safe_get(url: str, *, params: dict[str, Any] | None = None, timeout: int = 20) -> dict[str, Any] | list[dict[str, Any]]:
    full_url = f"{url}?{urlencode(params or {})}" if params else url
    with urlopen(full_url, timeout=timeout) as resp:  # noqa: S310
        return json.loads(resp.read().decode("utf-8"))


def load_fallback_stations() -> list[dict[str, Any]]:
    return json.loads(FALLBACK_DATA.read_text(encoding="utf-8"))


def fetch_overpass_stations() -> list[dict[str, Any]]:
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="charging_station"]({MAINZ_BBOX['south']},{MAINZ_BBOX['west']},{MAINZ_BBOX['north']},{MAINZ_BBOX['east']});
      way["amenity"="charging_station"]({MAINZ_BBOX['south']},{MAINZ_BBOX['west']},{MAINZ_BBOX['north']},{MAINZ_BBOX['east']});
      relation["amenity"="charging_station"]({MAINZ_BBOX['south']},{MAINZ_BBOX['west']},{MAINZ_BBOX['north']},{MAINZ_BBOX['east']});
    );
    out center tags;
    """
    try:
        data = _safe_get("https://overpass-api.de/api/interpreter", params={"data": query})
    except Exception:
        return []

    items: list[dict[str, Any]] = []
    for e in data.get("elements", []):
        tags = e.get("tags", {})
        lat = e.get("lat") or (e.get("center") or {}).get("lat")
        lon = e.get("lon") or (e.get("center") or {}).get("lon")
        if lat is None or lon is None:
            continue
        items.append(
            {
                "id": f"osm-{e['type']}-{e['id']}",
                "name": tags.get("name") or "Ladesäule (OSM)",
                "operator": tags.get("operator") or tags.get("network"),
                "lat": lat,
                "lon": lon,
                "address": tags.get("addr:street"),
                "source": "OpenStreetMap / Overpass",
            }
        )
    return items


def fetch_open_charge_map_stations() -> list[dict[str, Any]]:
    params = {
        "output": "json",
        "countrycode": "DE",
        "latitude": 49.9929,
        "longitude": 8.2473,
        "distance": 20,
        "distanceunit": "KM",
        "maxresults": 500,
    }
    try:
        data = _safe_get("https://api.openchargemap.io/v3/poi", params=params)
    except Exception:
        return []

    items: list[dict[str, Any]] = []
    for row in data:
        addr = row.get("AddressInfo", {})
        op = row.get("OperatorInfo", {})
        lat = addr.get("Latitude")
        lon = addr.get("Longitude")
        if lat is None or lon is None:
            continue
        items.append(
            {
                "id": f"ocm-{row.get('ID')}",
                "name": addr.get("Title") or "Ladepunkt (OpenChargeMap)",
                "operator": op.get("Title"),
                "lat": lat,
                "lon": lon,
                "address": addr.get("AddressLine1"),
                "source": "OpenChargeMap",
            }
        )
    return items
