"""Local browser workbench. Offline by default; opt into live Foundry at startup."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
from urllib.parse import urlparse
from portfolio.registry import catalog, execute
from portfolio.ai import AIError

WEB = Path(__file__).resolve().parent / "web"
RUN_LOCK = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # Avoid logging client text or model output.

    def reply(self, code, body, mime="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/apps":
            return self.reply(200, {"apps": catalog(), "live_enabled": self.server.live})
        routes = {"/": ("index.html", "text/html; charset=utf-8"),
                  "/style.css": ("style.css", "text/css"), "/app.js": ("app.js", "application/javascript")}
        if path not in routes:
            return self.reply(404, {"error": "Not found"})
        name, mime = routes[path]
        self.reply(200, (WEB / name).read_bytes(), mime)

    def do_POST(self):
        # A local webpage cannot silently run your paid model from another origin.
        host = self.headers.get("Host", "")
        if host != f"127.0.0.1:{self.server.server_port}":
            return self.reply(403, {"error": "Invalid local host"})
        if self.headers.get("Origin") not in (None, "http://" + host):
            return self.reply(403, {"error": "Cross-origin request denied"})
        if self.headers.get("X-Portfolio-Request") != "1":
            return self.reply(403, {"error": "Missing application request header"})
        if urlparse(self.path).path != "/api/run":
            return self.reply(404, {"error": "Not found"})
        if not RUN_LOCK.acquire(blocking=False):
            return self.reply(429, {"error": "A run is in progress. Please wait."})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 100000:
                return self.reply(400, {"error": "Request size outside limits"})
            request = json.loads(self.rfile.read(length))
            if not isinstance(request, dict) or not isinstance(request.get("live", False), bool):
                raise ValueError("Invalid request")
            live = request.get("live", False)
            if live and not self.server.live:
                return self.reply(403, {"error": "Restart with --enable-live to allow Foundry inference"})
            result = execute(request["project"], request["payload"], live)
            self.reply(200, result)
        except (ValueError, KeyError, TypeError) as exc:
            self.reply(400, {"error": "Invalid input. Check the format and project example."})
        except AIError as exc:
            self.reply(502, {"error": str(exc)})
        except Exception:
            self.reply(500, {"error": "Application failed. Check the local terminal and tests."})
        finally:
            RUN_LOCK.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--enable-live", action="store_true")
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.live = args.enable_live
    print(f"AI portfolio workbench: http://127.0.0.1:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
