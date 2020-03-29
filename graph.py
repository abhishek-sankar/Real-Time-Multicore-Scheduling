class Task:
	def __init__(self, name, WHP, WLP, ALP, alphaLP, AHP=None, alphaHP=None):
		
		self.name = name
		self.WHP = WHP
		self.WLP = WLP
		self.ALP = ALP
		self.alphaLP = alphaLP
		self.core = None
		if AHP == None:
			self.AHP = 1.0
		if alphaHP == None:
			self.alphaHP = 0.1
		
class Core:
	def __init__(self, name, power, fhpMax=None, flpMax=None, phpIdle=None, plpIdle=None):
		self.name = name
		self.power = power
		if fhpMax == None:
			self.fhpMax = 1.0
		if flpMax == None:
			self.flpMax = 0.8
		if phpIdle == None:
			self.phpIdle = 0.05
		if plpIdle == None:
			self.plpIdle = 0.02
		self.mutex = 0
		self.processingTime = 0
		self.presentTask = None
		self.maxTasks = 0

	def isLocked(self):
		return self.mutex
	def lock(self):
		if self.mutex == 0:
			self.mutex = 1
			return True # ie it worked
		elif self.mutex == 1:
			return False # ie it didn't work
	def unlock(self):
		if self.mutex == 1:
			self.mutex = 0
			return True # ie it worked
		elif self.mutex == 0:
			return False # ie it didn't work

readyList = []
processingList = []
doneList = []
timeList = []
taskList = []
doneData={}
r=[]
s=[]
frameLength=100


def checkEmpty():
	if len(readyList)==0:
		return True
	return False

def updateDependancyList():
	for i in doneList:
		for task in dependancyDict:
			if i in dependancyDict[task]:
				dependancyDict[task].remove(i)

def updateReadyList():
	for task in dependancyDict:
		if dependancyDict[task]==[]:
			if task not in doneList:
				if task not in processingList:
					if task not in readyList:
						readyList.append(task)

def getNextTask(core):
	max = 0
	val = 0
	for i in range(len(readyList)):
		if t[readyList[i]][core.power]>max:
			max = t[readyList[i]][core.power]
			val = i
	core.processingTime=t[readyList[val]][core.power]
	core.presentTask = readyList[val]
	# taskList[readyList[val]].core = core.name
	if not core.isLocked():
		core.lock()
		processingList.append(readyList.pop(val))
	else:
		print("Locked Core gets another task, error!\n")
def getNextTastTBLS(core):
	pass

def checkConditionTBLS(currentTime,presentIteration,size,thresholdValue=65):
	if currentTime < thresholdValue:
		return 0
	else:
		if presentIteration>=size:
			return None #escapePlanTBLS()  # Escape plan to be defined 
		else:
			return 1
def totalTime():
	total=[0,0]
	for i in t :
		total[0]+=t[i][0]
		total[1]+=t[i][1]
	print(total)
	return total
def updateContingencyData() :
	startTime=frameLength-totalTime()[1]
	print(startTime)
	for task in r:
		c[task][1]=startTime
		startTime+=t[task][1]
		c[task][0]=startTime-t[task][0]
	print("Contingency schedule :  :",c)
		


def findUSfactor():
	min=c["t0"][0]-doneData["t0"][0]
	minTask="t0"
	for task in r:
		if(doneData[task][1]) :
			if(min>(c[task][0]-doneData[task][0])) :
				minTask=task
				min= c[task][0] - doneData[task][0]
				contingencyCore=0
		else:
			if(min>(c[task][1]-doneData[task][0])) :
				minTask=task
				contingencyCore=1
				min=c[task][1]-doneData[task][0]
	print(minTask)
	USFactor=doneData[minTask][0]/c[minTask][contingencyCore]
	return USFactor


if __name__ == "__main__":

	g = { "t0" : ["t1","t2","t4"],
		  "t1" : ["t3","t5"],
		  "t2" : ["t6"],
		  "t3" : [],
		  "t4" : [],
		  "t5" : [],
		  "t6" : [],
		}
	t = { "t0" : [3.0,7.5,0.28,0.028],
		  "t1" : [10.0,23.1,0.45,0.045],
		  "t2" : [6.0,13.5,0.3,0.03],
		  "t3" : [6.5,14.6,0.4,0.04],
		  "t4" : [5.0,9.4,0.25,0.025],
		  "t5" : [4.5,7.9,0.2,0.02],
		  "t6" : [4.0,7.0,0.2,0.02],
		}
	c = { "t0" : [18,15],  #assuming contingency schedule --Change later
		  "t1" : [37,23],
		  "t2" : [55,48],
		  "t3" : [68,61],
		  "t4" : [78,74],
		  "t5" : [87,84],
		  "t6" : [92,95]
		}
	print("Initialized parameters\n")

	dependancyDict = {}
	for task in g:
		dependancyDict[task]=[]
	for task in g:
		for child in g[task]:
			dependancyDict[child].append(task)
	print(dependancyDict)
	for taskName in g:
		task = Task(taskName, t[taskName][0],t[taskName][1],t[taskName][2],t[taskName][3])
		taskList.append(task)

	# appends latest ready elements to readyList
	for task in dependancyDict:
		if dependancyDict[task]==[]:
			readyList.append(task)

	# print (readyList)
	# print (dependancyDict)
	HP = Core("HP",0) #HP is 0, because the t[task][0] has HP value
	LP = Core("LP",1) # LP is 1, because the t[task][1] has LP value
	# print(checkEmpty())
	# print(len(readyList))
# LTF algorithm
	def LTF():
		currentTime = 0
		while (readyList!=[] or processingList!=[]):
			if LP.isLocked():
				print("Entered LP is locked\n",LP.presentTask," executing\n",LP.processingTime," time remaining\n")
				if HP.isLocked():
					print("Entered HP is locked\n")
					currentTime+=0.1
					HP.processingTime-=0.1
					LP.processingTime-=0.1
					if (HP.processingTime - 0.1) <= 0:
						print("Entered HP.time < 0\n")
						print(HP.presentTask," finished\n")
						doneList.append(HP.presentTask)
						s.append(HP.presentTask)

						currentTime += HP.processingTime
						doneData[HP.presentTask]=[currentTime,0]
						LP.processingTime -= HP.processingTime # change this to min of the two
						timeList.append(currentTime)
						processingList.remove(HP.presentTask)
						updateDependancyList()
						updateReadyList()
						print(doneList)
						HP.unlock()
					if (LP.processingTime - 0.1) <= 0:
						print(LP.presentTask," finished\n")
						doneList.append(LP.presentTask)
						r.append(LP.presentTask)
						currentTime+=LP.processingTime 
						doneData[LP.presentTask]=[currentTime,1]
						HP.processingTime-=LP.processingTime # change this to min of the two 
						timeList.append(currentTime)					
						processingList.remove(LP.presentTask)
						updateDependancyList()
						updateReadyList()
						LP.unlock()
				else:
					if len(readyList)!=0:
						getNextTask(HP)
					else:
						LP.processingTime-=0.1
						currentTime+=0.1
						if (LP.processingTime - 0.1) <= 0:
							doneList.append(LP.presentTask)
							r.append(LP.presentTask)
							currentTime += LP.processingTime
							doneData[LP.presentTask]=[currentTime,1]
							timeList.append(currentTime)
							processingList.remove(LP.presentTask)
							updateDependancyList()						
							updateReadyList()
							LP.unlock()
			else :
				getNextTask(LP)
# TBLS Algorithm	
	def TBLS():
		thresholdValue = 65
		currentTime = 0
		presentIteration = 0
		successFlag = 0
		while checkConditionTBLS(currentTime,presentIteration,len(g)): # change condition to avoid infinite loop
			HP.maxTasks = presentIteration
			updateDependancyList()
			updateReadyList()
			while (readyList!=[] or processingList!=[]):
				if LP.isLocked():
					if HP.maxTasks > 0:
						if HP.isLocked(): # if HP can still be used but is not free right now
							HP.processingTime-=1.0
							LP.processingTime-=1.0
							currentTime+=1.0
							if (HP.processingTime - 1.0) <=0:
								currentTime+=HP.processingTime
								LP.processingTime-=HP.processingTime
								doneList.append(HP.presentTask)
								timeList.append(currentTime)
								updateDependancyList()
								updateReadyList()
								HP.unlock()
						else: # if HP is not locked
							getNextTastTBLS(LP)
					else:
						pass # if HP is at max tasks
				else:
					getNextTastTBLS(LP) # if LP is not locked
			if currentTime <= thresholdValue:
				successFlag = 1
			presentIteration+=1
	LTF()
	r=r+s
	updateContingencyData()
	print(doneData)
	print("Scaling Factor : :",findUSfactor())

		
# todo find out why 2x t1,t2 came, and also when to update ready list and other lists