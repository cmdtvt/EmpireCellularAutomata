import pygame
from pygame.locals import *
import automataClassed as automata
import random
import guiTools as gt

#Render automata class with pygame.
class Automata(automata.Automata):
    def __init__(self):
        super(Automata, self).__init__()
        self.cellRenderOffsetX = 20
        self.cellRenderOffsetY = 20
        self.cellSize = 20
        self.zoomlevel = 0
        self.colors = []
        self.oldNodes = []

        self.renderGrid = False


        for c in range(100):
            self.colors.append(
                (
                    random.randrange(0,254),
                    random.randrange(0,254),
                    random.randrange(0,254)
                )
            )

    def Render(self,screen):

        gt.text(screen,self.Stats(),20,20,30,)

        for node in list(set(self.nodes) - set(self.oldNodes)):
            if self.renderGrid:
                pygame.draw.rect(screen, (64, 66, 65), ((node.x*self.cellSize+self.cellRenderOffsetX), (node.y*self.cellSize+self.cellRenderOffsetY), self.cellSize, self.cellSize), 1)  

            if node.cellReference != None:

                pygame.draw.rect(
                    screen,
                    self.colors[node.cellReference.colony],
                    pygame.Rect(
                        (node.x*self.cellSize+self.cellRenderOffsetX),
                        (node.y*self.cellSize+self.cellRenderOffsetY),
                        self.cellSize,
                        self.cellSize
                    )
                )

    def MoveCamera(self,x,y):
        self.cellRenderOffsetX += x
        self.cellRenderOffsetY += y

    def ChangeZoom(self,zoomlevel):
        self.cellSize += zoomlevel

    def test(self,):
        print("This is a test")

if __name__ == "__main__":
    am = Automata()
