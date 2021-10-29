import pygame
from pygame.locals import *
import automata

#Render automata class with pygame.
class Automata(automata.Automata):
    def __init__(self,colonies,rpTreshold):
        super(Automata, self).__init__(colonies,rpTreshold)
        self.cellRenderOffsetX = 20
        self.cellRenderOffsetY = 20
        self.cellSize = 20
        self.zoomlevel = 0

    def Render(self,screen):
        for y,value in self.cells.items():
            for x,cellID in value.items():
                pygame.draw.rect(
                    screen,
                    self.colors[self.cellData[cellID]['colonyID']],
                    pygame.Rect(
                        (x*self.cellSize+self.cellRenderOffsetX),
                        (y*self.cellSize+self.cellRenderOffsetY),
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
    am.generate(10,40,40)
    #am.Render("yeeet")
    #am.test()