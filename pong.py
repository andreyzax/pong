#!/usr/bin/env python3

import sys
import pygame

SCREEN_W = 1920
SCREEN_H = 1200

pygame.init()

pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('pong')


clock = pygame.time.Clock()

while True:
   for event in pygame.event.get():
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
         pygame.quit()
         sys.exit(0)

   pygame.display.update()

   clock.tick(60)
