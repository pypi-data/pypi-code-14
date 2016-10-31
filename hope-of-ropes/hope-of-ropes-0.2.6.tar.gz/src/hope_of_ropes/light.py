from FGAme import *
import math

f = draw.Poly(((0,0), (0, 600), (800, 600), (800, 0)))

EPS = 1e-6

class Light(object):
	def __init__(self, pos, size=5):
		self.obj = world.add.circle(size, pos=pos, color=(255, 255, 0), vel=(300,0))
		self.seg = []
		self.light_area = []
		self.points = []
		self.color = False

	def draw_lines(self):
		while len(self.seg) > 0:
			remove(self.seg[-1])
			self.seg.pop()

		if len(self.light_area) > 0 and self.color:
			remove(self.light_area)
			self.light_area = []

		lines = []
		vertices = []
		points = []
		rays = []		
		for obj in world:
			if hasattr(obj, 'vertices'):
				for index, vertice in enumerate(obj.vertices):
					index = (index+1)%len(obj.vertices)
					lines.append((vertice, obj.vertices[index]))
					vertices.append(vertice)

		for vertice in vertices:
			dist = vertice - self.obj.pos
			rays.append(dist)


		lines.append((Vec(0, 600), Vec(800, 600)))
		lines.append((Vec(0, 0), Vec(800, 0)))
		lines.append((Vec(0, 0), Vec(0, 600)))
		lines.append((Vec(800, 0), Vec(800, 600)))
		for index, ray in enumerate(rays):
			dist = ray
			for line in lines:
				x, y = line_intersection(line, (dist+self.obj.pos, self.obj.pos))
				if x != None and y != None:
					curr_distance = Vec(x, y) - self.obj.pos
					if curr_distance.norm() < dist.norm():
						dist = curr_distance
			point = self.obj.pos+dist

			for vertice in vertices:
				if math.fabs(point.x-vertice.x) < EPS and math.fabs(point.y-vertice.y) < EPS:
					rays.insert(index+1, ray.rotate((math.pi/180)*0.0001)*100)
					rays.insert(index+2, ray.rotate((math.pi/180)*-0.0001)*100)

			seg = draw.Segment(self.obj.pos+dist, self.obj.pos)
			self.seg.append(seg)
			world.add(seg)	
			points.append(point)

		points.sort(key=lambda p: math.atan2(p.y-self.obj.pos.y,p.x-self.obj.pos.x))

		if self.color:
			self.light_area = draw.Poly(points, color=(200, 200, 0))
			world.add(self.light_area)

	def switch(self):
		self.color = not self.color
		if self.color == True:
			world.add(f)
		else:
			remove(f)
			remove(self.light_area)
			self.light_area = []

	def update(self):
		self.draw_lines()

def remove(obj):
	rt = world._render_tree._data[0][1]
	world_objects = world._objects

	rt.remove(obj)
	world_objects.remove(obj)

def line_intersection(line1, line2):
	xdiff = Vec(line1[0].x - line1[1].x, line2[0].x - line2[1].x)
	ydiff = Vec(line1[0].y - line1[1].y, line2[0].y - line2[1].y)

	def det(a, b):
		return a[0] * b[1] - a[1] * b[0]

	div = det(xdiff, ydiff)
	if div == 0:
		return None, None
	q, c = line1
	s = c - q
	p, c = line2
	r = c - p

	t = q-p
	t = t.cross(s)
	t /= r.cross(s)

	u = q-p
	u = u.cross(r)
	u /= r.cross(s)

	d = (det(*line1), det(*line2))
	x = det(d, xdiff) / div
	y = det(d, ydiff) / div

	if r.cross(s) != 0 and t >= 0  and t <= 1 and u >= 0 and u <= 1:
		return x, y
	else:
		return None, None

	return 0, 0