"""Command-line interface.

Subcommands share the top-level ``--config`` via a parent parser (argparse does
not inherit top-level args into subparsers automatically -- a historical pit).
"""
import argparse
import json
import sys

from .config import load_config
from .engine import DramaEngine


def _build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--config", default=None, help="path to config YAML")

    parser = argparse.ArgumentParser(prog="dramaforge", parents=[common])
    sub = parser.add_subparsers(dest="cmd")

    s = sub.add_parser("synth", parents=[common])
    s.add_argument("--text", required=True)
    s.add_argument("--direction", default=None)
    s.add_argument("--voice", default=None)
    s.add_argument("--emotion", default=None)
    s.add_argument("--out", default=None, help="save waveform to a WAV file")

    sub.add_parser("bench", parents=[common])

    sub.add_parser("serve", parents=[common])
    sub.add_parser("doctor", parents=[common])
    sub.add_parser("train", parents=[common])

    return parser


def main(argv=None):
    parser = _build_parser()
    args = parser.parse_args(argv)
    cfg = load_config(args.config)
    engine = DramaEngine(cfg)

    if args.cmd == "synth":
        r = engine.synth(args.text, direction=args.direction,
                         voice=args.voice, emotion=args.emotion)
        print(json.dumps(r.as_dict(), ensure_ascii=False, indent=2))
        if args.out:
            from .engine.audio import save_wav
            save_wav(args.out, r.waveform, r.sample_rate)
            print("wrote %s" % args.out)
    elif args.cmd == "bench":
        from .bench import run_all, summarize
        results = run_all(engine)
        print(summarize(results))
    elif args.cmd == "train":
        from .train import Trainer
        from .backends import get_backend
        backend = get_backend(cfg.model.name, cfg)
        t = Trainer(backend)
        print("skill before: %.4f" % backend.skill)
        hist = t.train(20)
        print("skill after:  %.4f" % backend.skill)
        print("monotonic: %s" % all(b <= a for b, a in hist))
    elif args.cmd == "serve":
        from .serving import run_server
        run_server(engine, cfg.serving.host, cfg.serving.port)
    elif args.cmd == "doctor":
        from .doctor import run_doctor
        run_doctor(cfg, engine)
    else:
        parser.print_help()
        sys.exit(1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
