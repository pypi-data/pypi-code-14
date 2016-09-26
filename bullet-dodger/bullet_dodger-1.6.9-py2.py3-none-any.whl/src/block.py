#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

from global_constants import *


class Block(pygame.sprite.Sprite):
    def __init__(self):
        super(Block, self).__init__()
        self.img = pygame.Surface((30, 30))
        self.img.fill(YELLOW)
        self.rect = self.img.get_rect()
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery

    def set_pos(self, x, y):
        'Positions the block center in x and y location'
        self.rect.x = x - self.centerx
        self.rect.y = y - self.centery

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite
