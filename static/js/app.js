const map = L.map('map').setView([49.9929, 8.2473], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap-Mitwirkende',
}).addTo(map);

let markerLayer = L.layerGroup().addTo(map);
const apiBaseUrl = (window.API_BASE_URL || '').replace(/\/$/, '');

function buildStationsUrl(query) {
  if (apiBaseUrl) {
    const url = new URL(`${apiBaseUrl}/api/stations`);
    url.search = query.toString();
    return url.toString();
  }

  const url = new URL('api/stations', window.location.href);
  url.search = query.toString();
  return url.toString();
}

async function loadStations(lat = null, lon = null) {
  const query = new URLSearchParams();
  if (lat !== null && lon !== null) {
    query.set('lat', lat);
    query.set('lon', lon);
    query.set('radius_km', '15');
  }

  const response = await fetch(buildStationsUrl(query));
  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`);
  }
  const data = await response.json();

  markerLayer.clearLayers();
  data.stations.forEach((s) => {
    const tariffText = s.tariff
      ? `<strong>${s.tariff.provider}</strong><br>AC: ${s.tariff.ac_eur_kwh ?? '-'} €/kWh<br>DC: ${s.tariff.dc_eur_kwh ?? '-'} €/kWh<br><a href="${s.tariff.source_url}" target="_blank">Tarifquelle</a>`
      : 'Kein öffentlicher Preis zuordenbar';

    const popup = `
      <strong>${s.name}</strong><br>
      Anbieter: ${s.operator ?? 'unbekannt'}<br>
      Distanz: ${s.distance_km} km<br>
      Quellen: ${s.sources.join(', ')}<br>
      ${tariffText}
    `;
    L.marker([s.lat, s.lon]).bindPopup(popup).addTo(markerLayer);
  });

  document.getElementById('stats').textContent = `${data.count} Ladepunkte gefunden (${data.sources_used.join(' + ')})`;
}

loadStations().catch(() => {
  document.getElementById('stats').textContent =
    'API nicht erreichbar. Fuer GitHub Pages bitte window.API_BASE_URL setzen.';
});

document.getElementById('locateBtn').addEventListener('click', () => {
  if (!navigator.geolocation) {
    alert('Geolocation wird nicht unterstützt.');
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const { latitude, longitude } = pos.coords;
      map.setView([latitude, longitude], 13);
      L.circleMarker([latitude, longitude], { radius: 8, color: '#0052a3' })
        .bindPopup('Ihr Standort')
        .addTo(map);
      loadStations(latitude, longitude).catch(() => {
        document.getElementById('stats').textContent =
          'API nicht erreichbar. Fuer GitHub Pages bitte window.API_BASE_URL setzen.';
      });
    },
    () => alert('Standort konnte nicht ermittelt werden.'),
    { enableHighAccuracy: true, timeout: 10000 }
  );
});
