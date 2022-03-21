import pygame
from pygame.locals import *
import automataVisualizer
from guiTools import *
import time
import winsound


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

aut.newRandomColonies(amount=4)

done = False
while done == False:
	mouse_x, mouse_y = pygame.mouse.get_pos()
				
	if sr == 0:
		screen.fill((127, 130, 129))
		aut.Render(screen)
		#text(screen,aut.Stats(),20,20,30)

		if doSimulate:
			if aut.CalculateAliveColonies() > 1:
				aut.Simulate()
			else:
				winsound.Beep(400, 1000)
				doSimulate = False
	

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
