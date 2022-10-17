#!/usr/bin/env python3

import pygame

SCREEN_W = 1920
SCREEN_H = 1200

pygame.init()

pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('pong')


clock = pygame.time.Clock()

while True:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()
         exit(0)

   pygame.display.update()

   clock.tick(60)
