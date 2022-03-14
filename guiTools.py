import pygame

#Render text with pygame.
#Pygame does not support newlines so this a quick work around.
def text(screen,text,x,y,fontsize=30,color=(0, 0, 0)):
	pygame.font.init()
	font = pygame.font.SysFont('arial', fontsize)
	text = text.split('\n')
	for t in range(len(text)):
		surf = font.render(text[t], False, color)
		screen.blit(surf,(x,y+(fontsize*t)))





