#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pkg_resources import resource_stream
import random

from pygame.locals import *
import pygame

from .global_constants import WIDTH, HEIGHT

B_WIDTH = 10
B_HEIGHT = 13


def random_bullet(speed):
    random_or = random.randint(1, 4)
    if random_or == 1:  # Up -> Down
        return Bullet(random.randint(0, WIDTH), 0, 0, speed)
    elif random_or == 2:  # Right -> Left
        return Bullet(WIDTH, random.randint(0, HEIGHT), -speed, 0)
    elif random_or == 3:  # Down -> Up
        return Bullet(random.randint(0, WIDTH), HEIGHT, 0, -speed)
    elif random_or == 4:  # Left -> Right
        return Bullet(0, random.randint(0, HEIGHT), speed, 0)


class Bullet(pygame.sprite.Sprite):

    def __init__(self, xpos, ypos, hspeed, vspeed):
        super(Bullet, self).__init__()
        self.image = pygame.image.load(resource_stream('bullet_dodger',
                                                       'assets/bullet.png'))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.hspeed = hspeed
        self.vspeed = vspeed

        self.set_direction()

    def update(self):
        self.rect.x += self.hspeed
        self.rect.y += self.vspeed
        if self.collide():
            self.kill()

    def collide(self):
        if self.rect.x < 0 - B_WIDTH or self.rect.x > WIDTH:
            return True
        elif self.rect.y < 0 - B_HEIGHT or self.rect.y > HEIGHT:
            return True

    def set_direction(self):
        if self.hspeed > 0:
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.hspeed < 0:
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.vspeed > 0:
            self.image = pygame.transform.rotate(self.image, 180)
