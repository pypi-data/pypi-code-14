# coding=utf-8

"""
"""

__author__ = "Morten Lind"
__copyright__ = "Morten Lind 2016"
__credits__ = ["Morten Lind"]
__license__ = "GPLv3"
__maintainer__ = "Morten Lind"
__email__ = "morten@lind.dyndns.dk"
__status__ = "Development"


import numpy as np
from math2d import Vector, Transform
from . import EPS


class Line:
    """A mathematic line, i.e. double infinite."""

    def __init__(self, start, end):
        self.start = Vector(start)
        self.end = Vector(end)
        Line._update(self)

    def _update(self):
        """Update derived data from changed fundamental data."""
        self.dir = self.end - self.start
        self.dir.normalize()

    def transform(self, trf):
        """Apply the given transform inline."""
        self.start = trf * self.start
        self.end  = trf * self.end
        Line._update(self)

    def __rmul__(self, trf):
        """Return the homogeneous transformed of this line."""
        if type(trf) == Transform:
            return Line(trf * self.start, trf * (self.start + self.dir))
        else:
            return NotImplemented

    def __repr__(self):
        return 'Line(p{}, d{})'.format(self.start.tolist(), self.end.tolist())

    def project(self, pos):
        """Return the projection of p onto the line"""
        return self.start + (pos - self.start) * self.dir * self.dir

    def __contains__(self, pos):
        """Test if 'pos' is on the line segment."""
        # Shortest dist vector must be of 0 length
        return (self.project(pos) - pos).norm < EPS

    def _l_intersect(self, ls):
        """http://stackoverflow.com/a/565282"""
        s = self
        o = ls
        s2o = o.start - s.start
        dcross = np.cross(s.dir, o.dir)
        if np.abs(dcross) < EPS:
            return []
        else:
            # The paramerers t for which the line intersection problem
            # matches the lines:
            st = np.cross(s2o, o.dir) / dcross
            return [s.start + st * s.delta]

    def intersection(self, other):
        if type(other) == Line:
            return self._l_intersect(self, other)
        else:
            return other.intersection(self)

    def dist(self, other):
        """Compute the distance to 'other'."""
        if type(other) == Vector:
            pp = self.project(other)
            return other.dist(pp)
        else:
            raise NotImplementedError


class LineSegment(Line):
    """A segment of a line."""

    def __init__(self, start, end):
        Line.__init__(self, start, end)
        LineSegment._update(self)

    def _update(self):
        """Update derived data from changed fundamental data."""
        self.delta = self.end - self.start
        self.length = self.delta.norm
        self.centre = self.start + 0.5 * self.delta

    @classmethod
    def new_from_dxf(cls, dxf_line):
        return LineSegment(dxf_line.start, dxf_line.end)

    def __contains__(self, p):
        """Test if 'p' is on the line segment."""
        pp = self.project(p)
        # Check if projection distance is different from 0, to some
        # level of precision
        if (pp - p).norm > EPS:
            return False
        pp_along = (pp - self.start) * self.dir / self.length
        if pp_along <= 1 and pp_along >= 0:
            return True
        else:
            return False

    def transform(self, trf):
        """Apply the given transform inline."""
        Line.transform(self, trf)
        LineSegment._update(self)

    def __rmul__(self, trf):
        """Return the homogeneously transformed of this line segment."""
        if type(trf) == Transform:
            return LineSegment(trf * self.start, trf * self.end)
        else:
            return NotImplemented

    def __repr__(self):
        return 'LineSegment({} -> {})'.format(self.start.tolist(),
                                              self.end.tolist())

    def dist(self, other):
        """Compute the distance to 'other'."""
        if type(other) == Vector:
            pp = self.project(other)
            if pp in self:
                return other.dist(pp)
            else:
                return min(other.dist(self.start), other.dist(self.end))
        else:
            raise NotImplementedError

    def _ls_intersect(self, ls):
        """http://stackoverflow.com/a/565282"""
        s = self
        o = ls
        s2o = o.start - s.start
        dcross = np.cross(s.delta, o.delta)
        if np.abs(dcross) < EPS:
            return []
        # The paramerers t for which the line intersection problem
        # matches the lines:
        st = np.cross(s2o, o.delta) / dcross
        if st < 0 or st > 1:
            return []
        ot = np.cross(s2o, s.delta) / dcross
        if ot >= 0 and ot <= 1:
            return [s.start + st * s.delta]
        else:
            return []

    def _l_intersect(self, l):
        """Based on http://stackoverflow.com/a/565282"""
        s = self
        o = l
        s2o = o.start - s.start
        dcross = np.cross(s.delta, o.dir)
        if np.abs(dcross) < EPS:
            return []
        # The paramerers t for which the line intersection problem
        # matches the lines:
        st = np.cross(s2o, o.dir) / dcross
        if st < 0 or st > 1:
            return []
        else:
            return [s.start + st * s.delta]

    def intersection(self, other):
        if type(other) == LineSegment:
            return self._ls_intersect(other)
        elif type(other) == Line:
            return self._l_intersect(other)
        else:
            return other.intersection(self)


class Circle:
    def __init__(self, centre, radius):
        self.centre = Vector(centre)
        self.radius = radius

    def transform(self, trf):
        """Apply the given transform inline."""
        self.centre = trf * self.centre

    def __rmul__(self, trf):
        """Return the homogeneously transformed of this circle."""
        if type(trf) == Transform:
            return Circle(trf * self.centre, self.radius)
        else:
            return NotImplemented

    def __repr__(self):
        return 'Circle(c{}, r[{}])'.format(self.centre.tolist(), self.radius)

    def _l_intersection(self, line):
        cp = line.project(self.centre)
        cp_dist = (cp - self.centre).norm
        xes = []
        if cp_dist < self.radius:
            # Two possibles: The half chords form triangles with a
            # radius and closest point vector
            hcl = np.sqrt(self.radius**2 - cp_dist**2)
            # This must be added and subtracted to the closes point
            # along the segment direction
            hc = hcl * line.dir
            xes = [cp + hc, cp - hc]
        elif cp_dist == self.radius:
            # one possible
            xes = [cp]
        return xes

    def __contains__(self, p):
        """Compute if p is on the circle."""
        return (p - self.centre).norm - self.radius < EPS

    def intersection(self, obj):
        if type(obj) == Line:
            return Circle._l_intersection(self, obj)
        else:
            return other.intersection(self)
        

class CircleSegment(Circle):
    def __init__(self, centre, radius, a_start, a_end):
        Circle.__init__(self, centre, radius)
        self.a0 = np.deg2rad(a_start)
        self.a1 = np.deg2rad(a_end)
        CircleSegment._update(self)

    def _update(self):
        """Update derived data from changed fundamental data."""
        self.start = self.centre + self.radius * Vector([np.cos(self.a0), np.sin(self.a0)])
        self.end = self.centre + self.radius * Vector([np.cos(self.a1), np.sin(self.a1)])
        self.chord = self.end - self.start

    def transform(self, trf):
        """Apply the given transform inline."""
        Circle.transform(self, trf)
        tang = trf.orient.angle
        self.a0 = (self.a0 + tang) % (2 * np.pi)
        self.a1 = (self.a1 + tang) % (2 * np.pi)
        CircleSegment._update(self)

    @classmethod
    def new_from_dxf(cls, dxf_arc):
        """Create a CircleSegment from a DXF Arc."""
        darc = dxf_arc
        return CircleSegment(darc.center, darc.radius,
                             darc.start_angle, darc.end_angle)

    def __contains__(self, p):
        """Evaluate if p is on the circle segment."""
        return (Circle.__contains__(self, p)
                and np.cross(self.chord, p-self.start) <= 0)

    def __rmul__(self, trf):
        """Return the homogeneously transformed of this circle segment."""
        if type(trf) == Transform:
            tang = trf.orient.angle
            a0 = (self.a0 + tang) % (2 * np.pi)
            a1 = (self.a1 + tang) % (2 * np.pi)
            return CircleSegment(trf * self.centre, self.radius, a0, a1)
        else:
            return NotImplemented

    def __repr__(self):
        return 'Circle(c{}, r[{}])'.format(self.centre.tolist(), self.radius)

    def _ls_intersection(self, ls):
        # First find possible line-circle collisions
        xposs = Circle.intersection(self, ls)
        # Filter points that are not on the circle segment
        return [x for x in xposs if x in self and x in ls]

    def _l_intersection(self, l):
        # First find possible line-circle collisions
        xposs = Circle.intersection(self, l)
        # Filter points that are not on the circle segment
        return [x for x in xposs if x in self]

    def intersection(self, other):
        if type(other) == LineSegment:
            return self._ls_intersection(other)
        elif type(other) == Line:
            return self._l_intersection(other)
        else:
            return other.intersection(self)
