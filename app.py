from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from src.aggregator import aggregate_stations

BASE_DIR = Path(__file__).parent


class AppHandler(BaseHTTPRequestHandler):
    def _send(self, body: bytes, content_type: str = "text/html", status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            index = (BASE_DIR / "templates" / "index.html").read_bytes()
            return self._send(index)

        if path.startswith("/static/"):
            file_path = BASE_DIR / path.lstrip("/")
            if not file_path.exists():
                return self._send(b"Not Found", "text/plain", 404)
            content_type = "text/plain"
            if file_path.suffix == ".css":
                content_type = "text/css"
            elif file_path.suffix == ".js":
                content_type = "application/javascript"
            return self._send(file_path.read_bytes(), content_type)

        if path == "/api/stations":
            query = parse_qs(parsed.query)
            lat = _to_float(query.get("lat", [None])[0])
            lon = _to_float(query.get("lon", [None])[0])
            radius = _to_float(query.get("radius_km", [12])[0]) or 12
            payload = aggregate_stations(center_lat=lat, center_lon=lon, radius_km=radius)
            return self._send(json.dumps(payload).encode("utf-8"), "application/json")

        return self._send(b"Not Found", "text/plain", 404)


def _to_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def run() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", 8000), AppHandler)
    print("Server running on http://0.0.0.0:8000")
    server.serve_forever()


if __name__ == "__main__":
    run()
