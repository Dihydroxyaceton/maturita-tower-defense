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
    
  turret
    attributes: type, cadency, cost, name, location
    methodes: firing
  
  bullet
    attributes: type, damage, location
    methodes: dealing damage
"""

class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y, width, height, color, health): #TODO: movement speed, type
		super().__init__()
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
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
           
		
	def drawEnemy(self, surface): # draw enemy
		pygame.draw.rect(surface, (0, 0, 0), self.rect)

	def update(self):
		self.move()


class Turret(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y, width, height, color): #TODO: cost, type, fire_delay
		super().__init__()
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.center = [pos_x, pos_y]
		self.delay_counter = 0

		"""
	def update(self):
		self.fire() #TODO: different settings (closest, strongest)
		
	def fire(self):
		for i in range(50): #TODO: replace 50 with "fire_delay": every x pygame cycles, the turret fires
			self.delay_counter+=1
		self.delay_counter = 0
		

class Bullet(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y, width, height, color): #TODO: damage, type
		super().__init__()
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.center = [pos_x, pos_y]

	def update(self):
		#detecting collision with a bullet
		if enemy.rect.colliderect(self.rect):
			enemy.kill() # TODO: damage, not kill
		self.pew()
	
	def pew(self): #TODO: rename
		for i in range(50): #TODO: replace 50 with "fire_delay": every x pygame cycles, the turret fires
			self.delay_counter+=1
		self.delay_counter = 0

		for i in range(50): #TODO: replace "20" with bullet_life = how long the bullet will fly before despawning
			self.rect.move_ip(1, 0)
		#self.kill()

		"""


class GameMap():
	def __init__(self):
		self.current_health = 100	# current health
		self.maximum_health = 100	# maximum health
		self.health_bar_length = 180
		self.health_ratio = self.maximum_health / self.health_bar_length # for optimal health bar appearence
		self.end_hitbox = pygame.Rect(570, 400, 30, 40) # hitbox for obtaining damage
		
		
	def drawMap(self, surface):  # TODO: structure, array, multiple levels
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
				elif (self.levelMap[x][y]==4): # tiles for placing turrets
					pygame.draw.rect(surface, (128, 128, 128), (y*40, x*40, 40, 40))	
				elif (self.levelMap[x][y]==0): # road
					pygame.draw.rect(surface, (234, 234, 160), (y*40, x*40, 40, 40))
			
			
	def detectDamage(self):		# TODO: add "amount" (damage system - different enemy types)
		"""detecting enemy reaching the end of the map"""
		if enemy.rect.colliderect(self.end_hitbox):
			enemy.kill()
			self.getDamage(1)	# TODO: OPTIMISE
			
	
	def getDamage(self, amount):
		"""subtracting health"""
		if self.current_health > 0: # protection against HP under 0
			self.current_health -= amount
		if self.current_health <=0:
			self.current_health = 0 # TODO: end of game
	
	# HEALING: to be implemented?
	"""
	def getHealth(self, amount):
		if self.current_health < self.maximum_health:
			self.current_health += amount
		if self.current_health >= self.maximum_health:
			self.current_health = self.maximum_health
	"""


	def healthBar(self):	
		"""health bar of the 'castle': damaged when an enemy reaches the end of the map"""
		pygame.draw.rect(surface, (255, 0, 0), (610, 50, self.current_health/self.health_ratio, 25))
		pygame.draw.rect(surface, (0, 0, 0), (610, 50, self.health_bar_length, 25), 4)
		myfont = pygame.font.SysFont("calibri", 20)
		self.current_health_label = myfont.render(str(self.current_health)+"/"+str(self.maximum_health), 1, (0, 0, 0))
		surface.blit(self.current_health_label, (670 , 55))

	def update(self):
		self.healthBar()
		self.detectDamage()
		#self.showDeveloperStuff()

	def showDeveloperStuff(self):
		pygame.draw.rect(surface, (255, 154, 0), self.end_hitbox) #HITBOX END
	
	
	
os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init() #pygame initialisation

surface = pygame.display.set_mode((800, 600)) # screen initialisation, TODO: move to class

pygame.display.set_caption("soon to be TOWER DEFENSE") # window name



enemy = Enemy(20, 100, 20, 20, (0, 0, 0), 100)

enemy_group = pygame.sprite.Group()
enemy_group.add(enemy)


turret = Turret(420, 400, 20, 20, (255, 0, 255))

turret_group = pygame.sprite.Group()
turret_group.add(turret)


#bullet = Bullet(420, 400, 5, 5, (255, 0, 0))

#bullet_group = pygame.sprite.Group()
#bullet_group.add(bullet)


gamemap = GameMap()

clock = pygame.time.Clock()



running = True  

     
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:	# TODO: link with enemy crossing the line
			if event.key == pygame.K_d:
				gamemap.getDamage(20)


	surface.fill((255, 255, 255))
	
	gamemap.drawMap(surface)
	gamemap.update()
	
	enemy_group.draw(surface)
	enemy.update()
	
	turret_group.draw(surface)
	turret.update()
	
	
	pygame.display.update()

	clock.tick(100)





pygame.quit()
