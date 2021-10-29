import pygame

#Render text with pygame.
#Pygame does not support newlines so this a quick work around.
def text(screen,text,x,y,fontsize):
	pygame.font.init()
	font = pygame.font.SysFont('arial', fontsize)
	text = text.split('\n')
	for t in range(len(text)):
		surf = font.render(text[t], False, (0, 0, 0))
		screen.blit(surf,(x,y+(fontsize*t)))





