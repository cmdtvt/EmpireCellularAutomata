import random

class Cell():
    def __init__(self,colonyID,strength=None,ageMax=None):
        self.colony = colonyID
        self.strength = random.randrange(5,12)
        self.age = 0
        self.ageMax = random.randrange(5,8)
        self.rprChance = 40
        self.mutateRate = 1

        if strength:
            self.strength = strength 
        if ageMax:
            if ageMax <= 20:
                self.ageMax = ageMax
        #if rprChance:
            #self.rprChance = rprChance
        #if mutateRate:
            #self.mutateRate = mutateRate

    def createMutate(self,):
        traits = [self.strength,self.ageMax]
        for i,t in enumerate(traits):
            if bool(random.getrandbits(1)):
                traits[i] = t+self.mutateRate
            else:
                traits[i] = t-self.mutateRate
        return Cell(self.colony,*traits)

class Node():
    def __init__(self,x,y):
        self.x = x
        self.y = y

        self.cellReference = None
        self.nodeReferences = None
        self.nodeRefDirs = {
            "topleft":0,
            "top":1,
            "topright":2,
            "left":3,
            "center":4,
            "right":5,
            "bottomleft":6,
            "bottom":7,
            "bottomright":8
        }

    def simulate(self,):
        if self.cellReference:
            cell = self.cellReference

            cell.age += 1
            if cell.age > cell.ageMax:
                self.cellKill()

            if random.randrange(0,100) <= cell.rprChance:
                self.cellReproduce()
                

            #Movement code
            move_dir = random.choice(["top","bottom","right","left"])
            if not self.cellMove(move_dir):
                self.cellAttack(move_dir)



    def cellMove(self,direction):
        if self.nodeRefrences[self.nodeRefDirs[direction]] != None: #Check if position has node
            if self.nodeRefrences[self.nodeRefDirs[direction]].cellReference == None: #Check if position is not occupied
                self.nodeRefrences[self.nodeRefDirs[direction]].cellReference = self.cellReference
                self.cellReference = None
                return True
        return False


    def cellAttack(self,direction):
        target = self.nodeRefrences[self.nodeRefDirs[direction]]
        if target != None:
            if target.cellReference != None and self.cellReference != None: #Check if position is occupied
                #if self.nodeRefrences != None and target != None:
                if target.cellReference.colony != self.cellReference.colony:
                    if target.cellReference.strength > self.cellReference.strength:
                        self.cellKill()
                    elif target.cellReference.strength < self.cellReference.strength:
                        target.cellReference = None
                    elif target.cellReference.strength == self.cellReference.strength:
                        target.cellReference = None
                        self.cellKill()
                    return True
        return False

    def cellKill(self,atype=None):
        self.cellReference = None

    def cellReproduce(self,):
        if self.nodeRefrences != None and self.cellReference != None:
            empty = []
            foundPartner = False
            for n in self.nodeRefrences:
                if n != None:
                    #Find all empty spots where child can be made.
                    if n.cellReference == None:
                        empty.append(n)
                    #Check if the cells are in same colony
                    elif n.cellReference.colony == self.cellReference.colony:
                        if n.x != self.x and n.y != self.y: #Make sure cells dont mate with themselfs.
                            foundPartner = True
                
            if len(empty) > 0 and foundPartner == True:
                random.choice(empty).cellReference = self.cellReference.createMutate()#Cell(self.cellReference.colony)
                return True
        return False

    def getPos(self,):
        return (self.x,self.y)


class Automata():
    def __init__(self):
        self.simulationSteps = []
        self.temp_nodes = {}
        self.nodes = []

        #Colony names for the stats function.
        self.names = ["no names set"]
        try:
            file = open("names.txt", "r")
            self.names = file.readlines()
            file.close()
        except:
            print("Error reading names.txt file")


        self.statData = {
            "steps":0,
            "totalKills":0,
            "colonies":{

            }
        }

        #World max size in cells
        self.maxWidth = 100
        self.maxHeight = 100


        for y in range(self.maxHeight):
            self.temp_nodes[y] = {}
            for x in range(self.maxWidth):
                self.temp_nodes[y][x] = Node(x,y)

        for y in self.temp_nodes.keys():
            self.nodes.extend(list(self.temp_nodes[y].values()))


        #Initialize refrence nodes.
        for n in self.nodes:
            temp_refs = []
            for y in range(3):
                for x in range(3):

                    #Select left top node with current node as center offset
                    locx = (x-1)+n.x
                    locy = (y-1)+n.y

                    #Check if node exsists in location.
                    if locy in self.temp_nodes and locx in self.temp_nodes[locy]:
                        temp_refs.append(self.temp_nodes[locy][locx])
                    else:
                        temp_refs.append(None)

            n.nodeRefrences = temp_refs

    def newCell(self,x=0,y=0,colonyID=0):
        if y in self.temp_nodes and x in self.temp_nodes[y]:
            self.temp_nodes[y][x].cellReference = Cell(colonyID)

        '''
        name = random.choice(['Jaska','Marko','Derppis','Topisetä','Sarita','Tommo','Keisari','Dotto'])

        if not colonyID in self.statData['colonies']:
            self.statData['colonies'][colonyID] = {
                'name':name,
                'strn':0,
                'cells':0
            }
        '''

    def newColony(self,sx,sy,colonyID):
        for y in range(3):
            for x in range(3):
                self.newCell(x+sx,y+sy,colonyID)






    def GenStartPos(self,colonies=2,separation=25):
        temp = 0
        for c in range(colonies):
            for y in range(3):
                for x in range(3):
                    self.temp_nodes[y][x+temp].cellRefrence = Cell(c)
                    #print(self.temp_nodes[y][x+temp].cellRefrence.colony)
            temp += separation

    def Simulate(self,steps=1):
        for i in range(steps):
            for n in self.nodes:
                n.simulate()
        self.statData['steps'] += 1

    def SaveStep(self,):
        self.simulationSteps.append(self.nodes)

    def CalulateAliveCells(self,):
        amount = 0
        for n in self.nodes:
            if n.cellReference != None:
                amount += 1
        return amount

    def CalculateAliveColonies(self,):
        for n in self.nodes:
            if n.cellReference != None:
                cell = n.cellReference
                
                

    def Stats(self,):

        tempData = {}

        for n in self.nodes:
            if n.cellReference != None:
                cell = n.cellReference
                

                if cell.colony not in tempData:
                    tempData[cell.colony] = {
                        "totalCells":0,
                        "strength":0
                    }

                tempData[cell.colony]["totalCells"] += 1
                tempData[cell.colony]["strength"] += cell.strength

        infoText = ""
        infoText += "Simulations: "+str(self.statData['steps'])+"\n"


        for colony,colonyData in sorted(tempData.items()):
        
            infoText += "{id} {key}: {members} | {strn:.2f} | {avgStrn:.2f} \n".format(
                id=colony,
			    key="noname",
			    members=colonyData['totalCells'],
			    strn=colonyData['strength'],
			    avgStrn=(colonyData['strength']/colonyData['totalCells'])
		    )
		
        return infoText


    def LoadSimulation(self,):
        pass

if __name__ == "__main__":
    a = Automata()
