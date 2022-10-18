#!/usr/bin/env python3

from random import randint

import sys
import pygame

SCREEN_W = 1920
SCREEN_H = 1200

INITIAL_BALL_SPEED = 10.0
MAX_BALL_SPEED     = 20.0
MAX_BALL_YV        = 15.0

pygame.init()

pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('pong')
screen = pygame.display.get_surface()

bg_color = pygame.Color('grey 12')
light_grey = pygame.Color(175, 175, 175)

game_font = pygame.font.Font('fonts/bit5x3.ttf', SCREEN_H // 10)

clock = pygame.time.Clock()


score = 0

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
      pygame.draw.line(display, self.border_color, self.play_area.midtop, self.play_area.midbottom, 3)


class Paddle(pygame.sprite.Sprite):

   right_nv  = pygame.Vector2(-1,0)
   left_nv   = pygame.Vector2(1,0)

   def __init__(self, x, y, collision_normal, color, step=10): # Coordinates are for the CENTER of the sprite (NOT top right corner).

      super().__init__()

      self.step = step
      self.image = pygame.surface.Surface((SCREEN_W * 0.005, SCREEN_H * 0.15))
      self.image.fill(color)
      self.rect = self.image.get_rect(center=(x, y))
      self.nv = collision_normal
      self.velocity_y = 0


   def _is_mouse_virtual(self):

      return (not pygame.mouse.get_visible()) and pygame.event.get_grab()


   def _mouse_vert_movment(self):

      y_delta = 0
      if self._is_mouse_virtual():
         _, y_delta = pygame.mouse.get_rel()

      return y_delta


   def update(self):
      # Move the paddle up & down but limit range of motion to the play_area top and bottom edges
      if pygame.key.get_pressed()[pygame.K_UP]:
         self.rect.top = max((self.rect.top - self.step), background.play_area.top)
         self.velocity_y = -self.step
      elif pygame.key.get_pressed()[pygame.K_DOWN]:
         self.rect.bottom = min((self.rect.bottom + self.step), background.play_area.bottom)
         self.velocity_y = self.step
      else: # This being here means that keyboard input gets priority over mouse input
         mouse_y = self._mouse_vert_movment()
         self.velocity_y = self.step * mouse_y * 0.08
         if mouse_y == 0:
            pass
         elif mouse_y < 0:
            self.rect.top = max((self.rect.top + self.step * mouse_y * 0.08), background.play_area.top)
         elif mouse_y > 0:
            self.rect.bottom = min((self.rect.bottom + self.step * mouse_y * 0.08), background.play_area.bottom)


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

      global score

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

      # Check for collisions with the player
      if paddle := pygame.sprite.spritecollideany(self, player): # ':=' is a new python 3.8 operator, it does excatly what it looks it's doing
         score += 1
         self.velocity.reflect_ip(paddle.nv)
         self.velocity.y += min(paddle.velocity_y, MAX_BALL_YV, key=abs) # This limit is mostly for playability, the game runs fine without this limit
                                                                         # but trying to hit the ball when it's moving nearly verticly is very hard.

         self.velocity.scale_to_length(min(MAX_BALL_SPEED, self.velocity.length())) # Make sure to limit the speed (our collision logic doesn't handle high speeds well)
                                                                                    # We are doing this here since this is the only place we actually *change* the magnitude of the
                                                                                    # velocity vector (aka the speed). All other collsions just change it's direction
         #print(self.velocity.length())

         self.postion += self.velocity # Same here as in the border collison checks, prevents overshooting, ball getting "stuck" in a collision state


background = Background(bg_color, light_grey)

player = pygame.sprite.GroupSingle()
player.add(Paddle(background.play_area.left + SCREEN_W * 0.005 * 3, background.play_area.centery, Paddle.left_nv ,light_grey,
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
      elif event.type == pygame.MOUSEBUTTONDOWN:
         pygame.event.set_grab(True)
         pygame.mouse.set_visible(False)
      elif event.type == pygame.MOUSEBUTTONUP:
         pygame.event.set_grab(False)
         pygame.mouse.set_visible(True)

   background.draw_bg(screen)

   player.update()
   player.draw(screen)

   ball.update()
   ball.draw(screen)

   score_surf = game_font.render(f'{score:02}', False, light_grey)
   score_rect = score_surf.get_rect(centerx=background.play_area.centerx * 0.9, centery=background.play_area.top + 100)
   screen.blit(score_surf, score_rect)

   pygame.display.update()

   clock.tick(60)
