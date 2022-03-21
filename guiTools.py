import pygame

#Render text with pygame.
#Pygame does not support newlines so this a quick work around.
def text(screen,text,x,y,fontsize=30,basecolor=(0, 0, 0)):
	pygame.font.init()
	font = pygame.font.SysFont('arial', fontsize)
	text = text.split('\n')
	for t in range(len(text)):
		surf = font.render(text[t], False, basecolor)
		screen.blit(surf,(x,y+(fontsize*t)))


#Render string so newlines are used and implement basic color code support.
def advancedText(screen,text,x,y,fontsize=30,basecolor=(0, 0, 0)):

	pygame.font.init()
	font = pygame.font.SysFont('arial', fontsize)
	text = text.split('\n')

	#Loop all text cut by newlines.
	for t in range(len(text)):
		

		#loop all parts of the text by color codes.
		parts = text[t].split('$c')
		for p in range(len(parts)):
			surf = font.render(text[t], False, basecolor)
			screen.blit(surf,(x+(fontsize*p),y+(fontsize*t)))
			print(parts[p])


		print(text[t])
		#surf = font.render(text[t], False, basecolor)
		#screen.blit(surf,(x,y+(fontsize*t)))


if __name__ == "__main__":
	text = '''This is a test \nyes $ctest $c is cool \n'''
	advancedText(None,text,10,10,fontsize=30,basecolor=(0, 0, 0))





