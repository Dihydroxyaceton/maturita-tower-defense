import os
import random
import pygame
import math
import sys

os.environ["SDL_VIDEO_CENTERED"] = "1"

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("TOWER DEFENSE")

clock = pygame.time.Clock()

class Player(object):
    def __init__(self):
        self.rect = pygame.rect.Rect((64, 54, 16, 16))

    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = 1
        if key[pygame.K_LEFT]:
           self.rect.move_ip(-1, 0)
        if key[pygame.K_RIGHT]:
           self.rect.move_ip(1, 0)
        if key[pygame.K_UP]:
           self.rect.move_ip(0, -1)
        if key[pygame.K_DOWN]:
           self.rect.move_ip(0, 1)

    def draw(self, surface):
        pygame.draw.rect(screen, (0, 0, 128), self.rect)

pygame.init()

player = Player()
clock = pygame.time.Clock()

running = True       
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((255, 255, 255))

    player.draw(screen)
    player.handle_keys()
    pygame.display.update()

    clock.tick(40)

pygame.quit()
