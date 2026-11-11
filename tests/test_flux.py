# -*- coding: utf-8 -*-
import unittest

from photonforge.flux.base import MockVelocity, Trajectory
from photonforge.flux.euler import EulerSampler
from photonforge.flux.heun import HeunSampler
from photonforge.flux.rk4 import RK4Sampler
from photonforge.flux.dpm_solver import DPMSolverSampler
from photonforge.flux.dpmpp_2m import DPMPP2MSampler


class TestTrajectory(unittest.TestCase):
    def test_straight_line(self):
        tr = Trajectory(0.0, 1.0)
        self.assertAlmostEqual(tr.sample(0.0), 0.0)
        self.assertAlmostEqual(tr.sample(1.0), 1.0)
        self.assertAlmostEqual(tr.sample(0.5), 0.5)

    def test_list_latent(self):
        tr = Trajectory([0.0, 0.0], [2.0, 4.0])
        self.assertEqual(tr.sample(0.5), [1.0, 2.0])


class TestSamplers(unittest.TestCase):
    def test_euler_converges(self):
        s = EulerSampler(8)
        x = 0.0
        for t in s.schedule():
            x = s.step(x, t, MockVelocity(1.0), "c")
        self.assertGreater(x, 0.5)

    def test_heun_converges(self):
        s = HeunSampler(8)
        x = 0.0
        for t in s.schedule():
            x = s.step(x, t, MockVelocity(1.0), "c")
        self.assertGreater(x, 0.5)

    def test_rk4_converges(self):
        s = RK4Sampler(8)
        x = 0.0
        for t in s.schedule():
            x = s.step(x, t, MockVelocity(1.0), "c")
        self.assertGreater(x, 0.5)

    def test_dpm(self):
        s = DPMSolverSampler(8)
        x = 0.0
        for t in s.schedule():
            x = s.step(x, t, MockVelocity(1.0), "c")
        self.assertGreater(x, 0.5)

    def test_dpmpp_2m(self):
        s = DPMPP2MSampler(8)
        x = 0.0
        for t in s.schedule():
            x = s.step(x, t, MockVelocity(1.0), "c")
        self.assertGreater(x, 0.5)


if __name__ == "__main__":
    unittest.main()
