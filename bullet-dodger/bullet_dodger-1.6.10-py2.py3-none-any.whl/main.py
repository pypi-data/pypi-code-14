#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Bullet dodger: a game where you must dodge bullets
# Copyright (C) 2016 Jorge Maldonado Ventura

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pkg_resources import resource_filename
import math
import random

import pygame
from pygame.locals import *

from .block import *
from .bonus import Bonus
from .bullet import *
from .global_constants import *

pygame.init()
# Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
fullscreen = False
# Window titlebar
pygame.display.set_caption('Bullet dodger')
game_icon = resource_filename('bullet_dodger', 'assets/bullet.png')
pygame.display.set_icon(pygame.image.load(game_icon))
# Timing
fps_clock = pygame.time.Clock()
FPS = 60
# Preload resources
default_font = pygame.font.Font(None, 28)
ground_texture = resource_filename('bullet_dodger', 'assets/ground.png')
background_img = pygame.image.load(ground_texture)
bullet_fire_sound = resource_filename('bullet_dodger', 'assets/gun_fire.ogg')
game_music = resource_filename('bullet_dodger', 'assets/Hitman.ogg')
pygame.mixer.music.load(game_music)


def draw_repeating_background(background_img):
    background_rect = background_img.get_rect()
    background_rect_width = background_rect.width
    background_rect_height = background_rect.height
    for i in range(math.ceil(WIDTH / background_rect.width)):
        for j in range(math.ceil(HEIGHT / background_rect.height)):
            screen.blit(background_img, Rect(i * background_rect_width,
                                             j * background_rect_height,
                                             background_rect_width,
                                             background_rect_height))


def draw_text(text, font, surface, x, y, main_color, background_color=None):
    textobj = font.render(text, True, main_color, background_color)
    textrect = textobj.get_rect()
    textrect.centerx = x
    textrect.centery = y
    surface.blit(textobj, textrect)


def toggle_fullscreen():
    if pygame.display.get_driver() == 'x11':
        pygame.display.toggle_fullscreen()
    else:
        global screen, fullscreen
        screen_copy = screen.copy()
        if fullscreen:
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
        else:
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        fullscreen = not fullscreen
        screen.blit(screen_copy, (0, 0))


def start_screen():
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    in_start_screen = True
    while in_start_screen:
        title_font = pygame.font.Font('freesansbold.ttf', 65)
        big_font = pygame.font.Font(None, 36)
        default_font = pygame.font.Font(None, 28)
        draw_text('BULLET DODGER', title_font, screen,
                  WIDTH / 2, HEIGHT / 3, RED, YELLOW)
        draw_text('Use the mouse to dodge the bullets', big_font, screen,
                  WIDTH / 2, HEIGHT / 2, GREEN, BLACK)
        draw_text('Press any mouse button or S when you\'re ready',
                  default_font, screen, WIDTH / 2, HEIGHT / 1.7, GREEN, BLACK)
        draw_text('Press F11 to toggle full screen', default_font, screen,
                  WIDTH / 2, HEIGHT / 1.1, GREEN, BLACK)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                in_start_screen = False
                main_loop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    in_start_screen = False
                    main_loop()
                if event.key == K_F11:
                    toggle_fullscreen()
            if event.type == QUIT:
                in_start_screen = False


def main_loop():
    pygame.mixer.music.play(-1)
    pygame.mouse.set_visible(False)

    square = Block()
    square.set_pos(*pygame.mouse.get_pos())
    bullets = pygame.sprite.Group()
    bonuses = pygame.sprite.Group()
    running = True
    game_over = False
    points = 0
    min_bullet_speed = 1
    max_bullet_speed = 1
    bullets_per_gust = 1
    odds = 12

    while running:
        pygame.display.update()
        fps_clock.tick(FPS)
        draw_repeating_background(background_img)

        if points >= 2000:
            bullets_per_gust = 3000
            max_bullet_speed = 80
        elif points >= 1000:
            bullets_per_gust = 3
            min_bullet_speed = 3
            max_bullet_speed = 15
        elif points >= 800:
            max_bullet_speed = 20
        elif points >= 600:
            bullets_per_gust = 2
            max_bullet_speed = 10
        elif points >= 500:
            min_bullet_speed = 2
        elif points >= 400:
            max_bullet_speed = 8
        elif points >= 200:
            # The smaller this number is, the probability for a bullet
            # to be shot is higher
            odds = 8
            max_bullet_speed = 5
        elif points >= 100:
            odds = 9
            max_bullet_speed = 4
        elif points >= 60:
            odds = 10
            max_bullet_speed = 3
        elif points >= 30:
            odds = 11
            max_bullet_speed = 2

        if random.randint(1, odds) == 1:
            if random.randint(1, odds * 10) == 1:
                bonus = Bonus(random.randint(30, WIDTH - 30),
                              random.randint(30, HEIGHT - 30))
                bonuses.add(bonus)
            for _ in range(0, bullets_per_gust):
                bullets.add(random_bullet(random.randint(min_bullet_speed,
                                                         max_bullet_speed)))
                points += 1
        draw_text('{}  points'.format(points), default_font, screen,
                  WIDTH / 2, 20, GREEN)
        bullets.update()
        bonuses.update()
        bullets.draw(screen)
        bonuses.draw(screen)

        bonus = square.collide(bonuses)
        if square.collide(bullets):
            game_over = True
            sound = pygame.mixer.Sound(bullet_fire_sound)
            pygame.mixer.music.stop()
            sound.play()
        elif bonus:
            points += 10
            bonus.kill()

        screen.blit(square.img, square.rect)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] <= 10:
                    pygame.mouse.set_pos(WIDTH - 10, mouse_pos[1])
                elif mouse_pos[0] >= WIDTH - 10:
                    pygame.mouse.set_pos(0 + 10, mouse_pos[1])
                elif mouse_pos[1] <= 10:
                    pygame.mouse.set_pos(mouse_pos[0], HEIGHT - 10)
                elif mouse_pos[1] >= HEIGHT - 10:
                    pygame.mouse.set_pos(mouse_pos[0], 0 + 10)
                square.set_pos(*mouse_pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                random_x = random.randint(0, WIDTH)
                random_y = random.randint(0, HEIGHT)
                square.set_pos(random_x, random_y)
                pygame.mouse.set_pos([random_x, random_y])
            if event.type == QUIT:
                running = False

        while game_over:
            pygame.mouse.set_visible(True)
            # Text
            draw_text('{}  points'.format(points), default_font, screen,
                      WIDTH / 2, 20, GREEN)
            # Transparent surface
            transp_surf = pygame.Surface((WIDTH, HEIGHT))
            transp_surf.set_alpha(200)
            screen.blit(transp_surf, transp_surf.get_rect())

            draw_text('You lose', pygame.font.Font(None, 40), screen,
                      WIDTH / 2, HEIGHT / 3, RED)
            draw_text('To play again press C or any mouse button',
                      default_font, screen, WIDTH / 2, HEIGHT / 2.1, GREEN)
            draw_text('To quit the game press Q', default_font, screen,
                      WIDTH / 2, HEIGHT / 1.9, GREEN)
            draw_text('Press F11 to toggle full screen', default_font, screen,
                      WIDTH / 2, HEIGHT / 1.1, GREEN, BLACK)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_F11:
                        toggle_fullscreen()
                    if event.key == pygame.K_q:
                        game_over = False
                        running = False
                    elif event.key == pygame.K_c:
                        game_over = False
                        main_loop()
                        return  # Avoids recursion
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_over = False
                    main_loop()
                    return
                if event.type == QUIT:
                    game_over = False
                    running = False

if __name__ == '__main__':
    start_screen()
    pygame.quit()
