"""RVQ codec round-trip."""
import unittest

from dramaforge.codec import RVQCodec, reconstruction_error
from dramaforge.utils.hash import stable_vector


class TestCodec(unittest.TestCase):
    def test_round_trip_shape(self):
        codec = RVQCodec(n_quantizers=4, codebook_size=256, dim=32)
        frames = [stable_vector("f%d" % i, 32) for i in range(8)]
        codes = codec.encode_frames(frames)
        self.assertEqual(len(codes), 8)
        self.assertEqual(len(codes[0]), 4)
        decoded = codec.decode_frames(codes)
        self.assertEqual(len(decoded), 8)
        self.assertEqual(len(decoded[0]), 32)

    def test_more_quantizers_lower_error(self):
        frames = [stable_vector("g%d" % i, 16) for i in range(8)]
        c2 = RVQCodec(2, 128, 16)
        c8 = RVQCodec(8, 128, 16)
        e2 = reconstruction_error(frames, c2.decode_frames(c2.encode_frames(frames)))
        e8 = reconstruction_error(frames, c8.decode_frames(c8.encode_frames(frames)))
        self.assertLessEqual(e8, e2)


if __name__ == "__main__":
    unittest.main()
