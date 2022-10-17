#!/usr/bin/env python3

import pygame


pygame.init()

pygame.display.set_mode((1200,800))
pygame.display.set_caption('PyGame')

clock = pygame.time.Clock()

while True:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()
         exit(0)

   pygame.display.update()

   clock.tick(60)
