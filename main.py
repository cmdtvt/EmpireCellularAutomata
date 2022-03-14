import pygame
from pygame.locals import *
import automataVisualizer
from guiTools import *
import time


pygame.init()
size = [300, 300]
screen = pygame.display.set_mode((size[0], size[1]),pygame.RESIZABLE)
pygame.display.set_caption('Game of war')
clock = pygame.time.Clock()

sr = 0
CameraSpeed = 5
ZoomSpeed = 1
doSimulate = False
count = 0
aut = automataVisualizer.Automata()

'''
aut.newColony(20,20,0)
aut.newColony(40,20,2)
aut.newColony(60,20,4)
aut.newColony(20,40,3)
aut.newColony(40,40,1)
'''
aut.newColony(40,40,5)
aut.newColony(60,40,6)
aut.newColony(40,60,7)
aut.newColony(60,60,8)

aut.newColony(50,50,9)
#aut.newColony(2,2,69)
#aut.newCell(2,2,69)

done = False
while done == False:
	mouse_x, mouse_y = pygame.mouse.get_pos()
				
	if sr == 0:
		screen.fill((127, 130, 129))
		aut.Render(screen)
		#text(screen,aut.Stats(),20,20,30)

		if doSimulate:
			aut.Simulate()
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_p:
				aut.Simulate()

			if event.key == pygame.K_b:
				if doSimulate:
					doSimulate = False
				else:
					doSimulate = True

			if event.key == pygame.K_ESCAPE:
				done = True

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 4:
				aut.ChangeZoom(ZoomSpeed)

			elif event.button == 5:
				aut.ChangeZoom(-ZoomSpeed)

	keys = pygame.key.get_pressed()
	
	if keys[pygame.K_w]:
		aut.MoveCamera(0,CameraSpeed)
	if keys[pygame.K_s]:
		aut.MoveCamera(0,-CameraSpeed)
	if keys[pygame.K_a]:
		aut.MoveCamera(CameraSpeed,0)
	if keys[pygame.K_d]:
		aut.MoveCamera(-CameraSpeed,0)


	pygame.display.flip()
	clock.tick(200)

pygame.display.quit()
pygame.quit()
quit()
