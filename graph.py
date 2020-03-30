class Task:
	def __init__(self, name, WHP, WLP, ALP, alphaLP, AHP=None, alphaHP=None):
		
		self.name = name
		self.WHP = WHP
		self.WLP = WLP
		self.ALP = ALP
		self.alphaLP = alphaLP
		self.core = None
		self.startTime = None
		self.endTime = None
		self.contingencyActivationTime = None
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
startList = []
startTimeList = []
doneList = []
timeList = []
taskList = []
contingencyEndTimeList = []
successFlag = 0

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

def getNextTask(core,currentTime=None,TBLS=None):
	if TBLS == None:
		TBLS = core.power
	max = 0
	val = 0
	for i in range(len(readyList)):
		if t[readyList[i]][TBLS]>max:
			max = t[readyList[i]][TBLS]
			val = i
	core.processingTime=t[readyList[val]][core.power]
	core.presentTask = readyList[val]
	startList.append(readyList[val])
	startTimeList.append(currentTime)
	for task in taskList:
		if task.name == readyList[val]:
			task.core = core.name
			task.startTime = currentTime
			break
	if not core.isLocked():
		core.lock()
		processingList.append(readyList.pop(val))
	else:
		print("Locked Core gets another task, error!\n")

def exitCheckTBLS(presentIterations, successFlag, processDict):
	if presentIterations >= len(processDict):
		return True
	if successFlag == 1:
		return True
	return False
	

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
	print("Initialized parameters\n")

	dependancyDict = {}
	for task in g:
		dependancyDict[task]=[]

	# print(dependancyDict)
	for taskName in g:
		task = Task(taskName, t[taskName][0],t[taskName][1],t[taskName][2],t[taskName][3])
		taskList.append(task)

	# appends latest ready elements to readyList


	# print (readyList)
	# print (dependancyDict)
	HP = Core("HP",0) #HP is 0, because the t[task][0] has HP value
	LP = Core("LP",1) # LP is 1, because the t[task][1] has LP value


# LTF algorithm
	def LTF():
		currentTime = 0
		for task in g:
			for child in g[task]:
				dependancyDict[child].append(task)
		for task in dependancyDict:
			if dependancyDict[task]==[]:
				readyList.append(task)
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
						currentTime += HP.processingTime
						LP.processingTime -= HP.processingTime # change this to min of the two
						timeList.append(currentTime)
						for task in taskList:
							if task.name == HP.presentTask:
								task.endTime = currentTime
						processingList.remove(HP.presentTask)
						updateDependancyList()
						updateReadyList()
						print(doneList)
						HP.unlock()
					if (LP.processingTime - 0.1) <= 0:
						print(LP.presentTask," finished\n")
						doneList.append(LP.presentTask)
						currentTime+=LP.processingTime 
						HP.processingTime-=LP.processingTime # change this to min of the two 
						timeList.append(currentTime)	
						for task in taskList:
							if task.name == LP.presentTask:
								task.endTime = currentTime				
						processingList.remove(LP.presentTask)
						updateDependancyList()
						updateReadyList()
						LP.unlock()
				else:
					if len(readyList)!=0:
						getNextTask(HP,currentTime)
					else:
						LP.processingTime-=0.1
						currentTime+=0.1
						if (LP.processingTime - 0.1) <= 0:
							doneList.append(LP.presentTask)
							currentTime += LP.processingTime
							timeList.append(currentTime)
							for task in taskList:
								if task.name == LP.presentTask:
									task.endTime = currentTime
							processingList.remove(LP.presentTask)
							updateDependancyList()						
							updateReadyList()
							LP.unlock()
			else :
				getNextTask(LP,currentTime)
# Uniform Scaling : Part #1 Prepare contingency time list
	readyList = []
	processingList = []	
	currentTimeContingency = 0
	for task in g:
		for child in g[task]:
			dependancyDict[child].append(task)
	for task in dependancyDict:
		if dependancyDict[task]==[]:
			readyList.append(task)
	while readyList!=[] or processingList!=[]:
		if LP.isLocked():
			LP.processingTime-=1.0
			currentTimeContingency+=1.0
			if LP.processingTime - 1.0 <=0:
				doneList.append(LP.presentTask)
				currentTimeContingency+=LP.processingTime
				LP.processingTime = 0
				contingencyEndTimeList.append(currentTimeContingency)
				for task in taskList:
					if task.name == LP.presentTask:
						task.contingencyActivationTime = currentTimeContingency
						break
				if LP.presentTask in processingList:
					processingList.remove(LP.presentTask)
				updateDependancyList()
				updateReadyList()
				LP.unlock()
		else:
			getNextTask(LP,currentTimeContingency,1)
	print(contingencyEndTimeList)
# Uniform Scaling : Part #2 Find out scaling factor

# TBLS Algorithm
 	
	presentIteration = 0
	successFlag = 0
	thresholdTime = 65
	while not exitCheckTBLS(presentIteration,successFlag,t):
		currentTimeTBLS = 0
		HP.maxTasks = presentIteration
		readyList = []
		processingList = []
		doneList = []
		timeList = []
		LP.processingTime = 0
		HP.processingTime = 0
		LP.unlock()
		HP.unlock()
		for task in g:
			for child in g[task]:
				dependancyDict[child].append(task)
		for task in dependancyDict:
			if dependancyDict[task]==[]:
				readyList.append(task)
	
		while (readyList!=[] or processingList!=[]):
			# print("Entered inner while")
			if LP.isLocked():
				# print("Entered LP.isLocked")
				if HP.isLocked():
					# print("Entered HP.isLocked")
					LP.processingTime-=1.0
					HP.processingTime-=1.0
					currentTimeTBLS+=1.0
					if (HP.processingTime - 1.0 <= 0): 
						currentTimeTBLS+=HP.processingTime
						LP.processingTime-=HP.processingTime
						doneList.append(HP.presentTask)
						HP.processingTime = 0
						for task in taskList:
							if task.name == HP.presentTask:
								task.endTime = currentTimeTBLS
								break
						processingList.remove(HP.presentTask)
						timeList.append(currentTimeTBLS)
						updateDependancyList()
						updateReadyList()
						HP.unlock()
					if (LP.processingTime - 1.0 <= 0):
						currentTimeTBLS+=LP.processingTime
						HP.processingTime-=LP.processingTime
						doneList.append(LP.presentTask)
						timeList.append(currentTimeTBLS)						
						LP.processingTime = 0
						for task in taskList:
							if task.name == LP.presentTask:
								task.endTime = currentTimeTBLS
								break
						if LP.presentTask in processingList:
							processingList.remove(LP.presentTask)
						updateDependancyList()
						updateReadyList()
						LP.unlock()
				else:
					if HP.maxTasks > 0 and len(readyList)!=0:
						HP.maxTasks-=1
						getNextTask(HP,currentTimeTBLS,0)
					else:
						LP.processingTime-=1.0
						currentTimeTBLS+=1.0
						if (LP.processingTime - 1.0) <= 0:
							doneList.append(LP.presentTask)
							currentTimeTBLS += LP.processingTime
							timeList.append(currentTimeTBLS)
							for task in taskList:
								if task.name == LP.presentTask:
									task.endTime = currentTimeTBLS
									break							
							processingList.remove(LP.presentTask)
							updateDependancyList()						
							updateReadyList()
							LP.unlock()
			else:
				getNextTask(LP,currentTimeTBLS,0)
			if currentTimeTBLS > thresholdTime:
				break	
		if currentTimeTBLS < thresholdTime:
			successFlag = 1	
		# print(presentIteration)
		presentIteration+=1	
	# print(readyList)
	print(doneList)
	print(timeList)
	# LTF()
	if successFlag:
		print("Successfully Allocated")


		