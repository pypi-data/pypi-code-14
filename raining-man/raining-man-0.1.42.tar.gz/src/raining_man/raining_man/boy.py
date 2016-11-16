from FGAme import *
import pygame

class Boy:

	def __init__(self):
		self.body = world.add.aabb(shape=(30,80), pos=(400, 100), mass=500)
		self.body_pygame = pygame.image.load('images/1.png')
		self.rect = [0, 0, 60, 60]
		self.position = [400, 100]
		self.k = 1.05

	def update(self):
		pass

	def move_p1(self, dx):
		self.position = [self.position[0] + dx, 100]
		self.body.pos = self.position