import pygame
import os
import numpy

os.environ["SDL_VIDEO_CENTERED"] = "1"

screen = pygame.display.set_mode((600, 600)) # the map
pygame.display.set_caption("TOWER DEFENSE")

move_right = 1
clock = pygame.time.Clock()


class GameMap():
	def __init__(self):
		self.


class Enemy(object):
	def __init__(self):
		self.rect = pygame.rect.Rect((0, 100, 20, 20))

	def move(self): # basic movement function, TODO: automatise (pathfinding)
		#"""
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
		#"""
           
		
	def drawEnemy(self, surface): # draw enemy
		pygame.draw.rect(screen, (0, 0, 0), self.rect)

pygame.init()

enemy = Enemy()
clock = pygame.time.Clock()

running = True       
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill((255, 255, 255))

	enemy.drawEnemy(screen)
	enemy.move()
	pygame.display.update()

	clock.tick(40)

pygame.quit()
