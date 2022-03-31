import pygame
import os
import sys


import maps.gamemap1
import maps.gamemap2
import maps.gamemap3
"""
imported maps not used directly in launcher file
necessary to include here so that Pyinstaller detects them as dependencies to succesfully create an exe file
"""

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init() #pygame initialisation

surface = pygame.display.set_mode((800, 630)) # screen initialisation

pygame.display.set_caption("TOWER DEFENSE LAUNCHER") # name of the window

chosen_map = 0

running = True  

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # closes window
			running = False
			
		if event.type == pygame.MOUSEBUTTONDOWN: # detects map selection
			x, y = pygame.mouse.get_pos()
			if y > 530 and y < 630: # checking coordinates of mouse click event
				if x > 100 and x < 200: 
					print ("Map 1 selected")
					chosen_map = 1
					exec(open("tower_defense.py").read(), globals()) # opening main tower defense file, sending global variables (chosen_map)
					pygame.display.quit()
					pygame.quit()
					sys.exit() # exit the launcher
				elif x > 300 and x < 400:
					print ("Map 2 selected")
					chosen_map = 2
					exec(open("tower_defense.py").read(), globals())
					pygame.display.quit()
					pygame.quit()
					sys.exit()
				elif x > 500 and x < 600:
					print ("Map 3 selected")
					chosen_map = 3
					exec(open("tower_defense.py").read(), globals())
					pygame.display.quit()
					pygame.quit()
					sys.exit()


	surface.fill((255, 255, 255)) # white surface
	
	font = pygame.font.SysFont("calibri", 20)
	bigfont = pygame.font.SysFont("calibri", 50)
	
	surface.blit(bigfont.render("Tower defense launcher", 1, (0,0,0)), (150, 10))
		
	tutorial_image = pygame.image.load("tutorial.png")
	surface.blit(tutorial_image, (180, 70))
	
	surface.blit(font.render("When ready to play, select a map:", 1, (0,0,0)), (250, 500))
	
	surface.blit(font.render("Map 1", 1, (0,0,0)), (150, 570))
	
	surface.blit(font.render("Map 2", 1, (0,0,0)), (350, 570))
	
	surface.blit(font.render("Map 3", 1, (0,0,0)), (550, 570))
	
	
	pygame.display.update()
	

pygame.quit()
