# -*- coding: utf-8 -*-
import unittest

from photonforge.providers.base import get_provider
from photonforge.providers import mock


class TestProviders(unittest.TestCase):
    def test_get_mock(self):
        p = get_provider("mock")
        self.assertEqual(p.name, "mock")

    def test_unknown(self):
        with self.assertRaises(KeyError):
            get_provider("nonexistent")

    def test_mock_generate(self):
        p = mock.MockProvider()
        img = p.generate("一只柴犬", steps=2, width=32, height=32)
        self.assertEqual(len(img[0]), 32)


if __name__ == "__main__":
    unittest.main()
