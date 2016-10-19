"""TODO:
		Make this.
"""
from FGAme import *

class Player:
	def __init__(self):
		self.obj = world.add.circle(10, pos=pos.middle)
		self.obj.gravity = 500
		self.obj.damping = 1

