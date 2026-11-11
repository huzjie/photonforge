# -*- coding: utf-8 -*-
import unittest

from photonforge.engine import pipeline, batch, doctor
from photonforge.engine.pipeline import GenerationPipeline


class TestPipeline(unittest.TestCase):
    def test_generate(self):
        p = GenerationPipeline()
        img = p.generate("一只柴犬", steps=2, width=64, height=64)
        self.assertEqual(len(img[0]), 64)

    def test_with_reference(self):
        p = GenerationPipeline()
        ref = [[[0.5] * 16 for _ in range(16)] for _ in range(3)]
        img = p.generate("风格迁移", reference_images=[ref], steps=2, width=32, height=32)
        self.assertEqual(len(img[0]), 32)


class TestBatch(unittest.TestCase):
    def test_drain(self):
        s = batch.BatchScheduler(max_batch_size=2)
        s.submit("a")
        s.submit("b")
        s.submit("c")
        self.assertEqual(s.drain(), ["a", "b"])
        self.assertEqual(s.drain(), ["c"])


class TestDoctor(unittest.TestCase):
    def test_all_pass(self):
        self.assertTrue(doctor.run_doctor(verbose=False))


if __name__ == "__main__":
    unittest.main()
