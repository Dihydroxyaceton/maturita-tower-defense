import pygame
import os

# the following imports wouldn't be needed if pyinstaller wasn't used
import maps.gamemap1
import maps.gamemap2
import maps.gamemap3

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init() #pygame initialisation

surface = pygame.display.set_mode((800, 600)) # screen initialisation

pygame.display.set_caption("TOWER DEFENSE LAUNCHER")

chosen_map = 0

running = True  

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			
		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y = pygame.mouse.get_pos()
			print(str(x), str(y))
			if y > 300 and x < 400:
				if x > 100 and x < 200:
					print ("Map 1")
					chosen_map = 1
					exec(open("tower_defense.py").read(), globals())
					running = False
					pygame.quit()
					sys.exit()
					break
				elif x > 300 and x < 400:
					print ("Map 2")
					chosen_map = 2
					exec(open("tower_defense.py").read(), globals())
				elif x > 500 and x < 600:
					print ("Map 3")
					chosen_map = 3
					exec(open("tower_defense.py").read(), globals())


	surface.fill((255, 255, 255))
	font = pygame.font.SysFont("calibri", 20)
	bigfont = pygame.font.SysFont("calibri", 50)
	surface.blit(bigfont.render("Tower defense launcher", 1, (0,0,0)), (150, 165))
	
	
	surface.blit(font.render("Map 1", 1, (0,0,0)), (150, 350))
	
	surface.blit(font.render("Map 2", 1, (0,0,0)), (350, 350))
	
	surface.blit(font.render("Map 3", 1, (0,0,0)), (550, 350))
	
	
	pygame.display.update()
	

pygame.quit()
