# imports
import pygame, sys, time, pygame.display, random
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
metroidnormal = "img/metroidwalking4.png"
metroidattacking2 = "img/metroidattacking2.png"
metroidattacking3 = "img/metroidattacking3.png"
gameover_screen = "img/gameover.jpg"
ridley_img = "img/ridley.png"
ridbeam_img = "img/wingattack.png"
win = "img/metroidwin.jpg"
metroidwalk1 = "img/metroidwalking1.png"
metroidwalk2 = "img/metroidwalking3.png"
devil_right = "img/yellowdevil.png"
devilattack = "img/smileyattack.png"
startscreen_img = "img/startscreen.jpg"

# housekeeping
pygame.init()
screen = pygame.display.set_mode((800,500),0,32)
gameoverscreen = pygame.display.set_mode((800,500),0,32)
gameover_background = pygame.image.load(gameover_screen).convert()
background = pygame.image.load(bif).convert()
startscreen = pygame.image.load(startscreen_img).convert()
wingame = pygame.image.load(win).convert()

#Colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)

# state:[jump,direction,motion]
samus = {"x":400,"y":360,"hp":100,"ammo":400,"dx":0,"dy":0,"current_img":mif,"state":[0,0,0]}
metroid = {"x": 600, "y":280, "hp":10000000000000, "current_img":metroidnormal, "met_state":0}
ridley = {"x": 1, "y":280, "hp":5000, "current_img":ridley_img}
devil = {"x":500, "y":143, "hp":99999999999, "current_img":devil_right}
blasts = []
x=30
y=345
ydx=600
ydy=345
ydx2=600
ydy2=random.randint(300, 360)
ydy3=random.randint(0,500)
ydx3=random.randint(0,500)

pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.load('boss.ogg')
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1.0)

clock=pygame.time.Clock()
speed=150

startgame = False
samusdie = False

if samusdie == True:
	pygame.mixer.music.set_volume(1.0)
	pygame.mixer.music.load('gameover.ogg')
	pygame.mixer.music.set_volume(1.0)
	pygame.mixer.music.play(1)
	pygame.mixer.music.set_volume(1.0)

# GAME LOOP
while True:

	# time
	time_elapsed_since_last_action = 0
	milli=clock.tick()
	seconds=milli/1000.
	dm=seconds*speed
	digit = int(str(time.clock()).split(".")[1]) / 10
	time_elapsed_since_last_action += milli

	# events
	for event in pygame.event.get():
		#start game when key pressed
		if event.type==KEYDOWN:
			if event.key==K_s:
				startgame = True

		# quit game
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if startgame == True:
			# key down
			if event.type==KEYDOWN:
				# key left
				if event.key==K_LEFT:
					samus['dx']=-1.5
					samus['state'][1] = 0
					samus['state'][2] = 1

				# key right
				elif event.key==K_RIGHT:
					samus['dx']=+1.5
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

	if samus['y'] < 170:
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
	#too close to ridley
	if samus['x']<ridley['x']+88:
		samus['hp'] -= 20
		samus ['dx'] = +5

	#ridley attacking you
	if startgame == True:
		if samus['x'] <= x and x <= samus['x'] + 40 and samus['y'] == 360:
			samus['hp'] -= 1
	
	#attacking ridley
	if startgame == True: 
		for blast in blasts:
			if ridley['x'] <= blast['x'] and blast['x'] <= ridley['x'] + 100:
				ridley['hp'] -= 1

	#metroid moving
	if startgame == True:
		if digit % 2 == 0:
			metroid['current_img'] = metroidwalk1
		else:
			metroid['current_img'] = metroidwalk2

	#too close to metroid
	if startgame == True:
		if metroid['x'] <= samus['x'] and samus['x'] <= metroid['x'] + 100 and samus['y']>=360:
			samus['hp'] -= 1
			samus ['dx'] = -10

		for blast in blasts:
			if metroid['x'] <= blast['x'] and blast['x'] <= metroid ['x'] + 110:
				metroid['hp'] -= 2

	#metroid homing into you
	if startgame == True:
		if samus['x'] < metroid['x']:
			metroid['x'] -= 0.6
		if metroid ['hp'] <= 9500:
			metroid ['x'] == 600
		if samus['x'] > metroid['x']+110:
			metroid['y']-=100
			metroid['x']+=240
			metroid['y']+=100

	#play gameover music
	if samusdie == True:
		pygame.mixer.music.set_volume(1.0)
		pygame.mixer.music.load('gameover.ogg')
		pygame.mixer.music.set_volume(1.0)
		pygame.mixer.music.play(1)
		pygame.mixer.music.set_volume(1.0)


	# display text
	font = pygame.font.Font(None, 30)
	textImg = font.render("SAMUS HEALTH: " + str(samus['hp']) + " AMMO: " + str(samus['ammo']), 1, (255, 0, 0))
	textbossImg = font.render ("RIDLEY HEALTH: " + str(ridley['hp']), 1, (255, 0, 0))
	textfinalbossImg = font.render ("YELLOW DEVIL HEALTH: " + str(devil['hp']), 1, (255, 0, 0))
	textcontrols = font.render ("x=jump  z=fire   left arrow=left   right arrow=right   press s to start", 1, (255, 0, 0))
	
	# update current state of sprite
	if startgame == True:
		sprite = pygame.image.load(samus['current_img']).convert_alpha()
		metroid_sprite = pygame.image.load(metroid['current_img']).convert_alpha()
		ridley_sprite = pygame.image.load(ridley['current_img']).convert_alpha()
		devil_sprite = pygame.image.load(devil['current_img']).convert_alpha()
		blast_sprite = pygame.image.load(blast_img).convert_alpha()
		ridattack_sprite = pygame.image.load(ridbeam_img).convert_alpha()
		devilattack_sprite = pygame.image.load(devilattack).convert_alpha()
		devilattack_sprite2 = pygame.image.load(devilattack).convert_alpha()
		devilattack_sprite3 = pygame.image.load(devilattack).convert_alpha()

	# artsy stuff
	if startgame == False:
		screen.blit (startscreen, (0,0))
		screen.blit(textcontrols,(80,420))
	if startgame == True:
		screen.blit (background, (0,0))
		screen.blit (sprite, (samus['x'],samus['y']))
		screen.blit (metroid_sprite, (metroid ['x'], metroid ['y']))
		screen.blit (ridley_sprite, (ridley ['x'], ridley ['y']))
		screen.blit (ridattack_sprite, (x,y))
	x+=5
	y==345

	if x>800:
		x=0

	
	if samus['hp']<=0:
		samus['ammo'] -= 100000
		screen.fill(BLACK)
		text = font.render("Game Over", True, WHITE)
		text_rect = text.get_rect()
		text_x = screen.get_width() / 2 - text_rect.width / 2
		text_y = screen.get_height() / 2 - text_rect.height / 2
		screen.blit(text, [text_x, text_y])
		samus['hp'] -= 10000000000
		metroid['hp'] += 10000000000
		ridley['hp'] += 1000000000
		devil['hp'] += 1000000000
		samusdie = True

	if devil['hp']<=0:
		samus['ammo'] -= 100000
		screen.fill(BLACK)
		text = font.render("YOU WIN!!! Game by Deepak Ramalingam", True, WHITE)
		text_rect = text.get_rect()
		text_x = screen.get_width() / 2 - text_rect.width / 2
		text_y = screen.get_height() / 2 - text_rect.height / 2
		screen.blit(text, [text_x, text_y])
		samus['hp'] += 99999999999999
		metroid['hp'] -= 99999999999999
		ridley['hp'] -= 99999999999999
		devil['hp'] -= 99999999999999
		pygame.mixer.music.set_volume(1.0)
		pygame.mixer.music.load('gameover.ogg')
		pygame.mixer.music.set_volume(1.0)
		pygame.mixer.music.play(1)
		pygame.mixer.music.set_volume(1.0)

	if startgame == True:
		for blast in blasts:
			if samus['hp']>=0:
				if samus['hp']<1000:
					if (blast['x'] <= 800 or blast['x'] >= -100):
						screen.blit (blast_sprite, (blast['x'],blast['y']))

	#Final Boss Comming After Ridley Dies
	if startgame == True:
		if samus ['hp'] > 0:
			if samus['hp'] < 1000:
				screen.blit(textImg,(0,0))
				if ridley['hp']>0:
					screen.blit(textbossImg,(0,30))
	if ridley['hp']<=0:
		if samus['hp']>=0:
			if samus['hp']<1000:
				ridley['x']-=1#making everything dissappear
				ridley['y']+=1
				metroid['y']-=10000000
				metroid['x']+=10000000000
				x-=10
				y+=1000
				screen.blit (devil_sprite, (devil ['x'], devil ['y']))#yellow devil blitting
				if samus ['hp'] > 0:
					if samus ['hp'] < 1000:
						screen.blit(textfinalbossImg,(0,30))

		#blob hurting you
		if ydx <= samus['x'] and samus['x'] <= ydx + 25:
			if ydy <= samus['y'] and samus['y'] <= ydy + 25:
				samus['hp'] -= 5
				samus['y'] -= 10

		if ydx2 <= samus['x'] and samus['x'] <= ydx2 + 25:
			if ydy2 <= samus['y'] and samus['y'] <= ydy2 + 25:
				samus['hp'] -= 5

		if ydx3 <= samus['x'] and samus['x'] <= ydx3 + 25:
			if ydy3 <= samus['y'] and samus['y'] <= ydy3 + 25:
				samus['hp'] -= 5

		#yellow blobs
		if samus['hp']>=0:
			if samus['hp']<1000:
				screen.blit(devilattack_sprite, (ydx2,ydy2))#left-right yellow blob
				ydx2-=5
				if ydx2<=0:
					ydx2=600
					ydy2=random.randint(300, 360)

				screen.blit(devilattack_sprite, (ydx3,ydy3))#up-down yellow blob
				ydy3+=7
				if ydy3>=500:
					ydy3=random.randint(0,500)
					ydx3=random.randint(0,500)

				screen.blit(devilattack_sprite, (ydx,ydy))#stalker blob
				if samus['x']>ydx:
					ydx+=0.5
				if samus['x']<ydx:
					ydx-=0.5
				if samus['y']>ydy:
					ydy+=0.5
				if samus['y']<ydy:
					ydy-=0.5

				if samus['x']>=490:
					samus['hp']-=30
					samus['x']-=300
				for blast in blasts:
					if blast['x']>=490:
						devil['hp']-=5000000
				if y == 1345:
					pygame.mixer.music.set_volume(0.8)
					pygame.mixer.music.load('finalboss.ogg')
					pygame.mixer.music.set_volume(0.8)
					pygame.mixer.music.play(-1)
					pygame.mixer.music.set_volume(0.8)
					samus['hp']+=200

	# update display
	pygame.display.update()