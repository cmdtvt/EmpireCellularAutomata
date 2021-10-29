import pygame
from pygame.locals import *
import automataVisualizer
from guiTools import *
import time


pygame.init()
size = [1900, 1000]
screen = pygame.display.set_mode((size[0], size[1]),pygame.RESIZABLE)
pygame.display.set_caption('Template')
clock = pygame.time.Clock()

sr = 0
CameraSpeed = 5
ZoomSpeed = 1

aut = automataVisualizer.Automata(4,80)

#aut.newCell(0,0,1,5)
#aut.newCell(2,0,1,2)
#aut.newCell(1,1,2,3)
#aut.newCell(2,1,2,1)

#aut.generate(99,400,150)

aut.newColony(0,0,0)
aut.newColony(20,0,1)
aut.newColony(0,20,2)
aut.newColony(20,20,3)

#print(aut.cells)
#print(aut.cellData)

done = False
while done == False:
	mouse_x, mouse_y = pygame.mouse.get_pos()
				
	if sr == 0:
		screen.fill((255,255,255))
		aut.Render(screen)
		text(screen,aut.Stats(),20,20,30)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True


		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_p:
				aut.step()

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
	clock.tick(60)

pygame.display.quit()
pygame.quit()
quit()
