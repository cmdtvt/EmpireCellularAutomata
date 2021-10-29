import concurrent.futures
import random
import timeit

class Automata():
	def __init__(self,colonies=2,rpThreshold=70):
		self.cells = {}
		self.cellData = {}
		self.largestCellID = 0
		self.colors = []
		self.colonies = colonies
		self.stepsSimulated = 0
		self.cellRandomMaxStrength = 8
		self.statsData = {
			"totalDead":0,
			"totalNewBorn":0,
			"totalKills":0,
			"colonyStrength":0
		}

		#If number 0-100 is over this create a new cell
		self.rpTreshold = rpThreshold 
		for c in range(self.colonies):
			self.colors.append(
				(
					random.randrange(0,254),
					random.randrange(0,254),
					random.randrange(0,254)
				)
			)

	#Return string which contains statistics.
	#TODO: Make this thing generate stats automaticly from dictionary.
	def Stats(self,):
		infoText = ""
		colonyMembers = {}

		#Calculate amount of colony memebrs in each colony
		for cellID,cell in self.cellData.items():
			if cell["colonyID"] not in colonyMembers:
				colonyMembers[cell["colonyID"]] = {
					"amount":0,
					"totalStrngth":0,
				}
			colonyMembers[cell["colonyID"]]["totalStrngth"] += cell["strength"]
			colonyMembers[cell["colonyID"]]["amount"] += 1



		infoText += "Simulations: "+str(self.stepsSimulated)+"\n"
		infoText += "totalNewBorn: "+str(self.statsData["totalNewBorn"])+"\n"
		infoText += "totalDead: "+str(self.statsData["totalDead"])+"\n"
		infoText += "totalKills: "+str(self.statsData["totalKills"])+"\n"
		infoText += "Cells | Strength | AVG Sstrength \n"
		for key,value in colonyMembers.items():
			infoText += "{key}: {members} | {strn} | {avgStrn:.2f} \n".format(
				key=key,
				members=value["amount"],
				strn=value["totalStrngth"],
				avgStrn=value["totalStrngth"]/value["amount"]
			)
		
		
		return infoText
			

	def generate(self,chance=50,xMax=200,yMax=200):
		cellsMade = 0
		for y in range(yMax):
			for x in range(xMax):
				if random.randrange(0,101) > chance:
					cellsMade += 1
					
					self.newCell(x,y,random.randrange(0,self.colonies),random.randrange(4,20))
		print("Cells made: ",cellsMade)
	
	#Check if x y position has something.
	def checkLocation(self,x,y):
		if y in self.cells:
			if x in self.cells[y]:
				return True
		return False

	#Check area around certain location. Return all valid locations.
	def checkArea(self,cx,cy):
		freeLoc = []
		for y in range(3):
			for x in range(3):

				#Offset the area we are looking in so that its center is
				#cx and cy center.
				location_x = (x-1)+cx
				location_y = (y-1)+cy
				#If location does not have anything add it to a list.
				if not self.checkLocation(location_x, location_y):
					freeLoc.append([location_x,location_y])

		return freeLoc

	#Creates dictionary keys so there is no crash later.
	def prepareLocation(self,x,y):
		if y not in self.cells:
			self.cells[y] = {}

	#Create a new cell and add it to cells and cellData
	def newCell(self,x,y,colonyID,strength=None):
		if self.checkLocation(x,y) == False:
			self.prepareLocation(x,y)
			self.largestCellID += 1

			if strength == None:
				strength = random.randrange(5,self.cellRandomMaxStrength)

			self.cellData[self.largestCellID] = {
				'strength':strength,
				'cellID':self.largestCellID,
				'colonyID':colonyID,
				'age':0,
				'rpValue':self.rpTreshold
			}
			self.cells[y][x] = self.largestCellID

			self.statsData["totalNewBorn"] += 1

	#Create a starting layout for colony.
	def newColony(self,cx,cy,colonyID):
		for y in range(3):
			for x in range(3):
				location_x = (x-1)+cx
				location_y = (y-1)+cy
				self.newCell(location_x,location_y,colonyID,random.randrange(5,10))

	#Find cell location in dictionary with cellID
	def findCellLocation(self,cellID):
		for y in self.cells:
			for x in self.cells[y]:
				if self.cells[y][x] == cellID:
					return [x,y]
		return False
		
	#Delete info about a cell with cellID
	def destroyCell(self,cellID):
		temp_val = self.findCellLocation(cellID)
		if temp_val != False: #If wanted cell was found.
			#Delete cell from cells dict and cellData dict.
			del self.cells[temp_val[1]][temp_val[0]]
			del self.cellData[cellID]
			return True

		return False

	#Move cell in x,y to another x,y
	def moveCell(self,x,y,tx,ty):
		if self.checkLocation(tx,ty) == False:
			self.prepareLocation(tx,ty)
			self.cells[ty][tx] = self.cells[y][x]
			del self.cells[y][x]
			return True
		return False

	#Compare two cells strength value.
	#One that has less is loses and is returned.
	def battleCells(self,x,y,ox,oy):
		if self.checkLocation(ox,oy) == True:
			
			c1 = self.cellData[self.cells[y][x]]
			c2 = self.cellData[self.cells[oy][ox]]

			#If fighting tiles are in different colony
			if c1["colonyID"] != c2["colonyID"]: 
				self.statsData["totalKills"] += 1
				if c1["strength"] > c2["strength"]:
					return self.cells[y][x]
				return self.cells[oy][ox]
		return False

		


	#Simulate a single step
	def step(self,):

		#Reset stats
		self.statsData["totalNewBorn"] = 0
		self.statsData["totalDead"] = 0
		self.statsData["totalKills"] = 0


		print("Simulating a step: ",self.stepsSimulated)
		start = timeit.default_timer() #Checking how long one step takes.
		
		toBeDestroyed = []
		toBeReproduced = []
		for cellID, value in self.cellData.items():
			#If cells age is bigger than strength add cellID to kill queue.
			if value['age'] > value['strength']:
				toBeDestroyed.append(cellID)
				continue
			
			#Check if unit should reproduce.
			if random.randrange(0,101) > value['rpValue']:
				toBeReproduced.append(cellID)
			self.cellData[cellID]['age'] += 1

		

		#TODO: It might be faster to get cells from cellData
		moveActions = []
		for y, tcells in self.cells.items():
			for x, value in tcells.items():

				#Up down left right
				temp_direction = random.randrange(1,5)
				if temp_direction == 1:
					moveActions.append([x,y,x,y-1])
				elif temp_direction == 2:
					moveActions.append([x,y,x,y+1])
				elif temp_direction == 3:
					moveActions.append([x,y,x-1,y])
				elif temp_direction == 4:
					moveActions.append([x,y,x+1,y])



		#TODO: This needs to be threaded. Checking for free locations takes too long.
		#Do cell reproduction.
		print("Trying to create: ",len(toBeReproduced)," new cells.")
		for i in toBeReproduced:
			searchData = self.findCellLocation(i)
			if searchData != False:
				freeLocations = self.checkArea(searchData[0],searchData[1])
				if len(freeLocations) > 0:
					temp = random.choice(freeLocations)
					strength = self.cellData[i]['strength']+random.randrange(0,5)
					self.newCell(temp[0],temp[1],self.cellData[i]["colonyID"],strength)
			else:
				#If this ever triggers there is a discrepancy in cells and cellData.
				print("Error cell not found.")


		#First do all battles after that move tiles.
		for i in moveActions:
			loser = self.battleCells(i[0],i[1],i[2],i[3])
			if loser != False:
				self.destroyCell(loser)
			self.moveCell(i[0],i[1],i[2],i[3])

		#Destroy all queued cells.
		for i in toBeDestroyed:
			self.destroyCell(i)
		print(str(len(toBeDestroyed))+" cells destroyed. "+str(len(self.cellData))+" cells left alive.")


		stop = timeit.default_timer()
		self.stepsSimulated += 1
		self.statsData["totalDead"] = len(toBeDestroyed)
		print("Step took: ", stop - start," seconds.")

		return self.cells, self.cellData