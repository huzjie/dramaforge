"""A tiny OpenAI-style audio speech endpoint using only the stdlib.

Serves:
    GET  /health             -> engine/backend status
    GET  /v1/models          -> available backends
    POST /v1/audio/speech    -> {"text", "voice"?, "emotion"?, "direction"?}
                                -> audio metadata + downsampled samples
"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from ..engine import DramaEngine


class _Handler(BaseHTTPRequestHandler):
    engine = None

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._json({"status": "ok", "backend": self.engine.config.model.name})
        elif self.path == "/v1/models":
            from ..backends import list_backends
            self._json({"models": list_backends()})
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        if self.path != "/v1/audio/speech":
            self._json({"error": "not found"}, 404)
            return
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n) if n else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._json({"error": "invalid json"}, 400)
            return
        text = payload.get("text", "")
        if not text:
            self._json({"error": "text is required"}, 400)
            return
        r = self.engine.synth(text, direction=payload.get("direction"),
                              voice=payload.get("voice"),
                              emotion=payload.get("emotion"))
        # downsample the waveform for a JSON-safe preview
        step = max(1, len(r.waveform) // 512)
        samples = r.waveform[::step][:512]
        self._json({
            "sample_rate": r.sample_rate,
            "duration_s": round(r.duration_s, 3),
            "n_samples": len(r.waveform),
            "samples": [round(x, 4) for x in samples],
            "metadata": r.metadata,
        })

    def log_message(self, *args):
        pass


def create_server(engine, host="127.0.0.1", port=8000):
    _Handler.engine = engine
    return ThreadingHTTPServer((host, port), _Handler)


def run_server(engine, host="127.0.0.1", port=8000):
    srv = create_server(engine, host, port)
    print("dramaforge serving on http://%s:%d" % (host, port), flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
