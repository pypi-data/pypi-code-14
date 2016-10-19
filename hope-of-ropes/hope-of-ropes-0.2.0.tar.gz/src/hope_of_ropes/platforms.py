"""TODO:
		Make a list or something like that of platforms
"""

from FGAme import *

DEFAULT_RADIUS = 30
DEFAULT_MASS = 100000000

class Platforms:
	def __init__(self):
		self.items = []	

	def add(self, pos, radius=DEFAULT_RADIUS):
		platform = world.add.circle(30, pos=pos, mass=100000000)
		self.items.append(platform)

	def remove(self, remove_item):
		self.items.remove(remove_item)
		