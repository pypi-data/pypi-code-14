"""TODO:
		Make this.
"""
from FGAme import *
from .number import *

class Player:
	def __init__(self):
		self.obj = world.add.circle(10, pos=pos.middle)
		self.obj.gravity = 500
		self.obj.damping = 1
		self.score = 0
		self.copied = []

	def update(self):
		self.score += 0.5
		# remove_num(self.copied)
		# for index, num in enumerate(str(int(self.score))):
		# 	self.copied.extend(print_num(int(num),(index*25, 0)))		