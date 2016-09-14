from shapely.ops import split

from . import unittest

from shapely.geometry import Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection
from shapely.ops import cascaded_union, linemerge

class TestSplitGeometry(unittest.TestCase):
	# helper class for testing below
	def helper(self, geom, splitter, expected_chunks):	
		s = split(geom, splitter)
		self.assertEqual(s.type, "GeometryCollection")
		self.assertEqual(len(s), expected_chunks)
		if expected_chunks > 1:
			# split --> expected collection that when merged is again equal to original geometry
			if s.geoms[0].type == 'LineString':
				self.assertTrue(linemerge(s).simplify(0.000001).equals(geom))
			elif s.geoms[0].type == 'Polygon':
				union = cascaded_union(s).simplify(0.000001)
				self.assertTrue(union.equals(geom))
				self.assertEqual(union.area, geom.area)
			else:
				raise ValueError
		elif expected_chunks == 1:
			# not split --> expected equal to line
			self.assertTrue(s[0].equals(geom))

class TestSplitPolygon(TestSplitGeometry):
	poly_simple = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
	poly_hole = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)], [[(0.5, 0.5), (0.5, 1.5), (1.5, 1.5), (1.5, 0.5), (0.5, 0.5)]])

	def test_split_poly_with_line(self):
		# crossing at 2 points --> return 2 segments
		splitter = LineString([(1, 3), (1, -3)])
		self.helper(self.poly_simple, splitter, 2)
		self.helper(self.poly_hole, splitter, 2)

		# touching the boundary--> return equal
		splitter = LineString([(0, 2), (5, 2)])
		self.helper(self.poly_simple, splitter, 1)
		self.helper(self.poly_hole, splitter, 1)

		# inside the polygon --> return equal
		splitter = LineString([(0.2, 0.2), (1.7, 1.7), (3, 2)])
		self.helper(self.poly_simple, splitter, 1)
		self.helper(self.poly_hole, splitter, 1)

		# outside the polygon --> return equal
		splitter = LineString([(0, 3), (3, 3) , (3, 0)])
		self.helper(self.poly_simple, splitter, 1)
		self.helper(self.poly_hole, splitter, 1)

	def test_split_poly_with_other(self):
		with self.assertRaises(ValueError):
			split(self.poly_simple, Point(1, 1))
		with self.assertRaises(ValueError):
			split(self.poly_simple, MultiPoint([(1, 1), (3, 4)]))
		with self.assertRaises(ValueError):
			split(self.poly_simple, self.poly_hole)

class TestSplitLine(TestSplitGeometry):
	ls = LineString([(0, 0), (1.5, 1.5), (3.0, 4.0)])

	def test_split_line_with_point(self):
		# point on line interior --> return 2 segments
		splitter = Point(1, 1)
		self.helper(self.ls, splitter, 2)

		# point on line point --> return 2 segments
		splitter = Point(1.5, 1.5)
		self.helper(self.ls, splitter, 2)

		# point on boundary --> return equal
		splitter = Point(3, 4)
		self.helper(self.ls, splitter, 1)

		# point on exterior of line --> return equal
		splitter = Point(2, 2)
		self.helper(self.ls, splitter, 1)

	def test_split_line_with_multipoint(self):
		# points on line interior --> return 4 segments
		splitter = MultiPoint([(1,1), (1.5, 1.5), (0.5, 0.5)])
		self.helper(self.ls, splitter, 4)

		# points on line interior and boundary -> return 2 segments
		splitter = MultiPoint([(1, 1), (3, 4)])
		self.helper(self.ls, splitter, 2)

		# point on linear interior but twice --> return 2 segments
		splitter = MultiPoint([(1, 1), (1.5, 1.5), (1, 1)])
		self.helper(self.ls, splitter, 3)

	def test_split_line_with_line(self):
		# crosses at one point --> return 2 segments
		splitter = LineString([(0, 1), (1, 0)])
		self.helper(self.ls, splitter, 2)	

		# crosses at two points --> return 3 segments
		splitter = LineString([(0, 1), (1, 0), (1, 2)])
		self.helper(self.ls, splitter, 3)

		# overlaps --> raise
		splitter = LineString([(0, 0), (15, 15)])
		with self.assertRaises(ValueError):
			self.helper(self.ls, splitter, 1)

		# does not cross --> return equal
		splitter = LineString([(0, 1), (0, 2)])
		self.helper(self.ls, splitter, 1)

		# is touching the boundary --> return equal
		splitter = LineString([(-1, 1), (1, -1)])
		self.assertTrue(splitter.touches(self.ls))
		self.helper(self.ls, splitter, 1)

	def test_split_line_with_multiline(self):
		# crosses at one point --> return 2 segments
		splitter = MultiLineString([[(0, 1), (1, 0)], [(0, 0), (2, -2)]])
		self.helper(self.ls, splitter, 2)	

		# crosses at two points --> return 3 segments
		splitter = MultiLineString([[(0, 1), (1, 0)], [(0, 2), (2, 0)]])
		self.helper(self.ls, splitter, 3)

		# crosses at three points --> return 4 segments
		splitter = MultiLineString([[(0, 1), (1, 0)], [(0, 2), (2, 0), (2.2, 3.2)]])
		self.helper(self.ls, splitter, 4)

		# overlaps --> raise
		splitter = MultiLineString([[(0, 0), (1.5, 1.5)], [(1.5, 1.5), (3, 4)]])
		with self.assertRaises(ValueError):
			self.helper(self.ls, splitter, 1)

		# does not cross --> return equal
		splitter = MultiLineString([[(0, 1), (0, 2)], [(1, 0), (2, 0)]])
		self.helper(self.ls, splitter, 1)

	def test_split_line_with_polygon(self):
		# crosses at two points --> return 3 segments
		splitter = Polygon([(1, 0), (1, 2), (2, 2), (2, 0), (1, 0)])
		self.helper(self.ls, splitter, 3)

		# crosses at one point and touches boundary --> return 2 segments
		splitter = Polygon([(0, 0), (1, 2), (2, 2), (1, 0), (0, 0)])
		self.helper(self.ls, splitter, 2)

		# exterior crosses at one point and touches at (0, 0)
		# interior crosses at two points
		splitter = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)], [[(0.5, 0.5), (0.5, 1.5), (1.5, 1.5), (1.5, 0.5), (0.5, 0.5)]])
		self.helper(self.ls, splitter, 4)

	def test_split_line_with_multipolygon(self):
		poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)]) # crosses at one point and touches at (0, 0)
		poly2 = Polygon([(0.5, 0.5), (0.5, 1.5), (1.5, 1.5), (1.5, 0.5), (0.5, 0.5)]) # crosses at two points
		poly3 = Polygon([(0, 0), (0, -2), (-2, -2), (-2, 0), (0, 0)]) # not crossing
		splitter = MultiPolygon([poly1, poly2, poly3])
		self.helper(self.ls, splitter, 4)

class TestSplitMulti(TestSplitGeometry):
	
	def test_split_multiline_with_point(self):
		# a cross-like multilinestring with a point in the middle --> return 4 line segments
		l1 = LineString([(0, 1), (2, 1)])
		l2 = LineString([(1, 0), (1, 2)])
		ml = MultiLineString([l1, l2])
		splitter = Point((1, 1))
		self.helper(ml, splitter, 4)
		
	def test_split_multiline_with_multipoint(self):
		# a cross-like multilinestring with a point in middle, a point on one of the lines and a point in the exterior 
		# --> return 4+1 line segments
		l1 = LineString([(0, 1), (3, 1)])
		l2 = LineString([(1, 0), (1, 2)])
		ml = MultiLineString([l1, l2])
		splitter = MultiPoint([(1, 1), (2, 1), (4, 2)])
		self.helper(ml, splitter, 5)
				
	def test_split_multipolygon_with_line(self):
		# two polygons with a crossing line --> return 4 triangles
		poly1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]) 
		poly2 = Polygon([(1, 1), (1, 2), (2, 2), (2, 1), (1, 1)])
		mpoly = MultiPolygon([poly1, poly2])
		ls = LineString([(-1, -1), (3, 3)])
		self.helper(mpoly, ls, 4)

		# two polygons away from the crossing line --> return identity
		poly1 = Polygon([(10, 10), (10, 11), (11, 11), (11, 10), (10, 10)]) 
		poly2 = Polygon([(-10, -10), (-10, -11), (-11, -11), (-11, -10), (-10, -10)])
		mpoly = MultiPolygon([poly1, poly2])
		ls = LineString([(-1, -1), (3, 3)])
		self.helper(mpoly, ls, 2)