# -*- coding: utf-8 -*-
"""RVQ audio codec demo: audio as a short token sequence."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dramaforge.codec import RVQCodec, reconstruction_error
from dramaforge.utils.hash import stable_vector


def main():
    for nq in (1, 2, 4, 8):
        codec = RVQCodec(n_quantizers=nq, codebook_size=256, dim=32)
        frames = [stable_vector("f%d" % i, 32) for i in range(40)]
        codes = codec.encode_frames(frames)
        dec = codec.decode_frames(codes)
        err = reconstruction_error(frames, dec)
        print("quantizers=%d -> %d tokens for %d frames, rmse=%.4f"
              % (nq, codec.token_count(len(frames)), len(frames), err))


if __name__ == "__main__":
    main()
