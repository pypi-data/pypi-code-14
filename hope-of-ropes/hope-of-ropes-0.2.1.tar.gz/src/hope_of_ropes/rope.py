"""TODO:
		Make a throwable rope, because right now it instantly appear out of thin air
            After making that, limit the number of ropes thrown to one at a time
        Name better those parameters. Or not. I dont know.
"""

from FGAme import *
from FGAme.physics.collision import get_collision, Collision
from math import fabs
from math import log

from FGAme.mathtools import Vec2, sin, pi, shapes, shadow_y, \
    shadow_x
from FGAme.physics.bodies import Body, AABB, Circle
from FGAme.physics.collision import get_collision, Collision, DEFAULT_DIRECTIONS
from smallshapes import aabb_coords
from smallshapes import area, clip, center_of_mass, ROG_sqr
from smallvectors import dot, Rotation2d

DEFAULT_SHAPE_X = 5
DEFAULT_ROPE_LENGTH = 200
DEFAULT_K = 5000

class Rope(World):
	"""
	Rope objects does not have collisions
	"""
	def __init__(self, player, \
				 length=DEFAULT_ROPE_LENGTH, k=DEFAULT_K):
		self.platform = None
		self.obj = None
		self.player = player
		self.length = length
		self.k = k

	def connect(self, platform):
		self.platform = platform
		self.create()

	def create(self):
		starting_position = self.player.pos
		ending_position = self.platform.pos

		self.dist = starting_position - ending_position
		if fabs(self.dist.norm()) <= 1:
			self.dist = 1
		
		self.obj = world.add.rectangle(shape=(1000/((self.dist.norm())), -self.dist.norm()), \
									   pos=starting_position - self.dist/2, color=(255, 0, 0))	
		self.obj.is_rope = True
		self.rotate()

	def rotate(self):
		starting_position = self.player.pos
		ending_position = self.platform.pos

		if ending_position.x > starting_position.x:
			self.obj.rotate(angle(Vec(0, 1), self.dist))
		else:
			self.obj.rotate(angle(Vec(0, -1), self.dist))

	def update(self):
		if self.platform != None:
			self.remove()
			self.create()

			dist = self.platform.pos - self.player.pos
			direction = dist - dist.normalize()*self.length
			direction *= self.k

			self.player.force = lambda t: direction

	def remove(self):
		world.remove(self.obj)
		self.player.force = lambda t: self.player.gravity
		
def angle(v1, v2):
	return math.acos(v1.dot(v2)/(v1.norm()*v2.norm()))

@get_collision.overload([Poly, Poly])
def collision_poly(A, B, directions=None, collision_class=Collision):
	"""
	Collision detection using SAT.
	"""

	if (hasattr(A, 'is_rope') or hasattr(B, 'is_rope')):
		return None

	# List of directions from normals
	if directions is None:
		if A.num_normals + B.num_normals < 9:
			directions = A.get_normals() + B.get_normals()
		else:
			directions = DEFAULT_DIRECTIONS

	# Test overlap in all considered directions and picks the smaller
	# penetration
	min_overlap = float('inf')
	norm = None
	for u in directions:
		A_coords = [dot(pt, u) for pt in A.vertices]
		B_coords = [dot(pt, u) for pt in B.vertices]
		Amax, Amin = max(A_coords), min(A_coords)
		Bmax, Bmin = max(B_coords), min(B_coords)
		minmax, maxmin = min(Amax, Bmax), max(Amin, Bmin)
		overlap = minmax - maxmin
		if overlap < 0:
			return None
		elif overlap < min_overlap:
			min_overlap = overlap
			norm = u

	# Finds the correct direction for the normal
	if dot(A.pos, norm) > dot(B.pos, norm):
		norm = -norm

	# Computes the clipped polygon: collision happens at its center point.
	try:
		clipped = clip(A.vertices, B.vertices)
		col_pt = center_of_mass(clipped)
	except ValueError:
		return None

	if area(clipped) == 0:
		return None

	return collision_class(A, B, pos=col_pt, normal=norm, delta=min_overlap)


@get_collision.overload([AABB, Poly])
def aabb_poly(A, B, collision_class=Collision):
	if (hasattr(A, 'is_rope') or hasattr(B, 'is_rope')):
		return None

	if shadow_x(A, B) < 0 or shadow_y(A, B) < 0:
		return None

	A_poly = Rectangle(A.rect_coords)
	col = collision_poly(A_poly, B)
	if col is not None:
		return collision_class(A, B, pos=col.pos, normal=col.normal,
							   delta=col.delta)
	else:
		return None


@get_collision.overload([Circle, Poly])
def circle_poly(A, B, collision_class=Collision):
	if (hasattr(A, 'is_rope') or hasattr(B, 'is_rope')):
		return None
	if shadow_x(A, B) < 0 or shadow_y(A, B) < 0:
		return None

	# Searches for the nearest point to B
	vertices = B.vertices
	center = A.pos
	normals = [(i, v - center, v) for i, v in enumerate(vertices)]
	idx, _, pos = min(normals, key=lambda x: x[1].norm())

	# The smaller distance to the center can be vertex-center or side-center.
	# We need to detect this.
	separation = (pos - center).norm()

	# Verify each face
	P0 = pos
	N = len(vertices)
	for idx in [(idx - 1) % N, (idx + 1) % N]:
		P = vertices[idx]
		v = center - P
		u = P0 - P
		L = u.norm()
		distance = abs(v.cross(u) / L)

		# Verify if closest point is inside segment
		if distance < separation and u.dot(v) < L ** 2:
			pos = P + (u.dot(v) / L ** 2) * u
			separation = distance

	# Verify if there is collision in the direction of smaller separation
	delta = A.radius - separation
	normal = (pos - center).normalize()

	if delta > 0:
		return collision_class(A, B, pos=pos, normal=normal, delta=delta)
	else:
		return None


@get_collision.overload([Poly, Circle])
def poly_circle(A, B, collision_class=Collision):

	return circle_poly(B, A, collision_class=Collision)


@get_collision.overload([Poly, AABB])
def poly_aabb(A, B, collision_class=Collision):

	return aabb_poly(B, A, collision_class=Collision)