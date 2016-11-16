from FGAme import *
import pygame
import os
from raining_man.images import *

class Boy:
    def __init__(self):

        _ROOT = os.path.abspath(os.path.dirname(__file__))
        absolute_image_path = os.path.join(_ROOT, 'images/1.png')

        self.body = world.add.aabb(shape=(30,80), pos=(400, 100), mass=500)
        self.body_pygame = pygame.image.load(absolute_image_path)
        self.rect = [0, 0, 60, 60]
        self.position = [400, 100]
        self.k = 1.05

    def update(self):
        pass

    def move_p1(self, dx):
        self.position = [self.position[0] + dx, 100]
        self.body.pos = self.position
