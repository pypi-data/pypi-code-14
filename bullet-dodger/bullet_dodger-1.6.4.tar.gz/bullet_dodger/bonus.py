#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

from bullet_dodger.global_constants import RED

class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bonus, self).__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.centerx
        self.rect.y = y - self.rect.centery
