import pygame
import os
import math
import gamemap2 as level_file

""" 

https://www.youtube.com/watch?v=TqbtxBntuF0&t=105s    
    
"""



# defining textures and stats:

grass_texture = pygame.image.load('ground_textures/grass.png')
road_texture = pygame.image.load('ground_textures/road.png')
stone_texture = pygame.image.load('ground_textures/stone.png')

enemy_type1_image = pygame.image.load('enemies/kubelwagen_right.png')
enemy_type2_image = pygame.image.load('enemies/bf_right.png')

tower_type1_image = pygame.image.load('towers/tower_1.png')
tower_type1_image_menu = pygame.image.load('towers/tower_1_menu.png')
tower_type2_image = pygame.image.load('towers/tower_2.png')
tower_type2_image_menu = pygame.image.load('towers/tower_2_menu.png')

bullet_type1_image = pygame.image.load('bullets/bullet_1.png')
bullet_type2_image = pygame.image.load('bullets/bullet_2.png')


enemy_type1 = [enemy_type1_image, 100]
enemy_type2 = [enemy_type2_image, 400]
# structure: image, health

tower_type1 = [tower_type1_image, 100, 1, 20]
tower_type2 = [tower_type2_image, 80, 2, 100, 90]
# structure: image, cooldown, bullet type, cost, (upgrade price)]

bullet_type1 = [bullet_type1_image, 80, 20]
bullet_type2 = [bullet_type2_image, 160, 25]
# structure: image, range, damage



# defining entity groups
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

		
	def drawMap(self, surface):  # TODO: structure
		"""draws the map"""
		self.levelMap=level_file.levelMap
		
		self.start_point_x = 20
		self.start_point_y = 100
		
		for x in range(15):
			for y in range(15):
				if (self.levelMap[x][y]==1): # empty tiles
					surface.blit(grass_texture, (y*40, x*40))
				elif (self.levelMap[x][y]==4): # tiles for placing towers
					surface.blit(stone_texture, (y*40, x*40))
				elif (self.levelMap[x][y]==0): # road
					surface.blit(road_texture, (y*40, x*40))
					
	def detectDamage(self):		# TODO: add "amount" (damage system - different enemy types)
		"""detecting enemy reaching the end of the map, subtracting money thereafter"""
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
		"""subtracting money"""
		if self.current_money > 0: # protection against money under 0
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
		#pygame.draw.rect(surface, (255, 0, 255), (self.towerchoice_type1_x, self.towerchoice_y, self.towerchoice_size, self.towerchoice_size))
		surface.blit(tower_type1_image_menu, (self.towerchoice_type1_x, self.towerchoice_y))
		#pygame.draw.rect(surface, (0, 255, 255), (self.towerchoice_type2_x, self.towerchoice_y, self.towerchoice_size, self.towerchoice_size))
		surface.blit(tower_type2_image_menu, (self.towerchoice_type2_x, self.towerchoice_y))

	def checkMouseIntentions(self, mouse_x, mouse_y):
		"""checks, where the click was made - decides on further action"""
		# tower type #1 chosen:
		if mouse_x > (self.towerchoice_type1_x) and mouse_x < (self.towerchoice_type1_x + self.towerchoice_size) and mouse_x > (self.towerchoice_y) and mouse_y < (self.towerchoice_y + self.towerchoice_size):
			self.tower_price = tower_type1[3]
			if gamemap.current_money - self.tower_price >= 0: # checking if enough money
				print("tower 1 chosen")
				self.placing_tower = 1
			else:
				print("not enough money!")
		# tower type #2 chosen:
		elif mouse_x > (self.towerchoice_type2_x) and mouse_x < (self.towerchoice_type2_x + self.towerchoice_size) and mouse_x > (self.towerchoice_y) and mouse_y < (self.towerchoice_y + self.towerchoice_size):
			self.tower_price = tower_type2[3]
			if gamemap.current_money - self.tower_price >= 0: # checking if enough money
				print("tower 2 chosen")
				self.placing_tower = 2
			else:
				print("not enough money!")
		# clicked in playing field
		elif mouse_x < 600 and mouse_y < 600:
			if self.placing_tower == 1 or self.placing_tower == 2:
				self.tower_place(mouse_x + 20, mouse_y + 20)
				# + 20: compensation for off-grid
			elif self.checkGridField(mouse_x, mouse_y) == 91:
				if gamemap.current_money - tower_type2[4] >= 0: # checking if enough money
					self.tower_upgrade(mouse_x, mouse_y)
				else:
					print("NOT ENOUGH MONEY FOR UPGRADE, "+str(tower_type2[4])+" NEEDED")

	def tower_place(self, pos_x, pos_y):
		"""xx"""
		if self.checkGridField(pos_x, pos_y) == 4:
			if self.placing_tower == 1:
				tower = Tower(pos_x, pos_y, tower_type1[0], tower_type1[1], tower_type1[2])
				tower_group.add(tower)
				self.levelMap[math.floor(mouse_y / 40)][math.floor(mouse_x / 40)] = 91 # marks the grid field as occupied by tower type 1
			if self.placing_tower == 2:
				tower = Tower(pos_x, pos_y, tower_type2[0], tower_type2[1], tower_type2[2])
				tower_group.add(tower)
				self.levelMap[math.floor(mouse_y / 40)][math.floor(mouse_x / 40)] = 92 # marks the grid field as occupied by tower type 2
			print("tower placed")
			self.spendMoney(self.tower_price)
			self.placing_tower = 0
		else:
			print("invalid position!")	

	def tower_upgrade(self, pos_x, pos_y):
		for tower in tower_group:
			if (math.floor(mouse_x / 40)) == (math.floor(tower.pos_x / 40)) and (math.floor(mouse_y / 40)) == (math.floor(tower.pos_y / 40)): # checks for the particular tower to upgrade
				pygame.sprite.Sprite.kill(tower)
				print("tower upgraded")
				self.spendMoney(tower_type2[4])
				tower = Tower(pos_x + 20, pos_y + 20, tower_type2[0], tower_type2[1], tower_type2[2])
				tower_group.add(tower)

	def enemySpawn(self): # spawn
			if self.current_wave < len(wave_list):
				self.spawn_delay = (wave_list[self.current_wave][0]) * tick_time
				self.ground_enemies_count = wave_list[self.current_wave][1]
				self.air_enemies_count = wave_list[self.current_wave][2]
			else:
				if len(enemy_group) == 0:	# checks for emptied list of enemies after last wave
					print("GAME OVER")
					self.do_spawn = False
					self.passed_ticks = 0
					running = False
			if self.passed_ticks >= self.spawn_delay:
				if self.do_spawn == True:
					self.passed_ticks = 0
					if self.spawned_ground_enemies < self.ground_enemies_count:		
						enemy = Enemy(20, 100, enemy_type1[0], enemy_type1[1])
						enemy_group.add(enemy)
						self.spawned_ground_enemies += 1
					else:
						if self.spawned_air_enemies < self.air_enemies_count:
							enemy = Enemy(20, 100, enemy_type2[0], enemy_type2[1])
							enemy_group.add(enemy)
							self.spawned_fair_enemies += 1
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
		#self.showDeveloperStuff()






	def checkGridField(self, mouse_x, mouse_y):
		"""checks clicked field in grid; finds the value in gamemap (numbers = grid coordinates)"""
		self.grid_field_x = math.floor(mouse_x / 40)
		self.grid_field_y = math.floor(mouse_y / 40)
		self.grid_value = (self.levelMap[self.grid_field_y][self.grid_field_x])
		return self.grid_value
	
	def editGridField(self, x, y, amount):
		print(self.levelMap)
	
	def showDeveloperStuff(self):
		pygame.draw.rect(surface, (255, 154, 0), self.end_hitbox) #HITBOX END



class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y, image, health):
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
		self.current_health = health
	


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
	def __init__(self, pos_x, pos_y, image, cooldown, bullet_type):
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
			
	def findTarget(self, target_x, target_y):
		self.target_x = target_x
		self.target_y = target_y
		if tower.know_target == False:
			self.know_target = True


	def shoot(self, target_x, target_y):
		self.know_target = False
		if self.shot_elapsed_time >= self.cooldown:	
			if self.bullet_type == 1:
				bullet = Bullet(self.pos_x, self.pos_y, target_x, target_y, bullet_type1[0], bullet_type1[1], bullet_type1[2])
			if self.bullet_type == 2:
				bullet = Bullet(self.pos_x, self.pos_y, target_x, target_y, bullet_type2[0], bullet_type2[1], bullet_type2[2])
			bullet_group.add(bullet)
			self.shot_elapsed_time = 0
		

	def update(self):
		if self.know_target == True:
			self.shoot(self.target_x, self.target_y)
		if self.shot_elapsed_time < self.cooldown:
			self.shot_elapsed_time += 1
			
			
			
			
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

surface = pygame.display.set_mode((800, 600)) # screen initialisation

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
			mouse_x = (math.floor(mouse_x_raw / 40) * 40)
			mouse_y = (math.floor(mouse_y_raw / 40) * 40)
			gamemap.checkMouseIntentions(mouse_x, mouse_y)
				
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
