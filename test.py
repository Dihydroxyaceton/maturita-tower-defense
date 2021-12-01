import pygame
import os
import numpy


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



class Tower(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y, width, height, color): #TODO: cost, type, fire_delay
		super().__init__()
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.center = [pos_x, pos_y]
		self.delay_counter = 0
		
	def drawMemory(self, surface):
		"""creates the memory to remember whether a tower can be placed or not"""
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

	def update(self):
		self.fire() #TODO: different settings (closest, strongest)
		
	def fire(self):
		for i in range(50): #TODO: replace 50 with "fire_delay": every x pygame cycles, the tower fires
			self.delay_counter+=1
		self.delay_counter = 0
		
	def spawn(self):	# TODO: make it work idk
		tower_group = pygame.sprite.Group()
		#tower_group.add(tower)
		
		#tower = Tower(420, 400, 20, 20, (255, 0, 255))
		
		
	


class GameMap():
	def __init__(self):
		self.current_health = 100	# current health
		self.maximum_health = 100	# maximum health
		self.current_money = 0 # money
		self.health_bar_length = 180
		self.health_ratio = self.maximum_health / self.health_bar_length # for optimal health bar appearence
		self.end_hitbox = pygame.Rect(570, 400, 30, 40) # hitbox for obtaining damage
		
		
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


	def update(self):
		self.moneyIndicator()
		self.healthBar()
		#self.detectDamage()
		#self.showDeveloperStuff()

	def enemy_spawn(self): # spawn
		enemy = Enemy(20, 100, 30, 30, (255, 0, 0), 100, enemy_type3)
		enemy_group.add(enemy)




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

	#tower_group.draw(surface)
	#tower.update() # group.update? 
	
	
	pygame.display.update()

	clock.tick(100)





pygame.quit()
