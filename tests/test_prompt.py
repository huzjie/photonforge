# -*- coding: utf-8 -*-
import unittest

from photonforge.prompt import t5, clip, chunking, parser


class TestParser(unittest.TestCase):
    def test_weights(self):
        segs = parser.parse_weights("一只(柴犬:1.3)在雪地")
        self.assertTrue(any("柴犬" in s for s, _ in segs))
        self.assertTrue(any(w > 1.0 for _, w in segs))

    def test_strip(self):
        self.assertEqual(parser.strip_weighting("(柴犬:1.3)"), "柴犬")


class TestChunking(unittest.TestCase):
    def test_short(self):
        self.assertEqual(chunking.chunk_by_chars("短文本"), ["短文本"])

    def test_long(self):
        chunks = chunking.chunk_by_chars("词," * 400, chunk_size=512)
        self.assertGreater(len(chunks), 1)


class TestT5(unittest.TestCase):
    def test_encode_long(self):
        v = t5.encode_long("一只戴红围巾的柴犬" * 100)
        self.assertEqual(len(v), 64)

    def test_pool(self):
        v = t5.attention_pool([[1.0] * 4, [2.0] * 4], 4)
        self.assertEqual(len(v), 4)


class TestCLIP(unittest.TestCase):
    def test_similarity(self):
        v1 = clip.encode_text("狗")
        v2 = clip.encode_text("狗")
        self.assertGreater(clip.similarity(v1, v2), 0.9)


if __name__ == "__main__":
    unittest.main()
