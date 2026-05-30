"""
MathLite API — servidor de backend sin dependencias web.

Expone los endpoints que consume el frontend:
- GET /api/health
- GET /api/tests
- POST /api/run
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from services.expression_service import ExpressionService
from services.testcase_service import list_tests


class MathLiteHandler(BaseHTTPRequestHandler):
    server_version = "MathLiteHTTP/1.0"

    def _set_headers(self, status: int = 200, content_type: str = "application/json") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _write_json(self, payload: Any, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._set_headers(status=status)
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._set_headers(status=204)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/api/health":
            self._write_json({"status": "ok", "service": "MathLite API"})
            return

        if self.path == "/api/tests":
            try:
                self._write_json(list_tests())
            except RuntimeError as exc:
                self._write_json({"detail": str(exc)}, status=503)
            return

        if self.path == "/":
            self._set_headers(status=200, content_type="text/plain; charset=utf-8")
            self.wfile.write(b"MathLite API")
            return

        self._write_json({"detail": "Not found"}, status=404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/run":
            self._write_json({"detail": "Not found"}, status=404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            payload = json.loads(raw_body.decode("utf-8"))
            code = payload.get("code", "")
            result = ExpressionService.execute(code)
            self._write_json(result)
        except json.JSONDecodeError:
            self._write_json({"detail": "Invalid JSON body"}, status=400)
        except Exception as exc:
            self._write_json({"detail": str(exc)}, status=500)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8000), MathLiteHandler)
    try:
        print("MathLite API running on http://0.0.0.0:8000")
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
