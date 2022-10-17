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


class Paddle(pygame.sprite.Sprite):

   def __init__(self, x, y, color, step=10): # Coordinates are for the CENTER of the sprite (NOT top right corner).

      super().__init__()

      self.step = step
      self.image = pygame.surface.Surface((SCREEN_W * 0.005, SCREEN_H * 0.15))
      self.image.fill(color)
      self.rect = self.image.get_rect(center=(x, y))


   def update(self):
      # Move the paddle up & down but limit range of motion to the play_area top and bottom edges
      if pygame.key.get_pressed()[pygame.K_UP]:
         self.rect.top = max((self.rect.top - self.step), background.play_area.top)
      elif pygame.key.get_pressed()[pygame.K_DOWN]:
         self.rect.bottom = min((self.rect.bottom + self.step), background.play_area.bottom)


background = Background(bg_color, light_grey)

player = pygame.sprite.GroupSingle()
player.add(Paddle(background.play_area.left + SCREEN_W * 0.005 * 3, background.play_area.centery, light_grey,
                  step=background.play_area.height * 0.01))

while True:
   for event in pygame.event.get():
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
         pygame.quit()
         sys.exit(0)

   background.draw_bg(screen)

   player.update()
   player.draw(screen)

   pygame.display.update()

   clock.tick(60)
