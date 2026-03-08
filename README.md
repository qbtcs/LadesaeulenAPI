# LadesäulenAPI Mainz

Interaktiver Webservice für öffentliche Ladesäulen in Mainz mit:

- Geolocation im Browser
- Zusammenführung mehrerer öffentlicher Kartenquellen
- Anbietername je Ladepunkt
- öffentlichem Preisrichtwert (AC/DC) je Anbieter

## Genutzte öffentliche Kartenquellen

1. OpenStreetMap (Overpass API)
2. OpenChargeMap API

> Hinweis: "Alle öffentlich verfügbaren Karten" ist praktisch unbegrenzt. In dieser Version werden die wichtigsten offenen, ohne Login zugänglichen Quellen zusammengeführt und dedupliziert.

## Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Dann auf `http://localhost:8000` öffnen.

## API

`GET /api/stations?lat=<float>&lon=<float>&radius_km=<float>`

Antwort enthält Ladepunkte, Quellen und Preisrichtwerte.

## Wichtige Annahme zu Preisen

Tarife sind Richtwerte aus öffentlich abrufbaren Tarifseiten der Anbieter und **keine Live-Abrechnungspreise**.
