"""vmkit-test-minimal — one-file stdlib HTTP server.

Single-process, single-threaded, no framework. The point is to be the
*smallest* thing the scanner can still pattern-match as 'this is a Python
service'. Anything VMKit can deploy beyond this proves the toolchain
isn't quietly requiring a fastapi/flask/django import to work.
"""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 — required override name
        if self.path == "/health":
            self._respond(200, b"ok\n")
        elif self.path == "/":
            self._respond(200, b"vmkit-test-minimal\n")
        else:
            self._respond(404, b"not found\n")

    def _respond(self, status: int, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args: object) -> None:
        # Quiet the default access log; structured-log replacement is out of
        # scope for a test fixture.
        return


def main() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", 8000), Handler)  # noqa: S104
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
