import numpy as np

#pegs: goal is to move all of the disks in order onto peg 3

#Class to represent the pegs
class Peg:
    def __init__(self, numDisk, num):
        self.pegList = [None] * numDisk
        self.pegNum = num
    def add(self, disk):
        #if the disk is the first disk in or the disk below is of larger width

        if type(disk) == Disk:
            for i in range(len(self.pegList)): #run through the pegList
                # go from bottom to top
                elem = self.pegList[i]
                if elem == None: #check if the current element is empty in the list
                    # the spot where it is empty will be the spot you add the disk to
                    if i == 0: # meaning empty list
                        self.pegList[0] = disk
                        disk.setPos(self.pegNum, 0)
                    elif type(self.pegList[i - 1]) == Disk and self.pegList[i - 1].width > disk.width:
                            self.pegList[i] = disk
                            disk.setPos(self.pegNum, i)
               

    def set(self, disk, idx):
        self.pegList[idx] = disk
        disk.setPos(self.pegNum, idx)

    def pop(self):
        temp = None
        for i in range(len(self.pegList)):
            if self.pegList[len(self.pegList) - 1 - i] != None:
                temp = self.pegList[len(self.pegList) - 1 - i]
                self.pegList[len(self.pegList) - 1 - i] = None
                break
        return temp

    def getTopDisk(self):
        temp = None
        for i in range(len(self.pegList)):
            if self.pegList[len(self.pegList) - 1 - i] != None:
                temp = self.pegList[len(self.pegList) - 1 - i]
                break
        return temp

#Class to represent the disks
class Disk:
    def __init__ (self, width):
        self.width = width

    def setPos(self, pegNum, height):
        self.pegNum = pegNum
        self.height = height

    
    #Returns a tuple, 1st elem is the peg number, 2nd elem is the height on that peg (0-indexed)
    def getDiskPos(self):
        return (self.pegNum, self.height)


#Starts the game by instantiating all of the disks and the pegs
def startGame(numDisks):
    global peg1
    peg1 = Peg(numDisks, 1)
    global peg2
    peg2 = Peg(numDisks, 2)
    global peg3
    peg3 = Peg(numDisks, 3)
    #create the disks and add them to the pegs
    # instantiating the disks
    global goalState
    goalState = []
    for i in range(numDisks):
        global disk
        disk = Disk(numDisks - i)
        disk.setPos(1, i)
        # you want to add the bigger disk first
        peg1.add(disk)
        disks.insert(0, disk)
        # creating the goal state (start state was already formed from initiating the states
        goalState.append((3, numDisks - 1 - i))
    goalState = tuple(goalState)


    #heights go 0 to 2 from bottom to top; higher the higher you go up


def printGame():

    #Iterate through each peg and print the width of the disk present
    #If no disk present at that position on the peg, None is printed
    for i in range(numDisks):
        width1 = None
        width2 = None
        width3 = None
        idx = len(peg1.pegList) - i - 1
        if type(peg1.pegList[idx]) is Disk:
            width1 = peg1.pegList[idx].width
        if type(peg2.pegList[idx]) is Disk:
            width2 = peg2.pegList[idx].width
        if type(peg3.pegList[idx]) is Disk:
            width3 = peg3.pegList[idx].width

        space1 = "  "
        space2 = "  "
        space3 = "  "
        if width1 != None:
            space1 = "    "
            space2 = space2 + " "
        if width2 != None:
            space2 = space2 + "  "
            space3 = space3 + " "
        if width3 != None:
            space3 = space3 + "  "


        print(space1, width1, space2, width2, space3, width3, "\n")

    print("**  a  **  b  **  c  **")


#defining actions

#Preconditions: the destination must have a disk with a larger width
#Effect: the disk will be moved to the destination peg
def move(startPeg, destPeg):
    moveDisk = startPeg.pop()
    destPeg.add(moveDisk)


#Prints the position of all of the disks
#Position is a tuple, 1st element is the peg, 2nd element is the height on that peg (0-indexed)
def getState():
    position = [None] * numDisks
    for i in range(numDisks):
        position[i] = disks[i].getDiskPos()
    return tuple(position)

#replicates the state based on the given position
def replicateState(pos):
    #the first element is pos for Disk1: pegNum; second element is height (0 = bottom, 2 = top three disks)
    #peg nums numbered normally
    for p in pegs:
        p.pegList = [None] * numDisks

    for i, diskPos in enumerate(pos):
        if diskPos[0] == 1:
            peg1.set(disks[i], diskPos[1])
        elif diskPos[0] == 2:
            peg2.set(disks[i], diskPos[1])
        elif diskPos[0] == 3:
            peg3.set(disks[i], diskPos[1])


numDisks = 5
disks = []
startGame(numDisks)

pegs = [peg1, peg2, peg3]
#1.) creating the queue and the visited
# queue stores the relevant states
# based on all of the possible states
visited = []
queue = []
startState = getState()

# startState = ((1, 0), (2, 0), (3, 0)) #this is for error checking
# replicateState(startState)
# goalState = ((3, 3), (3, 2), (3, 1), (3, 0))
#disk one is the first position, disk two is the second position and three is the third

#2.) append the first state/source node
pos = getState()
queue.append(pos)
# printGame()
# print(getState())

visited.append(pos) #anything in visited has been visited; using index() to check if the element has been visited

parentsToChildren = dict()
goalReached = False
#problem: you need a way to track your position and go back.
while queue and not goalReached: #while the queue is not empty
    previousPos = queue.pop(0) #start with the first element that was appended
    
    replicateState(previousPos)
    # print("This is the state of the game at the moment: ", getState())

    children = [] # children states that branch off of the parent/previous state or previous position


    #you need to replicate the state of previousPos bc you are checking for neighboring states from this position
    #after you find a possible move, replicate the previousPos again
    #step 3: get the next possible moves from the previous position
    for p in pegs:
        d = p.getTopDisk()
        #check all of the possible pegs that this disk can be moved to
        for i in range(len(pegs)):
            if d != None and pegs[i].pegNum != d.pegNum: #if the peg being checked isn't the one it's already on


                # if the destPeg has a topDisk with a larger width AND the peg isn't full
                # cond.1: if there is no disk
                # cond.2: if there is a top disk at the peg and it's width is greater than the width of the moving disk
                # you do not have to check if the peg is full because it never can be full unless you have every
                # disk on that peg
                if pegs[i].getTopDisk() == None or pegs[i].getTopDisk() != None and pegs[i].getTopDisk().width > d.width:
                        # pegs[i].getTopDisk().height != numDisks - 1:
                    move(p, pegs[i]) #you want to be able to move back to a specified state.
                    curPos = getState()
                    # print("Position: ", curPos, "Disk movement: ", p.pegNum, ", ", pegs[i].pegNum)
                    try:
                        if visited.index(curPos) >= 0: #meaning that this position was visited
                            # print("visited")
                            children.append(tuple(curPos))
                    except:
                        # print("not visited")
                        visited.append(curPos)
                        queue.append(curPos)
                        if curPos == goalState:
                            goalReached = True
                            break
                        #you are essentially finding the child to the previousPos
                        children.append(tuple(curPos))

                    #after you have found a possible move, make sure to reset the state
                    replicateState(previousPos)
                    # printGame()
                    # print("This is the state of the game at the moment: ", getState())
        if goalReached == True:
            break
    # print("Children: ", children, "\n")
    # after finding all of the children of a previous position, add them to the dictionary
    # only immutable datatypes are hashable, so you have to hash a tuple instead of a list
    parentsToChildren[previousPos] = tuple(children)
    # print(queue)
print("Finished checking all")
# # Search for the solution path
path = [goalState]
pos = goalState
while pos != startState:
    # step 1: get the parent of the current pos
    # dict.keys() returns an array of the keys
    # dict.values() returns an array of the values
    idx = -1
    # in the values, look for the set of children containing the position held in pos
    # the values held in the dictionary are sets of children of a parent (key)
    for i, childrenPositions in enumerate(parentsToChildren.values()):
        # run through each child contained in childrenPositions
        for child in childrenPositions:
            # if the position is found in this set of children in childrenPositions,
            # then that means you need to get the parent of this set of children
            if child == pos:
                # the index for parent in the list of keys/parents
                idx = list(parentsToChildren.values()).index(childrenPositions)
                break
        if idx != -1:
            break
    # step 2: add the parent to the path
    parent = list(parentsToChildren.keys())[idx]
    print(parent)
    path.append(parent)

    # step 3: trace back to the position of the parent you found
    # the next iteration will look for the parent of the parent you just found
    pos = parent
path.reverse()
for p in path:
    replicateState(p)
    printGame()
    print(p, "\n")# This is a sample Python script.