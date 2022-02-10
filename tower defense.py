import pygame
import os
import numpy
import math
import time
import gamemap2 as level_file
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

enemy_type2 = pygame.image.load('enemies/bf_right.png')
enemy_type2_d = pygame.image.load('enemies/bf_d_right.png')

tower_type1 = pygame.image.load('towers/tower_1.png')
tower_type2 = pygame.image.load('towers/tower_2.png')

bullet_type1 = pygame.image.load('bullets/bullet_1.png')
bullet_type2 = pygame.image.load('bullets/bullet_2.png')


enemy_group = pygame.sprite.Group()
tower_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

print("WELCOME TO TOWER DEFENSE, WAVE 1 IN 5 SECONDS")

tick_time = 180

wave_list = [(0,0,0), (2,2,0), (2,4,1), (1,5,3), (0.5,7,7)]
# tuple structure: (delay between enemies, ground enemies, air enemies)

class GameMap():
	def __init__(self):
		self.current_health = 100	# current health
		self.maximum_health = 100	# maximum health
		self.current_money = 40 # money
		self.health_bar_length = 180
		self.health_ratio = self.maximum_health / self.health_bar_length # for optimal health bar appearence
		self.end_hitbox = pygame.Rect(570, 400, 30, 40) # hitbox for obtaining damage
		self.placing_tower = 0
		self.passed_ticks = 0
		self.wave_pause = 0
		self.spawned_enemies = 0
		self.do_spawn = False
		self.current_wave = 0
		self.spawned_ground_enemies = 0
		self.spawned_air_enemies = 0
		
		# link the following to specific tower type attributes
		self.towerchoice_type1_x = 639 # -1 to compensate for click (click is perceived as directly on edge, wouldnt work without)
		self.towerchoice_type2_x = 719
		self.towerchoice_y = 119
		self.towerchoice_size = 41
		self.tower_price = 1
		self.towercolor = (255, 255, 255)

		
	def drawMap(self, surface):  # TODO: structure, multiple levels
		"""draws the map"""
		self.levelMap=level_file.levelMap
		
		self.start_point_x = 20 # TODO: not absolute number
		self.start_point_y = 100
		
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
					
	def detectDamage(self):		# TODO: add "amount" (damage system - different enemy types)
		"""detecting enemy reaching the end of the map"""
		for enemy in enemy_group:
			reachesEnd = enemy.colliderect(self.end_hitbox)
			if reachesEnd == True:
				self.getDamage(1)
	
	
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

	def checkMouseIntentions(self, mouse_x, mouse_y):
		"""checks, where the click was made - decides on further action"""
		# tower type #1 chosen:
		if mouse_x > (self.towerchoice_type1_x) and mouse_x < (self.towerchoice_type1_x + self.towerchoice_size) and mouse_x > (self.towerchoice_y) and mouse_y < (self.towerchoice_y + self.towerchoice_size):
			self.tower_price = 20 # PLACEHOLDER, change
			if gamemap.current_money - self.tower_price >= 0:
				print("tower 1 chosen")
				self.placing_tower = 1
				self.tower_reach = 80
				self.tower_image = tower_type1
				self.tower_cooldown = 10
				self.bullet_type = 1
				self.damage = 10
			else:
				print("not enough money!")
		# tower type #2 chosen: 			following coordinates (self.towerchoice_type_2_x, etc) to be changed
		elif mouse_x > (self.towerchoice_type2_x) and mouse_x < (self.towerchoice_type2_x + self.towerchoice_size) and mouse_x > (self.towerchoice_y) and mouse_y < (self.towerchoice_y + self.towerchoice_size):
			self.tower_price = 50 # PLACEHOLDER, change
			if gamemap.current_money - self.tower_price >= 0:
				print("tower 2 chosen")
				self.placing_tower = 1
				self.tower_reach = 160
				self.tower_image = tower_type2
				self.tower_cooldown = 3
				self.bullet_type = 2
				self.damage = 20
			else:
				print("not enough money!")
		# clicked in playing field
		elif mouse_x < 600 and mouse_y < 600:
			if self.placing_tower == 1:
				gamemap.tower_place(mouse_x + 20, mouse_y + 20, self.tower_reach, self.tower_image, self.tower_cooldown, self.bullet_type, self.damage)
				# + 20: compensation for off-grid
			
	
	
	def tower_place(self, pos_x, pos_y, reach, image, cooldown, bullet_type, damage):
		if self.checkGridField(pos_x, pos_y) == 4:
			#(self, pos_x, pos_y, width, height, reach, image, cooldown):
			tower = Tower(pos_x, pos_y, reach, image, cooldown, bullet_type, damage)
			
			tower_group.add(tower)
			
			
			# TODO: add protection against placing atop of another tower
			print("tower placed")
			gamemap.spendMoney(self.tower_price)
			self.placing_tower = 0
		else:
			print("invalid position!")	
		
			#self, pos_x, pos_y, width, height, color


	def enemySpawn(self): # spawn
		
			#print(str(self.wave_pause) + str(self.spawned_in_wave))
			if self.current_wave < len(wave_list):
				self.spawn_delay = (wave_list[self.current_wave][0]) * tick_time
				self.ground_enemies_count = wave_list[self.current_wave][1]
				self.air_enemies_count = wave_list[self.current_wave][2]
			else:
				print("GAME OVER")
				self.do_spawn = False
				self.passed_ticks = 0
				running = False
			if self.passed_ticks >= self.spawn_delay:
				if self.do_spawn == True:
					self.passed_ticks = 0
					if self.spawned_ground_enemies < self.ground_enemies_count:		
						enemy = Enemy(20, 100, 30, 30, (255, 0, 0), 100, enemy_type3)
						enemy_group.add(enemy)
						self.spawned_ground_enemies += 1
					else:	# hierarchy states order of spawning (in our case ground first, air thereafter)
						if self.spawned_air_enemies < self.air_enemies_count:
							enemy = Enemy(20, 100, 30, 30, (255, 0, 0), 200, enemy_type2)
							enemy_group.add(enemy)
							self.spawned_air_enemies += 1
						else:
							self.do_spawn = False
							self.spawned_ground_enemies = 0
							self.spawned_air_enemies = 0
							print("END WAVE "+str(self.current_wave)+", NEXT WAVE IN 5 SECONDS")
				else:
					if self.wave_pause >= 900:
						self.wave_pause = 0
						self.do_spawn = True
						self.current_wave += 1
						print("STARTING WAVE "+str(self.current_wave))
					else:
						self.wave_pause += 1
			else:
				self.passed_ticks += 1
		
		
	
	def update(self):
		self.moneyIndicator()
		self.healthBar()
		self.towerChoice()
		self.enemySpawn()
		#self.checkTowerRange(Enemy, Tower)
		#self.detectDamage()
		#self.showDeveloperStuff()






	def checkGridField(self, mouse_x, mouse_y):
		"""checks clicked field in grid; finds the value in gamemap (numbers = grid coordinates)"""
		self.grid_field_x = math.floor(mouse_x / 40)
		self.grid_field_y = math.floor(mouse_y / 40)
		self.grid_value = (self.levelMap[self.grid_field_y][self.grid_field_x])
		return self.grid_value
		
	def showDeveloperStuff(self):
		pygame.draw.rect(surface, (255, 154, 0), self.end_hitbox) #HITBOX END



class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y, width, height, color, health, image): #TODO: movement speed, type
		super().__init__()		
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.center = [pos_x, pos_y]
		self.pos_x = gamemap.start_point_x
		self.pos_y = gamemap.start_point_y
		self.clock = 0
		self.movement_var = 0 # 0 = look for path; 1 = up, 2 = right, 3 = down, 4 = left
		self.moved_pixels = 0
		self.goRightOk = True
		self.goLeftOk = True
		self.goUpOk = True
		self.goDownOk = True
		self.current_health = 50	# TODO: health system
	


	def findPath(self):
		if self.goRightOk == True:
			if gamemap.checkGridField(self.pos_x + 21, self.pos_y) == 0:
				self.movement_var = 2
				self.goLeftOk = False 	# protection against turning 180° and returning via same path; will be unlocked again by finishing movement to a non-opposite direction
				self.goRightOk = True
				self.goUpOk = True
				self.goDownOk = True
				return
		if self.goLeftOk == True:
			if gamemap.checkGridField(self.pos_x - 21, self.pos_y) == 0:
				self.movement_var = 4
				self.goRightOk = False
				self.goLeftOk = True
				self.goUpOk = True
				self.goDownOk = True
				return
		if self.goUpOk == True:
			if gamemap.checkGridField(self.pos_x, self.pos_y - 21) == 0:
				self.movement_var = 1
				self.goDownOk = False
				self.goRightOk = True
				self.goLeftOk = True
				self.goUpOk = True
				return
		if self.goDownOk == True:
			if gamemap.checkGridField(self.pos_x, self.pos_y + 21) == 0:
				self.movement_var = 3
				self.goUpOk = False				
				self.goRightOk = True
				self.goLeftOk = True
				self.goDownOk = True
				return
		
		
	def moveRight(self):
		if self.moved_pixels <= 39:
			self.moved_pixels += 1
			self.rect.move_ip(1, 0)
			self.pos_x += 1	
		else:
			self.movement_var = 0
			self.moved_pixels = 0
	
	def moveLeft(self):
		if self.moved_pixels <= 39:
			self.moved_pixels += 1
			self.rect.move_ip(-1, 0)
			self.pos_x -= 1
		else:
			self.movement_var = 0
			self.moved_pixels = 0
			
	def moveUp(self):
		if self.moved_pixels <= 39:
			self.moved_pixels += 1
			self.rect.move_ip(0, -1)
			self.pos_y -= 1	
		else:
			self.movement_var = 0
			self.moved_pixels = 0	

	def moveDown(self):			
		if self.moved_pixels <= 39:
			self.moved_pixels += 1
			self.rect.move_ip(0, 1)
			self.pos_y += 1
		else:
			self.movement_var = 0
			self.moved_pixels = 0
	
	def getHit(self, amount):
		self.current_health -= amount
		if self.current_health <= 0:
			pygame.sprite.Sprite.kill(self)
			gamemap.getMoney(20)		
	

	def update(self):
		if self.movement_var == 0:
			self.findPath()
		if self.movement_var == 1:
			self.moveUp()
		if self.movement_var == 2:
			self.moveRight()
		if self.movement_var == 3:
			self.moveDown()
		if self.movement_var == 4:
			self.moveLeft()
		if self.pos_x >= 570:
			pygame.sprite.Sprite.kill(self)
			gamemap.getDamage(1)
		
		

class Tower(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y, reach, image, cooldown, bullet_type, damage):
		super().__init__()
		self.cooldown = cooldown
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.center = [pos_x, pos_y]
		self.know_target = False
		self.shot_elapsed_time = cooldown
		self.bullet_type = bullet_type
		self.reach = reach
		self.damage = damage
			
			
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

	def findTarget(self, target_x, target_y):
		self.target_x = target_x
		self.target_y = target_y
		if tower.know_target == False:
			#print("ENEMY IN RANGE!")
			#print(str(target_x), str(target_y))
			self.know_target = True


	def shoot(self, target_x, target_y):
		if self.shot_elapsed_time > self.cooldown:		
			#print("pew pew, target is X"+str(target_x)+" Y"+str(target_y))
			if self.bullet_type == 1:
				bullet = Bullet(self.pos_x, self.pos_y, target_x, target_y, bullet_type1, self.reach, self.damage)
			if self.bullet_type == 2:
				bullet = Bullet(self.pos_x, self.pos_y, target_x, target_y, bullet_type2, self.reach, self.damage)
			bullet_group.add(bullet)
			self.shot_elapsed_time = 0
			self.know_target = False
		else:
			self.shot_elapsed_time += 1
		

	def update(self):
		if self.know_target == True:
			self.shoot(self.target_x, self.target_y)
			
			
			
class Bullet (pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y, target_x, target_y, image, reach, damage):
		super().__init__()
		self.start_x = pos_x
		self.start_y = pos_y
		self.target_x = target_x
		self.target_y = target_y
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.center = [pos_x, pos_y]
		self.reach = reach
		self.damage = damage
		
		# calculating movement vectors
		self.vector_x = (self.target_x - self.pos_x) * 0.05
		self.vector_y = (self.target_y - self.pos_y) * 0.05
			
	def update(self):
		self.move()
		if self.pos_x < (self.start_x - self.reach) or self.pos_x > (self.start_x + self.reach) or self.pos_y < (self.start_y - self.reach) or self.pos_y > (self.start_y + self.reach):
			# max flying range of bullet
			pygame.sprite.Sprite.kill(self)
	
	def move(self):
		# movement along X axis:
		self.rect.move_ip(self.vector_x, 0)
		self.pos_x += self.vector_x	
		# movement along Y axis:
		self.rect.move_ip(0, self.vector_y)
		self.pos_y += self.vector_y
	
	
	
	
os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init() #pygame initialisation

surface = pygame.display.set_mode((800, 600)) # screen initialisation, TODO: move to class

pygame.display.set_caption("soon to be TOWER DEFENSE") # window name



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
			
	"""
	for enemy in enemy_group:	
		for tower in tower_group:
			if tower.know_target == False:
				if pygame.sprite.spritecollide(tower, enemy_group, False):
					tower.findTarget(enemy.pos_x, enemy.pos_y)
				else:
					tower.know_target = False
	"""				
	
	for tower in tower_group:
		enemy_colliding = pygame.sprite.spritecollide(tower, enemy_group, False)
		for enemy in enemy_colliding:
			tower.findTarget(enemy.pos_x, enemy.pos_y)
			break

	
	for bullet in bullet_group:
		for enemy in enemy_group:
			if pygame.sprite.spritecollide(enemy, bullet_group, True):
				print("ENEMY HIT!")
				enemy.getHit(bullet.damage)
					
				
	
	surface.fill((255, 255, 255))
	
	gamemap.drawMap(surface)
	gamemap.update()
	
	enemy_group.draw(surface)
	enemy_group.update()
	
	tower_group.draw(surface)
	tower_group.update()
	
	bullet_group.draw(surface)
	bullet_group.update()
	
	
	pygame.display.update()

	clock.tick(tick_time)





pygame.quit()



