import pygame
import os
import math


if chosen_map == 1:
	import maps.gamemap1 as level_file
if chosen_map == 2:
	import maps.gamemap2 as level_file
if chosen_map == 3:
	import maps.gamemap3 as level_file

""" 

https://www.youtube.com/watch?v=TqbtxBntuF0&t=105s    
    
"""

# defining textures and stats:

grass_texture = pygame.image.load("ground_textures/grass.png")
road_texture = pygame.image.load("ground_textures/road.png")
stone_texture = pygame.image.load("ground_textures/stone.png")

enemy_type1_image = pygame.image.load("enemies/car_right.png")
enemy_type2_image = pygame.image.load("enemies/plane_right.png")

tower_type1_image = pygame.image.load("towers/tower_1.png")
tower_type1_image_menu = pygame.image.load("towers/tower_1_menu.png")
tower_type2_image = pygame.image.load("towers/tower_2.png")
tower_type2_image_menu = pygame.image.load("towers/tower_2_menu.png")

bullet_type1_image = pygame.image.load("bullets/bullet_1.png")
bullet_type2_image = pygame.image.load("bullets/bullet_2.png")


enemy_type1 = [enemy_type1_image, 100]
enemy_type2 = [enemy_type2_image, 220]
# structure: image, health

tower_type1 = [tower_type1_image, 100, 1, 20]
tower_type2 = [tower_type2_image, 80, 2, 100, 90]
# structure: image, cooldown, bullet type, cost, (upgrade price)]

bullet_type1 = [bullet_type1_image, 80, 20]
bullet_type2 = [bullet_type2_image, 160, 50]
# structure: image, range, damage



# defining entity groups
enemy_group = pygame.sprite.Group()
tower_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

wave_list = [(0,0,0), (2,2,0), (2,4,0), (1.5,5,1), (1,5,3), (0.5,7,7), (0.4,10,10), (0.1,15,12)]
# index 0 in wave list always needs to stay (0,0,0)
# tuple structure: delay between enemies; enemies type 1; enemies type 2

tick_time = 180


class GameMap():
	def __init__(self):	
		self.current_health = 100
		self.maximum_health = 100
		self.current_money = 60
		self.health_bar_length = 180
		self.health_bar_ratio = self.maximum_health / self.health_bar_length # for optimal health bar appearence
		self.placing_tower = 0 # 0 for no tower placement; 1 for tower type 1; 2 for tower type 2
		self.passed_ticks = 0 # counter (time measurement variable)
		self.wave_pause = 0 # counter (time measurement variable for pause between waves)
		self.spawned_enemies = 0
		self.wave_underway = False
		self.game_end = 0 # game status: 0 for game underway; 1 for game won; 2 for game lost
		self.current_wave = 0
		self.spawned_enemies_type1 = 0
		self.spawned_enemies_type2 = 0
		self.status_text = "Welcome to Tower defense. Place towers to eliminate enemies. Waves starting automatically."
		
		self.towerchoice_type1_x = 639
		self.towerchoice_type2_x = 719
		self.towerchoice_y = 119
		self.towerchoice_size = 41
		# in gamemap.checkMouseIntentions, click is divided by 40 and rounded down to match the field's grid index
		# the value is then multiplied by 40 again to get the coordinates - in this case to 640/720
		# the click wouldnt be received if directly on edge of the tower choice rectangle
		# therefore, 1 is subtracted so that the click coordinate is located inside the rectange

		
	def drawMap(self, surface):
		"""draws the map"""
		self.levelMap=level_file.levelMap
		
		# enemy spawning point coordinates
		self.start_point_x = 20
		self.start_point_y = 100
		
		# creating 15x15 map grid
		for x in range(15):
			for y in range(15):
				if (self.levelMap[x][y]==0): # 0 = road, path for enemies
					surface.blit(road_texture, (y*40, x*40))
				elif (self.levelMap[x][y]==1): # 1 = empty tiles
					surface.blit(grass_texture, (y*40, x*40))
				elif (self.levelMap[x][y]==4): # 4 = tiles for placing towers
					surface.blit(stone_texture, (y*40, x*40))
	
	def getDamage(self, amount):
		"""subtracting health"""
		if self.current_health > 0:
			self.current_health -= amount
		if self.current_health <=0: # detecting loss of all health
			self.current_health = 0
			self.status_text = "GAME OVER. To exit, close the window."
			self.game_end = 2 # setting the current game status to "lost"

	def getMoney(self, amount):
		"""adding money"""
		self.current_money += amount
		
	def spendMoney(self, amount):
		"""subtracting money"""
		if self.current_money > 0: # protection against money under 0
			self.current_money -= amount

	def moneyIndicator(self):	
		"""shows money available"""
		font = pygame.font.SysFont("calibri", 20)
		self.current_money_label = font.render(str(self.current_money)+'$', 1, (0, 0, 0))
		surface.blit(self.current_money_label, (690, 25))
		
	def statusBar(self):
		"""simple text messages to communicate with the player"""
		font = pygame.font.SysFont("calibri", 20)
		self.status_label = font.render(str(self.status_text), 1, (0, 0, 0))
		surface.blit(self.status_label, (20, 608))

	def healthBar(self):	
		"""displaying player's health bar (damaged when an enemy reaches the end of the map)
		inspired by: https://www.youtube.com/watch?v=pUEZbUAMZYA"""
		pygame.draw.rect(surface, (255, 0, 0), (610, 50, self.current_health/self.health_bar_ratio, 25))
		pygame.draw.rect(surface, (0, 0, 0), (610, 50, self.health_bar_length, 25), 4)
		font = pygame.font.SysFont("calibri", 20)
		self.current_health_label = font.render(str(self.current_health)+"/"+str(self.maximum_health), 1, (0, 0, 0))
		surface.blit(self.current_health_label, (670 , 55))

	def towerChoice(self):
		"""displaying tower menu"""
		font = pygame.font.SysFont("calibri", 20)
		surface.blit(font.render("| $ |", 1, (0,0,0)), (678, 165))
		# tower type 1:
		surface.blit(tower_type1_image_menu, (self.towerchoice_type1_x, self.towerchoice_y))
		surface.blit(font.render(str(tower_type1[3]), 1, (0, 0, 0)), (649, 165))
		# tower type 2:
		surface.blit(tower_type2_image_menu, (self.towerchoice_type2_x, self.towerchoice_y))
		surface.blit(font.render(str(tower_type2[3]), 1, (0, 0, 0)), (724, 165))

	def checkMouseIntentions(self, mouse_x, mouse_y):
		"""checks where the click was made - decides on further action"""
		if mouse_x > (self.towerchoice_type1_x) and mouse_x < (self.towerchoice_type1_x + self.towerchoice_size) and mouse_x > (self.towerchoice_y) and mouse_y < (self.towerchoice_y + self.towerchoice_size):
			# clicked on tower type 1 option
			self.tower_price = tower_type1[3]
			if gamemap.current_money - self.tower_price >= 0: 
				# enough money
				self.status_text = "Tower type 1 chosen. Click to place."
				self.placing_tower = 1
			else:
				"Not enough money! "+str(tower_type1[3])+" required for tower type 1."

		elif mouse_x > (self.towerchoice_type2_x) and mouse_x < (self.towerchoice_type2_x + self.towerchoice_size) and mouse_x > (self.towerchoice_y) and mouse_y < (self.towerchoice_y + self.towerchoice_size):
			# clicked on tower type 1 option
			self.tower_price = tower_type2[3]
			if gamemap.current_money - self.tower_price >= 0: # checking if enough money
				self.status_text = "Tower type 2 chosen. Click to place."
				self.placing_tower = 2
			else:
				self.status_text = "Not enough money! "+str(tower_type2[3])+" required for tower type 2."
		
		elif mouse_x < 600 and mouse_y < 600:
			# clicked in playing field
			if self.placing_tower == 1 or self.placing_tower == 2:
				# a tower was selected
				self.towerPlace(mouse_x + 20, mouse_y + 20)
				"""click is rounded down to nearest multiple of 40
				-> tower would be placed between tiles
				-> compensated for by adding 20 to rounded coordinates"""

			elif self.checkGridField(mouse_x, mouse_y) == 91: # grid field value 91 = tower type 1
				# clicked on an existing tower type 1
				if gamemap.current_money - tower_type2[4] >= 0: # checking if enough money
					self.towerUpgrade(mouse_x, mouse_y)
				else:
					self.status_text = "Not enough money! "+str(tower_type2[4])+" required for upgrade."
					
			elif self.checkGridField(mouse_x, mouse_y) == 92: # grid field value 92 = tower type 2
				# clicked on an existing tower type 2
				self.status_text = "This tower type is not upgradeable."
				

	def towerPlace(self, pos_x, pos_y):
		"""placing towers"""
		if self.checkGridField(pos_x, pos_y) == 4: # checking whether it is possible to place a tower on clicked field
			if self.placing_tower == 1: # which tower type to place
				tower = Tower(pos_x, pos_y, tower_type1[0], tower_type1[1], tower_type1[2]) # spawning the tower
				tower_group.add(tower)
				self.levelMap[math.floor(mouse_y / 40)][math.floor(mouse_x / 40)] = 91 # marking the grid field as occupied by tower type 1
			if self.placing_tower == 2:
				tower = Tower(pos_x, pos_y, tower_type2[0], tower_type2[1], tower_type2[2])
				tower_group.add(tower)
				self.levelMap[math.floor(mouse_y / 40)][math.floor(mouse_x / 40)] = 92 # marking the grid field as occupied by tower type 2
			self.status_text = "Tower placed."
			self.spendMoney(self.tower_price) # deducting in-game money amount
			self.placing_tower = 0 # tower choice reset, ready for next click event
		else:
			self.status_text = "Invalid position for tower placement!"

	def towerUpgrade(self, pos_x, pos_y):
		"""upgrading towers"""
		for tower in tower_group:
			# scanning all placed towers (using tower_group), matching coordinates of clicked field with a particular tower on same field
			if (math.floor(mouse_x / 40)) == (math.floor(tower.pos_x / 40)) and (math.floor(mouse_y / 40)) == (math.floor(tower.pos_y / 40)): 
				# a matching tower found
				pygame.sprite.Sprite.kill(tower) # removing existing tower
				self.status_text = "Tower upgraded."
				self.spendMoney(tower_type2[4]) # deducting in-game money amount
				tower = Tower(pos_x + 20, pos_y + 20, tower_type2[0], tower_type2[1], tower_type2[2]) # placing a new tower
				self.levelMap[math.floor(mouse_y / 40)][math.floor(mouse_x / 40)] = 92 # marking the grid field as occupied by tower type 2
				tower_group.add(tower)

	def enemySpawn(self):
		"""spawning enemies"""
		if self.current_wave < len(wave_list):
			# last wave wasn't reached
			self.spawn_delay = (wave_list[self.current_wave][0]) * tick_time # setting the interval of spawning
			self.enemies_type1_count = wave_list[self.current_wave][1] # setting the counter of enemies of the particular type to be spawned
			self.enemies_type2_count = wave_list[self.current_wave][2]
		else:
			# last wave was reached
			self.game_end = 1 # game status: won (all waves passed)
			self.passed_ticks = 0 # protection against spawning more enemies (spawn interval grounded at 0)
				
		if self.passed_ticks >= self.spawn_delay:
			# spawning interval fulfilled
			if self.wave_underway == True:
				self.passed_ticks = 0 # reset counter (time/tick measurement)
				if self.spawned_enemies_type1 < self.enemies_type1_count:
					# number of spawned enemies not fulfilled	
					enemy = Enemy(20, 100, enemy_type1[0], enemy_type1[1])
					enemy_group.add(enemy)
					self.spawned_enemies_type1 += 1
				else:
					# number of spawned enemies of type 1 fulfilled, moving onto next type
					if self.spawned_enemies_type2 < self.enemies_type2_count:
						enemy = Enemy(20, 100, enemy_type2[0], enemy_type2[1])
						enemy_group.add(enemy)
						self.spawned_enemies_type2 += 1
					else:
						# all spawning quotas for enemy spawns for all types was fulfilled
						self.wave_underway = False
						self.spawned_enemies_type1 = 0 # reset counters
						self.spawned_enemies_type2 = 0
						self.status_text = "End of wave "+str(self.current_wave)+"."
			else:
				# wave not underway
				if self.wave_pause >= (tick_time * 5) and self.game_end == 0:
					# interval between waves fulfilled
					self.wave_pause = 0 # reset interval between waves
					self.wave_underway = True
					self.current_wave += 1
					self.status_text = "Starting wave " +str(self.current_wave)+"."
				else:
					# wait for wave interval to pass
					self.wave_pause += 1
		else:
			# wait for spawn interval to pass
			self.passed_ticks += 1
			
	def update(self):
		"""update - called on every game loop run"""
		self.moneyIndicator()
		self.statusBar()
		self.healthBar()
		self.towerChoice()
		if self.game_end == 0:
			# game still underway
			self.enemySpawn()
			
		elif self.game_end == 1:
			# game was won
			if len(enemy_group) == 0:	# checks for emptied list of enemies after last wave
				self.status_text = "GAME OVER. To exit, close the window."
				font = pygame.font.SysFont("calibri", 50)
				surface.blit(font.render("You won!", 1, (0,255,0)), (610, 250))
				
		elif self.game_end == 2:
			# game was lost
			font = pygame.font.SysFont("calibri", 54)
			surface.blit(font.render("You lost!", 1, (255,0,0)), (610, 250))				

	def checkGridField(self, x, y):
		"""checks clicked field in grid; finds the value of the grid field in the game map"""
		self.grid_field_x = math.floor(x / 40) # dividing by 40 (grid fields are 40x40 pixels) - to bring the index in map grid list file
		self.grid_field_y = math.floor(y / 40)
		self.grid_value = (self.levelMap[self.grid_field_y][self.grid_field_x])
		return self.grid_value


class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y, image, health):
		super().__init__()
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.center = [pos_x, pos_y]
		self.pos_x = gamemap.start_point_x # spawning coordinates
		self.pos_y = gamemap.start_point_y
		self.movement_var = 0 # 0 = look for path; 1 = up, 2 = right, 3 = down, 4 = left
		self.moved_pixels = 0 # counter for movement
		self.goRightOk = True # memory device to avoid 180 degree turns
		self.goLeftOk = True
		self.goUpOk = True
		self.goDownOk = True
		self.current_health = health
	


	def findPath(self):
		"""checking all cardinal directions for a continuing path"""
		if self.goRightOk == True:
			# movement to the right not locked
			if gamemap.checkGridField(self.pos_x + 21, self.pos_y) == 0:
				# path was succesfully found
				self.movement_var = 2
				self.goLeftOk = False # protection against turning 180° and returning via same path; will be unlocked again by finishing movement to a non-opposite direction
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
		"""movement method"""
		if self.moved_pixels <= 39:
			# counter didn't reach the value of the field's size yet
			self.moved_pixels += 1 # counter add
			self.rect.move_ip(1, 0)
			self.pos_x += 1	# updating coordinates
		else:
			# already moved one field size -> stop movement
			self.movement_var = 0 # look for next path
			self.moved_pixels = 0 # counter reset
	
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
		"""the enemy got hit by a bullet"""
		self.current_health -= amount
		if self.current_health <= 0:
			# enemy's health reduced to none -> enemy eliminated
			pygame.sprite.Sprite.kill(self) # remove the enemy
			gamemap.getMoney(20) # add money to player's balance
	

	def update(self):
		"""update - called on every game loop run"""
		if self.pos_x >= 570:
			# reached the end of the map
			pygame.sprite.Sprite.kill(self) # remove the enemy
			gamemap.getDamage(20) # reduce player's health
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
		
		

class Tower(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y, image, cooldown, bullet_type):
		super().__init__()
		self.cooldown = cooldown
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.image = image
		self.rect = self.image.get_rect()
		"""remark: the texture is oversized, includes invisible parts overlaping onto enemy path
		-> enemy in range = enemy colliding with the tower texture
		see provided documentation for further reference"""
		self.rect.center = [pos_x, pos_y]
		self.know_target = False # states whether the tower has a target to aim at
		self.shot_elapsed_time = cooldown # tick counter - tower's shooting cooldown
		self.bullet_type = bullet_type
			
	def findTarget(self, target_x, target_y):
		"""called when an enemy has entered the tower's range box -> sets the target"""
		self.target_x = target_x
		self.target_y = target_y
		if self.know_target == False:
			self.know_target = True
			
	def shoot(self, target_x, target_y):
		"""shooting method - spawn bullets"""
		self.know_target = False # target reset: protection against targeting enemies already outside the tower's range
		if self.shot_elapsed_time >= self.cooldown:	
			# cooldown tick counter fulfilled
			if self.bullet_type == 1:
				bullet = Bullet(self.pos_x, self.pos_y, target_x, target_y, bullet_type1[0], bullet_type1[1], bullet_type1[2])
			if self.bullet_type == 2:
				bullet = Bullet(self.pos_x, self.pos_y, target_x, target_y, bullet_type2[0], bullet_type2[1], bullet_type2[2])
			bullet_group.add(bullet)
			self.shot_elapsed_time = 0 # cooldown reset
			
	def update(self):
		"""update - called on every game loop run"""
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
		# calculating movement vectors:
		self.vector_x = (self.target_x - self.pos_x) * 0.09
		self.vector_y = (self.target_y - self.pos_y) * 0.09
		# multiplied by a set amount < 1 to facilitate credible movement: see provided documentation for further reference
			
	def update(self):
		self.move()
		if self.pos_x < (self.start_x - self.reach) or self.pos_x > (self.start_x + self.reach) or self.pos_y < (self.start_y - self.reach) or self.pos_y > (self.start_y + self.reach):
			# bullet has reached its maximum range -> self-destructed
			pygame.sprite.Sprite.kill(self)
	
	def move(self):
		# movement along X axis:
		self.rect.move_ip(self.vector_x, 0)
		self.pos_x += self.vector_x	# position update
		# movement along Y axis:
		self.rect.move_ip(0, self.vector_y)
		self.pos_y += self.vector_y
	
	
	
	
os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init() #pygame initialisation

surface = pygame.display.set_mode((800, 630)) # screen initialisation

pygame.display.set_caption("TOWER DEFENSE") # window name

gamemap = GameMap()

clock = pygame.time.Clock()
 

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			
		if event.type == pygame.MOUSEBUTTONDOWN:
			# mouse click detected
			mouse_x_raw, mouse_y_raw = pygame.mouse.get_pos()
			mouse_x = (math.floor(mouse_x_raw / 40) * 40)
			mouse_y = (math.floor(mouse_y_raw / 40) * 40)
			# coordinates rounded down to nearest multiply of 40 in order to easily match it with its relevant index in the game map file
			gamemap.checkMouseIntentions(mouse_x, mouse_y)
				
	for tower in tower_group:
		enemy_colliding = pygame.sprite.spritecollide(tower, enemy_group, False)
		# enemy collision with a tower / its texture (= the enemy is in the tower's range, see explanation in tower class constructor)
		for enemy in enemy_colliding:
			tower.findTarget(enemy.pos_x, enemy.pos_y)
			break

	for bullet in bullet_group:
		for enemy in enemy_group:
			if pygame.sprite.spritecollide(enemy, bullet_group, True):
				# enemy collision with a bullet detected
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
