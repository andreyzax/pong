#!/usr/bin/env python3

import sys
import pygame

SCREEN_W = 1920
SCREEN_H = 1200

pygame.init()

pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('pong')
screen = pygame.display.get_surface()

bg_color = pygame.Color('grey 12')
light_grey = pygame.Color(200, 200, 200)

clock = pygame.time.Clock()

class Background:

   _instance = None
   _initialized = False

   def __new__(cls, *args):

      if cls._instance is None:    # Implement singalton pattern
         cls._instance = super().__new__(cls)

      return cls._instance


   def __init__(self, bg_color, border_color):

      if not self._initialized:   # Protect from mutiple calls to __init__()
         self._initialized = True
         self.bg_color = bg_color
         self.border_color = border_color
         self.border = pygame.Rect(SCREEN_W * 0.025, SCREEN_H * 0.025, SCREEN_W * 0.95, SCREEN_H * 0.95)
         self.play_area = pygame.Rect.inflate(self.border, -round(SCREEN_W * 0.005 * 2), -round(SCREEN_W * 0.005 * 2))


   def draw_bg(self, display):

      display.fill(self.bg_color)
      pygame.draw.rect(display, self.border_color, self.border, int(SCREEN_W * 0.005))
      #pygame.draw.rect(display,'Red',self.play_area,1)
      pygame.draw.line(display, self.border_color, self.border.midtop, self.border.midbottom, 3)

background = Background(bg_color, light_grey)

while True:
   for event in pygame.event.get():
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
         pygame.quit()
         sys.exit(0)

   background.draw_bg(screen)

   pygame.display.update()

   clock.tick(60)
