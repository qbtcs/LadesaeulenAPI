# LadesaeulenAPI Mainz

Interaktiver Webservice fuer oeffentliche Ladesaeulen in Mainz mit:

- Geolocation im Browser
- Zusammenfuehrung mehrerer oeffentlicher Kartenquellen
- Anbietername je Ladepunkt
- Oeffentlichem Preisrichtwert (AC/DC) je Anbieter

## Genutzte oeffentliche Kartenquellen

1. OpenStreetMap (Overpass API)
2. OpenChargeMap API

> Hinweis: "Alle oeffentlich verfuegbaren Karten" ist praktisch unbegrenzt. In dieser Version werden die wichtigsten offenen, ohne Login zugaenglichen Quellen zusammengefuehrt und dedupliziert.

## Start

```bash
uv sync
uv run app.py
```

Dann auf `http://localhost:8000` oeffnen.

## API

`GET /api/stations?lat=<float>&lon=<float>&radius_km=<float>`

Antwort enthaelt Ladepunkte, Quellen und Preisrichtwerte.

## Wichtige Annahme zu Preisen

Tarife sind Richtwerte aus oeffentlich abrufbaren Tarifseiten der Anbieter und **keine Live-Abrechnungspreise**.
