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

## Deployment auf GitHub Pages

Dieses Repository enthaelt jetzt einen Workflow unter `.github/workflows/deploy-pages.yml`,
der beim Push auf `main` automatisch auf GitHub Pages deployed.

Wichtig: GitHub Pages hostet nur statische Dateien. Der Python-Endpunkt
`/api/stations` laeuft dort nicht.

Damit die Seite auf Pages Daten laden kann:

1. Backend (diese Python-App) separat hosten (z. B. Render, Fly.io, Railway, eigener Server).
2. In `templates/index.html` den Wert von `window.API_BASE_URL` auf die Backend-URL setzen, z. B.:
   `window.API_BASE_URL = "https://your-api.example.com";`
3. Aenderung committen und nach `main` pushen.

Wenn `window.API_BASE_URL` leer ist und keine lokale API verfuegbar ist, zeigt die Seite einen Hinweis an.
