import pygame
import os
import numpy
import math
from random import randint

""" 
classes:

  enemy
    attributes: health, movement speed, type (hidden / air / ...), location, size
    methodes: movement, detecting and obtaining damage, spawning, despawning
    
  game (player)
    attributes: health, map, money
    methodes: detecting and obtaining damage
    
  tower
    attributes: type, cadency, cost, name, location
    methodes: firing
  
  bullet
    attributes: type, damage, location
    methodes: dealing damage
    
    
    
    
    
    
https://www.youtube.com/watch?v=TqbtxBntuF0&t=105s    
    
"""



# defining images for enemies and towers:

enemy_type3 = pygame.image.load('enemies/kubelwagen_right.png')
enemy_type3_d = pygame.image.load('enemies/kubelwagen_d_right.png')

tower_type1 = pygame.image.load('towers/generic_tower.jpg')

enemy_group = pygame.sprite.Group()
tower_group = pygame.sprite.Group()





class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y, width, height, color, health, image): #TODO: movement speed, type
		super().__init__()		
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.center = [pos_x, pos_y]
		
		
		#self.current_health = 50	# TODO: health system

	def move(self): # basic movement function, TODO: automatise (pathfinding?)
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
           
        # preparation for automatic movement
		#  analyzuj self.levelMap v gameMap
		#  pohybuj se pouze po "0" polích
	#def analyse(self, gameMapPlan)
           
           
           
           
           

		
		#
		
		
		
	def drawEnemy(self, surface): # draw enemy
		pygame.draw.rect(surface, (0, 0, 0), self.rect)

	def update(self):
		self.move()







class Tower(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y, width, height, color): #TODO: cost, type, fire_delay
		super().__init__()
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.center = [pos_x, pos_y]
		self.delay_counter = 0
	
	""" CURRENTLY NOT NEEDED, MIGHT BE NEEDED SOMETIME	
	def drawMemory(self, surface):
		# creates the memory to remember whether a tower can be placed or not
		# 0 = vacant place; 1 = occupied (either by a tower or a cliff)
		self.towerMemory=[]
		self.towerMemory.append([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
		self.towerMemory.append([1,0,1,1,1,0,0,1,1,1,1,1,1,1,1])
		self.towerMemory.append([1,1,1,0,1,1,0,1,1,0,0,0,0,0,1])
		self.towerMemory.append([1,1,0,0,0,1,0,1,1,0,1,1,1,0,1])
		self.towerMemory.append([1,1,1,0,0,1,0,1,1,0,1,0,1,0,1])
		self.towerMemory.append([1,0,0,0,1,1,0,1,0,0,1,0,1,0,1])
		self.towerMemory.append([1,0,1,1,1,0,0,0,0,0,1,0,1,0,1])
		self.towerMemory.append([1,0,1,0,0,0,0,0,0,0,1,0,1,0,1])
		self.towerMemory.append([1,0,1,1,1,1,1,0,0,1,1,0,1,0,1])
		self.towerMemory.append([1,0,0,0,0,0,1,1,1,1,0,0,1,0,1])
		self.towerMemory.append([1,1,0,0,1,0,1,0,1,1,0,0,1,1,1])
		self.towerMemory.append([1,1,1,1,1,1,1,0,0,1,0,0,0,0,1])
		self.towerMemory.append([1,1,1,1,1,0,1,1,1,1,0,0,1,1,1])
		self.towerMemory.append([1,1,1,1,1,0,0,0,0,0,0,1,1,1,1])
		self.towerMemory.append([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
	"""

	def update(self):
		self.fire() #TODO: different settings (closest, strongest)
		
	def fire(self):
		for i in range(50): #TODO: replace 50 with "fire_delay": every x pygame cycles, the tower fires
			self.delay_counter+=1
		self.delay_counter = 0
		


		
		
	


class GameMap():
	def __init__(self):
		self.current_health = 100	# current health
		self.maximum_health = 100	# maximum health
		self.current_money = 100 # money
		self.health_bar_length = 180
		self.health_ratio = self.maximum_health / self.health_bar_length # for optimal health bar appearence
		self.end_hitbox = pygame.Rect(570, 400, 30, 40) # hitbox for obtaining damage
		self.placing_tower = 0
		
		
		# link the following to specific tower type attributes
		self.towerchoice_type1_x = 639 # -1 to compensate for click (click is perceived as directly on edge, wouldnt work without)
		self.towerchoice_type2_x = 719
		self.towerchoice_y = 119
		self.towerchoice_size = 41
		self.tower_price = 1
		self.towercolor = (255, 255, 255)
		
		
	def drawMap(self, surface):  # TODO: structure, multiple levels
		"""draws the map"""
		self.levelMap=[]
		self.levelMap.append([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
		self.levelMap.append([1,4,0,0,0,4,4,1,1,1,1,1,1,1,1])
		self.levelMap.append([2,0,0,4,0,0,4,1,1,4,4,4,4,4,1])
		self.levelMap.append([1,1,4,4,4,0,4,1,1,4,0,0,0,4,1])
		self.levelMap.append([1,1,1,4,4,0,4,1,1,4,0,4,0,4,1])
		self.levelMap.append([1,4,4,4,0,0,4,1,4,4,0,4,0,4,1])
		self.levelMap.append([1,4,0,0,0,4,4,4,4,4,0,4,0,4,1])
		self.levelMap.append([1,4,0,4,4,4,4,4,4,4,0,4,0,4,1])
		self.levelMap.append([1,4,0,0,0,0,0,4,4,0,0,4,0,4,1])
		self.levelMap.append([1,4,4,4,4,4,0,1,1,0,4,4,0,4,1])
		self.levelMap.append([1,1,4,4,1,4,0,4,1,0,4,4,0,0,3])
		self.levelMap.append([1,1,1,1,1,1,0,4,4,0,4,4,4,4,1])
		self.levelMap.append([1,1,1,1,1,4,0,0,0,0,4,4,1,1,1])
		self.levelMap.append([1,1,1,1,1,4,4,4,4,4,4,1,1,1,1])
		self.levelMap.append([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
		
		for x in range(15):
			for y in range(15):
				if (self.levelMap[x][y]==1): # empty tiles
					pygame.draw.rect(surface, (64, 64, 64), (y*40, x*40, 40, 40))
				elif (self.levelMap[x][y]==2): # start
					pygame.draw.rect(surface, (0, 255, 0), (y*40, x*40, 40, 40))
				elif (self.levelMap[x][y]==3): # finish
					pygame.draw.rect(surface, (255, 0, 0), (y*40, x*40, 40, 40))
				elif (self.levelMap[x][y]==4): # tiles for placing towers
					pygame.draw.rect(surface, (139, 105, 20), (y*40, x*40, 40, 40))	
				elif (self.levelMap[x][y]==0): # road
					pygame.draw.rect(surface, (0, 128, 0), (y*40, x*40, 40, 40))
	
	def getDamage(self, amount):
		"""subtracting health"""
		if self.current_health > 0: # protection against HP under 0
			self.current_health -= amount
		if self.current_health <=0:
			self.current_health = 0 # TODO: end of game
	
	def getMoney(self, amount):
		"""adding money"""
		self.current_money += amount
		
	def spendMoney(self, amount):
		"""subtracting money"""		# TODO: protection against going below 0
		if self.current_money > 0: 
			self.current_money -= amount

	# HEALING: to be implemented?
	"""
	def getHealth(self, amount):
		if self.current_health < self.maximum_health:
			self.current_health += amount
		if self.current_health >= self.maximum_health:
			self.current_health = self.maximum_health
	"""

	def moneyIndicator(self):	
		"""shows money available; for money, the player can purchase towers"""
		myfont = pygame.font.SysFont("calibri", 20)
		self.current_money_label = myfont.render(str(self.current_money)+'$', 1, (0, 0, 0)) # TODO: make prettier
		surface.blit(self.current_money_label, (690 , 25))

	def healthBar(self):	
		"""health bar of the 'castle': damaged when an enemy reaches the end of the map"""
		pygame.draw.rect(surface, (255, 0, 0), (610, 50, self.current_health/self.health_ratio, 25))
		pygame.draw.rect(surface, (0, 0, 0), (610, 50, self.health_bar_length, 25), 4)
		myfont = pygame.font.SysFont("calibri", 20)
		self.current_health_label = myfont.render(str(self.current_health)+"/"+str(self.maximum_health), 1, (0, 0, 0))
		surface.blit(self.current_health_label, (670 , 55))

	def towerChoice(self):
		"""the player's ability to choose towers to place; tower goes gray when not affordable"""
		pygame.draw.rect(surface, (255, 0, 255), (self.towerchoice_type1_x, self.towerchoice_y, self.towerchoice_size, self.towerchoice_size))
		pygame.draw.rect(surface, (0, 255, 255), (self.towerchoice_type2_x, self.towerchoice_y, self.towerchoice_size, self.towerchoice_size))

	def enemy_spawn(self): # spawn
		enemy = Enemy(20, 100, 30, 30, (255, 0, 0), 100, enemy_type3)
		enemy_group.add(enemy)

	def checkMouseIntentions(self, mouse_x, mouse_y):
		"""checks, where the click was made - decides on further action"""
		# tower type #1 chosen:
		if mouse_x > (self.towerchoice_type1_x) and mouse_x < (self.towerchoice_type1_x + self.towerchoice_size) and mouse_x > (self.towerchoice_y) and mouse_y < (self.towerchoice_y + self.towerchoice_size):
			self.tower_price = 20 # PLACEHOLDER, change
			if gamemap.current_money - self.tower_price >= 0:
				print("tower 1 chosen")
				self.placing_tower = 1
				self.tower_color = (255, 0, 255) 
			else:
				print("not enough money!")
		# tower type #2 chosen: 			following coordinates (self.towerchoice_type_2_x, etc) to be changed
		elif mouse_x > (self.towerchoice_type2_x) and mouse_x < (self.towerchoice_type2_x + self.towerchoice_size) and mouse_x > (self.towerchoice_y) and mouse_y < (self.towerchoice_y + self.towerchoice_size):
			self.tower_price = 50 # PLACEHOLDER, change
			if gamemap.current_money - self.tower_price >= 0:
				print("tower 2 chosen")
				self.placing_tower = 1
				self.tower_color = (0, 255, 255)
			else:
				print("not enough money!")
		# clicked in playing field
		elif mouse_x < 600 and mouse_y < 600:
			if self.placing_tower == 1:
				 # PLACEHOLDER, change
				tower_width = 30 # CHANGE to image
				tower_height = 30 # CHANGE to image
				gamemap.tower_place(mouse_x + 20, mouse_y + 20, tower_width, tower_height, self.tower_color)
				# + 20: compensation for off-grid
		# clicked on spawn button
		elif mouse_x > 639 and mouse_x < 760 and mouse_y > 519 and mouse_y < 560:
			print("spawn")
			self.enemy_spawn()
	
	
	def spawnButton(self):
		pygame.draw.rect(surface, (0, 255, 0), (639, 519, 121, 41))
	
	def tower_place(self, pos_x, pos_y, width, height, color):
		if self.getGridField(pos_x, pos_y) == True:
			tower = Tower(pos_x, pos_y, width, height, color)
			tower_group.add(tower)
			print("tower placed")
			gamemap.spendMoney(self.tower_price)
			self.placing_tower = 0
		else:
			print("invalid position!")	
		
			#self, pos_x, pos_y, width, height, color


	def enemy_spawn(self): # spawn
		enemy = Enemy(20, 100, 30, 30, (255, 0, 0), 100, enemy_type3)
		enemy_group.add(enemy)
		

	""" BACKUP
	def tower_place(self):
		tower = Tower(420, 400, 30, 30, (255, 0, 255))
		tower_group.add(tower)
		print("tower placed")
		#self, pos_x, pos_y, width, height, colo
	"""


	def update(self):
		self.moneyIndicator()
		self.healthBar()
		self.towerChoice()
		self.spawnButton()
		#self.detectDamage()
		#self.showDeveloperStuff()

	def getGridField(self, mouse_x, mouse_y):
		"""gets clicked field in grid; finds the value in gamemap (numbers = grid coordinates)"""
		self.grid_field_x = math.floor(mouse_x / 40)
		self.grid_field_y = math.floor(mouse_y / 40)
		print(self.grid_field_x)
		print(self.grid_field_y)
		self.grid_value = (self.levelMap[self.grid_field_y][self.grid_field_x])
		if self.grid_value == 4:
			return True
		
		




	def showDeveloperStuff(self):
		pygame.draw.rect(surface, (255, 154, 0), self.end_hitbox) #HITBOX END
	
	
	
	
	
	
	
	
	
	
os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init() #pygame initialisation

surface = pygame.display.set_mode((800, 600)) # screen initialisation, TODO: move to class

pygame.display.set_caption("soon to be TOWER DEFENSE") # window name









#enemy = Enemy(20, 100, 30, 30, (255, 0, 0), 100, enemy_type3)

gamemap = GameMap()

clock = pygame.time.Clock()



running = True  

     
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x_raw, mouse_y_raw = pygame.mouse.get_pos()
			print("raw click x: "+str(mouse_x_raw)) # RAW data: not for grid
			print("raw click y: "+str(mouse_y_raw)) # RAW data: not for grid
			mouse_x = (math.floor(mouse_x_raw / 40) * 40)
			mouse_y = (math.floor(mouse_y_raw / 40) * 40)
			print("grid x: "+str((math.floor(mouse_x_raw / 40))))
			print("grid y: "+str((math.floor(mouse_y_raw / 40))))
			print("grid aligned x: "+str(mouse_x)) # aligned to grid
			print("grid aligned y: "+str(mouse_y)) # aligned to grid
			gamemap.checkMouseIntentions(mouse_x, mouse_y)
			
			
			
			
			
			
		# FOLLOWING IS FOR TESTING PURPOSES ONLY
		if event.type == pygame.KEYDOWN:	# TODO: link with enemy crossing the line
			if event.key == pygame.K_d:
				gamemap.getDamage(20)
		if event.type == pygame.KEYDOWN:	# TODO: link with wave spawn/kill/whatever
			if event.key == pygame.K_g:
				gamemap.getMoney(20)
		if event.type == pygame.KEYDOWN:	# TODO: link with tower build
			if event.key == pygame.K_h:
				gamemap.spendMoney(20)

				

# enemy = Enemy(...)
# group.add(enemy)


#NEBO add do konstruktoru 

	surface.fill((255, 255, 255))
	
	gamemap.drawMap(surface)
	gamemap.update()
	
	enemy_group.draw(surface)
	enemy_group.update() # group.update? 
	
	tower_group.draw(surface)
	tower_group.update() # group.update? 
	
	
	pygame.display.update()

	clock.tick(100)





pygame.quit()



