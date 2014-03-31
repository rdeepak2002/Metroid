bif = "img/bg.jpg"
mif = "img/metroidstanding.png"
rightrunning = "img/metroidrightrunning1.png"
rightrunning2 = "img/metroidrightrunning2.png"
rightfacing = "img/metroidrightfacing.png"
leftfacing = "img/metroidleftfacing.png"

import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800,500),0,32)
background=pygame.image.load(bif).convert()
metroidstanding=pygame.image.load(mif).convert_alpha()

x,y=400,360
movex, movey = 0,0

x=400
clock=pygame.time.Clock()
speed=150

state = 0

while True:

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type==KEYDOWN:

			if event.key==K_RIGHT:
				movex=+1


			elif event.key==K_LEFT:
				movex=-1

			elif event.key==K_x:
				if state == 0 and y == 360:
					state = 1

		if event.type==KEYUP:

			if event.key==K_RIGHT:
				movex=0

			elif event.key==K_LEFT:
				movex=0

			elif event.key==K_x:
				movey=0
				state = 0
				
	x+=movex
	y+=movey

	screen.blit (background, (0,0))
	screen.blit (metroidstanding, (x,y))

	milli=clock.tick()
	seconds=milli/1000.
	dm=seconds*speed
	if state == 1:
		y -= dm*3
	else:
		y +=dm*3

	if x>780:
		x=780

	if x<0:
		x=0

	if y>360:
		y=360

	if y<0:
		y=0

	if y < 200:
		state = 0

	pygame.display.update()