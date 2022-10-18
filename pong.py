#!/usr/bin/env python3

from random import randint

import sys
import pygame

SCREEN_W = 1920
SCREEN_H = 1200

INITIAL_BALL_SPEED = 10

pygame.init()

pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('pong')
screen = pygame.display.get_surface()

bg_color = pygame.Color('grey 12')
light_grey = pygame.Color(175, 175, 175)

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


class Ball(pygame.sprite.Sprite):

   top_nv    = pygame.Vector2(0,-1)
   bottom_nv = pygame.Vector2(0,1)
   right_nv  = pygame.Vector2(-1,0)
   left_nv   = pygame.Vector2(1,0)

   def __init__(self, postion, velocity, color):

      super().__init__()

      self.postion = postion
      self.velocity = velocity

      self.image = pygame.Surface((20,20))
      self.image.fill(color)
      self.rect = self.image.get_rect( center=(round(postion.x), round(postion.y)) )


   def update(self):
      self.postion += self.velocity
      self.rect.center = (round(self.postion.x), round(self.postion.y))

      # Check for collisions with play area border
      if self.rect.colliderect(background.play_area):
         if self.rect.top <= background.play_area.top:
            self.velocity.reflect_ip(self.top_nv)
            self.postion += self.velocity  # After reflecting the ball velocity away from the edge we immediatly move the ball one "step"
                                           # We do this here and in the other collision check clauses to avoid the ball overshooting the game area and getting stuck outside of it
         elif self.rect.bottom >= background.play_area.bottom:
            self.velocity.reflect_ip(self.bottom_nv)
            self.postion += self.velocity
         elif self.rect.right >= background.play_area.right:
            self.velocity.reflect_ip(self.right_nv)
            self.postion += self.velocity
         elif self.rect.left <= background.play_area.left:
            self.velocity.reflect_ip(self.left_nv)
            self.postion += self.velocity


background = Background(bg_color, light_grey)

player = pygame.sprite.GroupSingle()
player.add(Paddle(background.play_area.left + SCREEN_W * 0.005 * 3, background.play_area.centery, light_grey,
                  step=background.play_area.height * 0.01))

# Randomize intial ball velocity
ball_velocity = pygame.Vector2(INITIAL_BALL_SPEED,0)
ball_velocity.rotate_ip(randint(0, 360))

ball = pygame.sprite.GroupSingle()
ball.add(Ball(pygame.Vector2(background.play_area.center), ball_velocity, light_grey))

while True:
   for event in pygame.event.get():
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
         pygame.quit()
         sys.exit(0)

   background.draw_bg(screen)

   player.update()
   player.draw(screen)

   ball.update()
   ball.draw(screen)

   pygame.display.update()

   clock.tick(60)
