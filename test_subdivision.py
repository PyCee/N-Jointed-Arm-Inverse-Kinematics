import unittest
from vector import Vector
from arc import Arc
from sweep import get_swept_arc_subdivisions

from math import pi

d_0 = 0.0
d_180 = pi
d_360 = d_180 * 2.0
d_90 = d_180 / 2.0
d_45 = d_180 / 4.0
d_30 = d_180 / 6.0
d_15 = d_180 / 12.0
d_135 = d_45 * 3.0

class TestSubdivisionMethods(unittest.TestCase):
    def assert_subdiv_equal(self, arc, index, offset_length, sweep_radians, result):
        arcs = get_swept_arc_subdivisions(arc, index, offset_length, sweep_radians)
        self.assertEqual(arcs, result)
        
    def test_no_subdivision(self):
        self.assert_subdiv_equal(Arc(Vector(0.0, 0.0), 1.0, (d_0, d_180)),
                                 0, 1.0, d_45,
                                 (Arc(Vector(0.0, 0.0), 1.0, (d_0, d_180)), []))
    def test_no_subdivision_lim_deffer_from_extremes(self):
        self.assert_subdiv_equal(Arc(Vector(0.0, 0.0), 1.0, (d_45, d_180)),
                                 0, 1.0, d_45,
                                 (Arc(Vector(0.0, 0.0), 1.0, (d_45, d_180)), []))
    def test_subdivision_break(self):
        self.assert_subdiv_equal(Arc(Vector(0.0, 0.0), 1.0, (-d_45, d_180)),
                                 0, 1.0, d_90,
                                 (Arc(Vector(0.0, 0.0), 1.0, (d_45, d_180)),
                                   [Arc(Vector(1.0, 0.0), 1.0,
                                        (-0.7853981634, 0.0)),
                                    Arc(Vector(0.0, 0.0), 1.847759,
                                        (-0.3926990817, 0.3926990817))]))
    def test_subdivision_only_first_limit(self):
        self.assert_subdiv_equal(Arc(Vector(0.0, 0.0), 1.0, (-d_45, -d_135)),
                                 0, 1.0, d_90,
                                 (Arc(Vector(0.0, 0.0), 1.0,
                                       (d_45, -d_135)),
                                   [Arc(Vector(1.0, 0.0), 1.0,
                                        (-0.7853981634, 0.0)),
                                    Arc(Vector(0.0, 0.0), 1.847759,
                                        (-0.3926990817, 0.3926990817))]))
    def test_subdivision_no_break(self):
        self.assert_subdiv_equal(Arc(Vector(0.0, 0.0), 1.0, (-d_45, d_180)),
                                 0, 1.0, d_15,
                                 (Arc(Vector(0.0, 0.0), 1.0,
                                      (0.2617993878, d_180)),
                                  [Arc(Vector(1.0, 0.0), 1.0,
                                       (-0.7853981634, 0.0)),
                                   Arc(Vector(0.0, 0.0), 1.847759,
                                       (-0.3926990817, -0.1308996939)),
                                   Arc(Vector(0.966, 0.259), 1.0,
                                       (-0.5235987756, 0.0))]))
    def test_subdivision_no_break_floating_point_error(self):
        self.assert_subdiv_equal(Arc(Vector(0.0, 0.0), 1.0, (-d_45, d_180)),
                                 0, 1.0, d_45,
                                 (Arc(Vector(0.0, 0.0), 1.0, (d_45, d_180)),
                                  [Arc(Vector(1.0, 0.0), 1.0,
                                       (-0.7853981634, 0.0)),
                                   Arc(Vector(0.0, 0.0), 1.847759,
                                       (-0.3926990817, 0.3926990817))]))
    def test_subdivision_second_limit(self):
        self.assert_subdiv_equal(Arc(Vector(0.0, 0.0), 1.0, (d_0, -d_90)),
                                 1, 1.0, d_90,
                                 (Arc(Vector(0.0, 0.0), 1.0,
                                      (0.0, d_90)),
                                  [Arc(Vector(1.0, 0.0), 1.0,
                                       (-3.1415926536, -1.5707963268)),
                                   Arc(Vector(0.0, 0.0), 1.414214,
                                       (-0.7853981634, 0.7853981634))]))
    def test_subdivision_second_limit_no_break(self):
        self.assert_subdiv_equal(Arc(Vector(0.0, 0.0), 1.0, (d_0, -d_135)),
                                 1, 1.0, d_15,
                                 (Arc(Vector(0.0, 0.0), 1.0, (0.0, 3.1415926)),
                                  [Arc(Vector(1.0, 0.0), 1.0,
                                       (3.1415926, -2.356194)),
                                   Arc(Vector(0.0, 0.0), 0.7653668,
                                       (-1.178097, -0.916297)),
                                   Arc(Vector(0.966, 0.259), 1.0,
                                       (-2.879793, -2.094395))]))
    def test_subdivision_first_limit_overridden(self):
        self.assert_subdiv_equal(Arc(Vector(0.0, 0.0), 1.0, (d_135, d_0)),
                                 0, 1.0, d_90,
                                 (Arc(Vector(0.0, 0.0), 1.0,
                                      (-3.1415926536, 0.0)),
                                  []))
    def test_subdivision_second_limit_overridden(self):
        self.assert_subdiv_equal(Arc(Vector(0.0, 0.0), 1.0, (d_180, d_45)),
                                 1, 1.0, d_90,
                                 (Arc(Vector(0.0, 0.0), 1.0,
                                      (-3.1415926536, 0.0)),
                                  []))
    def test_subdivision_lim_0_is_neg_lim_1(self):
        self.assert_subdiv_equal(Arc(Vector(0.0, 0.0), 1.0, (-d_45, d_45)),
                                 0, 1.0, d_90,
                                 (None,
                                  [Arc(Vector(1.0, 0.0), 1.0,
                                       (-0.7853981634, 0.0)),
                                   Arc(Vector(0.0, 0.0), 1.847759,
                                       (-0.3926990817, 0.3926990817))]))
        
