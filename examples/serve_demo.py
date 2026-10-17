# -*- coding: utf-8 -*-
"""Start the HTTP server, then curl:
    curl -X POST http://127.0.0.1:8000/v1/audio/speech \
         -H 'Content-Type: application/json' \
         -d '{"text": "你好世界", "emotion": "gentle"}'
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dramaforge import Config
from dramaforge.serving import run_server
from dramaforge.engine import DramaEngine


def main():
    engine = DramaEngine(Config())
    run_server(engine, "127.0.0.1", 8000)


if __name__ == "__main__":
    main()
