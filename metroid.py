# imports
import pygame, sys, time, pygame.display
from pygame.locals import *
# images
bif = "img/bg.jpg"
mif = "img/metroidstanding.png"
rightrunning = "img/metroidrightrunning1.png"
rightrunning2 = "img/metroidrightrunning2.png"
rightfacing = "img/metroidrightfacing.png"
leftfacing = "img/metroidleftfacing.png"
leftrunning = "img/metroidleftrunning1.png"
leftrunning2 = "img/metroidleftrunning2.png"
blast_img = "img/blast.png"
metroidnormal = "img/metroidnormal.png"
metroidattacking1 = "img/metroidattacking1.png"
metroidattacking2 = "img/metroidattacking2.png"
metroidattacking3 = "img/metroidattacking3.png"

# housekeeping
pygame.init()
screen = pygame.display.set_mode((800,500),0,32)
background=pygame.image.load(bif).convert()

# state:[jump,direction,motion]
samus = {"x":400,"y":360,"hp":100,"ammo":1000,"dx":0,"dy":0,"current_img":mif,"state":[0,0,0]}
metroid = {"x": 600, "y":280, "hp":1000, "current_img":metroidnormal, "met_state":0}
blasts = []

pygame.mixer.music.load('boss.ogg')
pygame.mixer.music.play(-1)

clock=pygame.time.Clock()
speed=150

# GAME LOOP
while True:

	# time
	milli=clock.tick()
	seconds=milli/1000.
	dm=seconds*speed
	digit = int(str(time.clock()).split(".")[1]) / 10

	# events
	for event in pygame.event.get():

		# quit game
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		# key down
		if event.type==KEYDOWN:

			# key left
			if event.key==K_LEFT:
				samus['dx']=-1
				samus['state'][1] = 0
				samus['state'][2] = 1

			# key right
			elif event.key==K_RIGHT:
				samus['dx']=+1
				samus['state'][1] = 1
				samus['state'][2] = 1

			# key x => jump
			elif event.key==K_x:
				if samus['state'][0] == 0 and samus['y'] == 360:
					samus['state'][0] = 1

			# key z blast
			elif event.key==K_z:
				if (samus['ammo'] > 0):		
					dx = 0
					if samus['state'][1] == 0:
						dx = -2
					else:
						dx = +2

					blasts.append({"x":samus['x'], "y":samus['y'], "dx":dx})
					samus['ammo'] -= 1

		# key released
		if event.type==KEYUP:

			# key left
			if event.key==K_LEFT:
				samus['dx'] = 0
				samus['current_img'] = leftfacing
				samus['state'][1] = 0
				samus['state'][2] = 0

			# key right
			elif event.key==K_RIGHT:
				samus['dx'] = 0
				samus['current_img'] = rightfacing
				samus['state'][1] = 1
				samus['state'][2] = 0
			
			# key x => jump
			elif event.key==K_x:
				samus['dy']=0
				samus['state'][0] = 0
				
	samus['x']+=samus['dx']
	samus['y']+=samus['dy']

		# gravity
	if samus['state'][0] == 1:
		samus['y'] -= dm*3
	else:
		samus['y'] +=dm*3

	# boundaries
	if samus['x']>780:
		samus['x']=780

	if samus['x']<0:
		samus['x']=0

	if samus['y']>360:
		samus['y']=360

	if samus['y']<0:
		samus['y']=0

	if samus['y'] < 200:
		samus['state'][0] = 0

	for blast in blasts:
		blast['x'] += blast['dx']

		if blast ['x']>830:
			blasts.remove(blast)

	if samus['state'][1] == 0 and samus['state'][2] == 1:
		if digit % 2 == 0:
			samus['current_img'] = leftrunning
		else:
			samus['current_img'] = leftrunning2

	if samus['state'][1] == 1 and samus['state'][2] == 1:
		if digit % 2 == 0:
			samus['current_img'] = rightrunning
		else:
			samus['current_img'] = rightrunning2

	#too close to metroid
	if samus['x']>metroid['x']:
		metroid["met_state"] = 1
		samus['hp'] -= 40
		samus ['dx'] = -5

	if metroid['met_state'] == 1:
		if metroid['met_state'] ==1:
			#add timer
			pygame.time.Clock.tick(framerate=0)
			pygame.time.Clock.get_time()
			metroid['current_img'] = metroidattacking2
			metroid['current_img'] = metroidattacking3
			#add time
			metroid['current_img'] = metroidnormal
			metroid["met_state"] == 0

	font = pygame.font.Font(None, 30)
	textImg = font.render("SAMUS HEALTH: " + str(samus['hp']) + "                   Ammo: " + str(samus['ammo']) + "                   METROID HEALTH: " + str(metroid['hp']), 1, (255, 0, 0))

	# update current state of sprite
	sprite = pygame.image.load(samus['current_img']).convert_alpha()
	metroid_sprite = pygame.image.load(metroid['current_img']).convert_alpha()
	blast_sprite=pygame.image.load(blast_img).convert_alpha()

	# artsy stuff
	screen.blit (background, (0,0))
	screen.blit (sprite, (samus['x'],samus['y']))
	screen.blit (metroid_sprite, (metroid ['x'], metroid ['y']))

	for blast in blasts:
		if (blast['x'] <= 800 or blast['x'] >= -100):
			screen.blit (blast_sprite, (blast['x'],blast['y']))

	screen.blit(textImg,(0,0))

	# update display
	pygame.display.flip()