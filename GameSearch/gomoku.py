import sys
import copy
import string

globalcounter = 0
# def printLogLine(y,x,value)
class node(object):
    def __init__(self):
        self.name=None
        self.node=[]
        self.level = 0
        self.rowIndex = 0
        self.prev=None
        self.value = None
        self.alpha = -1000000
        self.beta= 1000000
        self.visited = False
        self.sum = 0
        self.x =0
        self.y =0

    def add(self):
        # Make a new node called Temp
        childNode=node()
        # append the new node to the parent
        self.node.append(childNode)
        # Set its pointer to parent
        childNode.prev=self

        return childNode


def printLog(node):
    res = node.name
    res += ","
    res += str(node.level)
    res += ","
    res += str(node.alpha)
    # print res

def cordinateToLetter(x,y,N):
    res = list(string.ascii_uppercase)[x]
    res += str(N - y)
    return res

def traverseLog(cordinate,N,depth,value,visited,cutOff,playingAsMax,logFileHandler):
    res = cordinate
    res += ","
    res += str(depth)
    res += ","

    # if(depth != cutOff and visited == False):
    #     res += "Infinity" if playingAsMax else "-Infinity"
    # else:
    if(value == 1000000):
        res += "Infinity"
    elif(value == -1000000):
        res += "-Infinity"
    else:
        res += str(value)


    res += "\n"

    logFileHandler.write(res)

def traverseLogAB(cordinate, N, depth, value,alpha,beta, cutOff, logFileHandler):
    res = cordinate
    res += ","
    res += str(depth)
    res += ","

    # if(depth != cutOff and visited == False):
    #     res += "Infinity" if playingAsMax else "-Infinity"
    # else:
    if (value == 1000000):
        res += "Infinity"
    elif (value == -1000000):
        res += "-Infinity"
    else:
        res += str(value)
    res += ","

    if (alpha == 1000000):
        res += "Infinity"
    elif (alpha == -1000000):
        res += "-Infinity"
    else:
        res += str(alpha)
    res += ","

    if (beta == 1000000):
        res += "Infinity"
    elif (beta == -1000000):
        res += "-Infinity"
    else:
        res += str(beta)


    # print res
    res += "\n"


    logFileHandler.write(res)

tempNode = 0
depth = 0

def MinMaxTraversalAlphaBeta(gameboard,player,opponent,parentNode,maxPlayer,cutOff,logFileHandler):

    if(parentNode.level < cutOff):
        N = len(gameboard[0])
        freeList = findNeighbors(gameboard)
        sortedNeighbors = sorted(freeList, key=lambda k: (k['x'], -k['y']))

        winCheck = False
        prune = False

        for child in sortedNeighbors:

            childNode = parentNode.add()
            childNode.x = child['x']
            childNode.y = child['y']
            childNode.name = cordinateToLetter(childNode.x, childNode.y, N)
            childNode.level = parentNode.level + 1


            gameboard[childNode.y][childNode.x] = player
            childNode.alpha = parentNode.alpha
            childNode.beta = parentNode.beta

            if (childNode.level == cutOff):
                childNode.value, isWin = calculateHeuristic(gameboard, childNode.y, childNode.x, player, opponent)
                if not maxPlayer:
                    childNode.value = -childNode.value
                childNode.value += parentNode.sum

                if (isWin):
                    winCheck = True

            else:
                childNode.value, isWin = calculateHeuristic(gameboard, childNode.y, childNode.x, player, opponent)
                if not maxPlayer:
                    childNode.value = -childNode.value
                childNode.sum = childNode.value + parentNode.sum

                if maxPlayer:
                    childNode.value = 1000000
                else:
                    childNode.value = -1000000

                if isWin:
                    childNode.value = childNode.sum
                    winCheck = True

            traverseLogAB(childNode.name, N, childNode.level, childNode.value,childNode.alpha,childNode.beta, cutOff, logFileHandler)


            if not winCheck:

                MinMaxTraversalAlphaBeta(gameboard, opponent, player, childNode, not maxPlayer, cutOff,logFileHandler)

            gameboard[childNode.y][childNode.x] = '.'



            if (maxPlayer):
                if childNode.value > parentNode.value:
                    parentNode.value = childNode.value

                if childNode.value >= parentNode.alpha:
                    if childNode.value >= parentNode.beta:
                        prune = True
                    else:
                        parentNode.alpha = childNode.value
                        childNode.alpha = childNode.value


            else:
                if childNode.value < parentNode.value:
                    parentNode.value = childNode.value

                if childNode.value <= parentNode.beta:
                    if childNode.value <= parentNode.alpha:
                        prune = True
                    else:
                        parentNode.beta = childNode.value
                        childNode.beta = childNode.value


            traverseLogAB(parentNode.name, N, parentNode.level, parentNode.value,parentNode.alpha,parentNode.beta, cutOff, logFileHandler)

            if parentNode.beta <= parentNode.alpha or prune:
                break

            if winCheck:
                winCheck = False



def getMinMaxAlphaBeta(gameboard,player,opponent,depth,cutOff):
    rootNode = node()
    rootNode.name = 'root'
    rootNode.level = 0
    rootNode.rowIndex = 0
    rootNode.value = -1000000
    rootNode.alpha = -1000000
    rootNode.beta = 1000000
    rootNode.sum = 0

    gameboardTemp = copy.deepcopy(gameboard)

    logFileHandler = open("traverse_log.txt", "w")
    logFileHandler.write("Move,Depth,Value,Alpha,Beta\n")
    logFileHandler.write("root,0,-Infinity,-Infinity,Infinity\n")

    MinMaxTraversalAlphaBeta(gameboard,player,opponent,rootNode,True,cutOff,logFileHandler)
    logFileHandler.close()



    bestmove = None

    for moves in rootNode.node:
        if (moves.value == rootNode.value):
            bestmove = (moves.x,moves.y)
            break

    return makeNextBoard(gameboardTemp,bestmove[1],bestmove[0],player)

def MinMaxTraversal(gameboard,player,opponent,Depth,parentNode,maxPlayer,cutOff,logFileHandler):
    if(Depth != 0):

        N = len(gameboard[0])
        freeList = findNeighbors(gameboard)
        sortedNeighbors = sorted(freeList, key=lambda k: (k['x'], -k['y']))

        winCheck = False

        for child in sortedNeighbors:
            childNode = parentNode.add()
            childNode.x = child['x']
            childNode.y = child['y']
            childNode.name = cordinateToLetter(childNode.x,childNode.y,N)
            childNode.level = parentNode.level + 1
            gameboard[childNode.y][childNode.x] = player

            if (childNode.level == cutOff):
                childNode.value,isWin = calculateHeuristic(gameboard, childNode.y, childNode.x, player, opponent)
                if not maxPlayer:
                    childNode.value = -childNode.value
                childNode.value += parentNode.sum

                if (isWin):
                    winCheck = True
            else:
                childNode.value, isWin = calculateHeuristic(gameboard, childNode.y, childNode.x, player, opponent)
                if not maxPlayer:
                    childNode.value = -childNode.value
                childNode.sum = childNode.value + parentNode.sum

                if maxPlayer:
                    childNode.value = 1000000
                else:
                    childNode.value = -1000000

                if isWin:
                    childNode.value = childNode.sum
                    winCheck = True

            traverseLog(childNode.name,N,childNode.level,childNode.value,True,cutOff,maxPlayer,logFileHandler)

            if not winCheck:
                MinMaxTraversal(gameboard,opponent,player,Depth-1,childNode,not maxPlayer,cutOff,logFileHandler)
            gameboard[childNode.y][childNode.x] = '.'


            if (maxPlayer):
                if childNode.value > parentNode.value:
                    parentNode.value = childNode.value
            else:
                if childNode.value < parentNode.value:
                    parentNode.value = childNode.value

            traverseLog(parentNode.name, N, parentNode.level, parentNode.value, True, cutOff, maxPlayer,logFileHandler)

            if winCheck:
                winCheck = False

def getMinMax(gameboard,player,opponent,depth,cutOff):
    rootNode = node()
    rootNode.name = 'root'
    rootNode.level = 0
    rootNode.rowIndex = 0
    rootNode.value = -1000000
    rootNode.sum = 0



    logFileHandler = open("traverse_log.txt", "w")
    logFileHandler.write("Move,Depth,Value\n")
    logFileHandler.write("root,0,-Infinity\n")

    MinMaxTraversal(gameboard,player,opponent,depth,rootNode,True,cutOff,logFileHandler)
    logFileHandler.close()


    # print rootNode.value
    bestmove = None

    for moves in rootNode.node:
        if (moves.value == rootNode.value):
            bestmove = (moves.x,moves.y)
            break

    return makeNextBoard(gameboard,bestmove[1],bestmove[0],player)

def getGreedyBoard(gameboard,player,opponent):
    freeList = findNeighbors(gameboard)
    heuristicsList = makeHeuristicBoard(gameboard,freeList,player,opponent)
    # print heuristicsList
    # print "\n----------------------\n"
    # print sorted(heuristicsList, key=lambda k: (k['hValue'], N - k['x'], k['y']), reverse=True)
    # print "\n----------------------\n"
    nextMove = sorted(heuristicsList, key=lambda k: (k['hValue'], N - k['x'], k['y']), reverse=True)[0]
    for i in range(N):
        for j in range(N):
            if (gameboard[i][j] == '*'):
                gameboard[i][j] = '.'

    gameboard[nextMove['y']][nextMove['x']] = player
    writeGameBoard(gameboard)
    # printGameBoard(gameboard)

def printGameBoard(gameboard):
    # print a given game board
    N = len(gameboard[0])
    for i in range(N):
        for j in range(N):
            print gameboard[i][j],
        print '\t'

def writeGameBoard(gameboard):

    fileResult = ""
    resultOutput = open("next_state.txt", "w")

    N = len(gameboard[0])
    for i in range(N):
        fileResult=""
        for j in range(N):
            fileResult += gameboard[i][j]
        fileResult += "\n"
        resultOutput.write(fileResult)

def writefileMiniMax(result):
    output = open("traverse_log.txt", "w")
    output.write(result)

def writefileState(self, result):
    output = open("trace_state.txt", "w")
    output.write(result)

def makeNextBoard(gameboard,y,x,value):
    #place a value on a location and print the gameboard
    gameboard[y][x] = value
    return gameboard

def checkLocation(gameboard,y,x,value):
    #place a value on a location and print the gameboard
    gameboard[y][x] = value

    printGameBoard(gameboard)


# Functions to check 8 directions
def checkNorth(gameboard,y,x,player,opponent,count):
    isOpen = False
    # Check board boundary condition
    if(y-1 > -1):
        # Check count of players stones in row
        if(gameboard[y-1][x] == player and count > -1):
            count,isOpen = checkNorth(gameboard,y-1,x,player,opponent,count+1)
        # Check count of opponents stones to block in row
        elif(gameboard[y-1][x] == opponent and count < 1):
            count, isOpen = checkNorth(gameboard, y-1, x, player, opponent, count-1)
        elif(gameboard[y-1][x] == '*' or gameboard[y-1][x] == '.'):
            isOpen = True
    return count,isOpen

def checkSouth(gameboard,y,x,player,opponent,count):
    isOpen = False
    if(y+1 < len(gameboard[0])):
        if(gameboard[y+1][x] == player and count >-1):
            count,isOpen = checkSouth(gameboard,y+1,x,player,opponent,count+1)
        elif(gameboard[y+1][x] == opponent and count < 1):
            count,isOpen = checkSouth(gameboard,y+1,x,player,opponent,count-1)
        elif(gameboard[y+1][x] == '*' or gameboard[y+1][x] == '.'):
                isOpen = True
    return count,isOpen
def checkEast(gameboard,y,x,player,opponent,count):
    isOpen = False
    if(x+1 < len(gameboard[0])):
        if(gameboard[y][x+1] == player and count >-1):
            count,isOpen  = checkEast(gameboard,y,x+1,player,opponent,count+1)
        elif (gameboard[y][x+1] == opponent and count < 1):
            count, isOpen = checkEast(gameboard, y,x+1, player, opponent, count-1)
        elif (gameboard[y][x+1] == '*' or gameboard[y][x+1] == '.'):
            isOpen = True
    return count, isOpen
def checkWest(gameboard,y,x,player,opponent,count):
    isOpen = False
    if(x-1 > -1):
        if(gameboard[y][x-1] == player and count >-1):
            count,isOpen = checkWest(gameboard,y,x-1,player,opponent,count+1)
        elif (gameboard[y][x-1] == opponent and count < 1):
            count, isOpen = checkWest(gameboard, y, x-1, player, opponent, count - 1)
        elif (gameboard[y][x-1] == '*' or gameboard[y][x-1] == '.'):
            isOpen = True
    return count, isOpen
def checkNorthEast(gameboard,y,x,player,opponent,count):
    isOpen = False
    # Check board boundary condition
    if(y-1 > -1 and x+1 <len(gameboard[0])):
        # Check count of players stones in row
        if(gameboard[y-1][x+1] == player and count > -1):
            count,isOpen = checkNorthEast(gameboard,y-1,x+1,player,opponent,count+1)
        # Check count of opponents stones to block in row
        elif(gameboard[y-1][x+1] == opponent and count < 1):
            count, isOpen = checkNorthEast(gameboard, y-1, x+1, player, opponent, count-1)
        elif(gameboard[y-1][x+1] == '*' or gameboard[y-1][x+1] == '.'):
            isOpen = True
    return count,isOpen
def checkNorthWest(gameboard,y,x,player,opponent,count):
    isOpen = False
    # Check board boundary condition
    if(y-1 > -1 and x-1 > -1):
        # Check count of players stones in row
        if(gameboard[y-1][x-1] == player and count > -1):
            count,isOpen = checkNorthWest(gameboard,y-1,x-1,player,opponent,count+1)
        # Check count of opponents stones to block in row
        elif(gameboard[y-1][x-1] == opponent and count < 1):
            count, isOpen = checkNorthWest(gameboard, y-1, x-1, player, opponent, count-1)
        elif(gameboard[y-1][x-1] == '*' or gameboard[y-1][x-1] == '.'):
            isOpen = True
    return count,isOpen
def checkSouthWest(gameboard,y,x,player,opponent,count):
    isOpen = False
    if(y+1 < len(gameboard[0]) and x-1 > -1):
        if(gameboard[y+1][x-1] == player and count >-1):
            count,isOpen = checkSouthWest(gameboard,y+1,x-1,player,opponent,count+1)
        elif(gameboard[y+1][x-1] == opponent and count < 1):
            count,isOpen = checkSouthWest(gameboard,y+1,x-1,player,opponent,count-1)
        elif(gameboard[y+1][x-1] == '*' or gameboard[y+1][x-1] == '.'):
                isOpen = True
    return count,isOpen
def checkSouthEast(gameboard,y,x,player,opponent,count):
    isOpen = False
    if(y+1 < len(gameboard[0]) and x+1 <len(gameboard[0])):
        if(gameboard[y+1][x+1] == player and count >-1):
            count,isOpen = checkSouthEast(gameboard,y+1,x+1,player,opponent,count+1)
        elif(gameboard[y+1][x+1] == opponent and count < 1):
            count,isOpen = checkSouthEast(gameboard,y+1,x+1,player,opponent,count-1)
        elif(gameboard[y+1][x+1] == '*' or gameboard[y+1][x+1] == '.'):
                isOpen = True
    return count,isOpen


def getHeuristicValue(Create,Open,Number):
    # create -> true block -> false
    # open -> true close-> false
    # number 2,3,4,5

    # Cheack if the number is negative indicating not my stone
    # Set it to positive and check the count
    # Else increase the count + 1 to account for the stone being placed and
    # check the count of my stones in a row
    # if the number is 0 indicating open then number + 1 will be = 1
    # We dont need to handle this case and return 0


    Number = -Number if (Number < 0) else Number + 1




    if (Number == 2):
        # CreateOpenTwo
        if (Create == True and Open == True):
            return 5,False
        # CreateCloseTwo
        elif (Create == True and Open == False):
            return 1,False
        else:
            return 0,False


    elif(Number == 3):
        # BlockOpenThree
        if (Create == False and Open == True):
            return 500,False
        # BlockClosedThree
        elif (Create == False and Open == False):
            return 100,False
        # CreateOpenThree
        elif (Create == True and Open == True):
            return 50,False
        # CreateClosedThree
        elif(Create == True and Open == False):
            return 10,False
        else:
            return 0,False

    elif (Number == 4):
        # BlockClosedFour
        if (Create == False and Open == False):
            return 10000,False
        # CreateOpenFour
        elif (Create == True and Open == True):
            return 5000,False
        # CreateClosedFour
        elif (Create == True and Open == False):
            return 1000,False
        else:
            return 0,False

    elif (Number >= 5):
        return 50000,True

    # When Number = 0 or 1
    else:
        return 0,False

def getHeuristicWinValue(Number):
    # Special case when 5 stones are sandwiched
    # If Less than 5 are sandwiched ignore completely
    if(Number == 5):
        return 50000,True
    else:
        return 0,False

def calculateHeuristic(gameboard,y,x,player,opponent):
    northCount,isNorthOpen = checkNorth(gameboard,y,x,player,opponent,0)
    southCount,isSouthOpen = checkSouth(gameboard,y,x,player,opponent,0)

    eastCount,isEastOpen= checkEast(gameboard,y,x,player,opponent,0)
    westCount,isWestOpen = checkWest(gameboard,y,x,player,opponent,0)

    northEastCount,isNorthEastOpen = checkNorthEast(gameboard,y,x,player,opponent,0)
    southWestCount,isSouthWestOpen = checkSouthWest(gameboard,y,x,player,opponent,0)

    southEastCount,isSouthEastOpen= checkSouthEast(gameboard,y,x,player,opponent,0)
    northWestCount,isNorthWestOpen= checkNorthWest(gameboard,y,x,player,opponent,0)

    vertical,hasWinV = getHeuristicTotal(northCount,isNorthOpen,southCount,isSouthOpen)
    horizontal,hasWinH = getHeuristicTotal(eastCount,isEastOpen,westCount,isWestOpen)
    diagonol1,hasWinD1 = getHeuristicTotal(northEastCount,isNorthEastOpen,southWestCount,isSouthWestOpen)
    diagonol2,hasWinD2 = getHeuristicTotal(southEastCount,isSouthEastOpen,northWestCount,isNorthWestOpen)

    sum = vertical + horizontal + diagonol1 + diagonol2
    win = hasWinV or hasWinH or hasWinD1 or hasWinD2
    return sum,win

def makeHeuristicBoard(gameboard,freeList,player,opponent):

    for cordinate in freeList:
        x=cordinate['x']
        y=cordinate['y']
        hValue,isWin=calculateHeuristic(gameCharLines,y,x,player,opponent)
        cordinate['hValue'] = hValue

    return freeList

def getHeuristicTotal(countA, isOpenA, countB, isOpenB):
    # Identify which all cases are applicable for the given configuration

    # Assign a value to increment the max player's heuristic value
    maxPlayerValue = 0
    hasWin = False
    # number += 1
    if (not isOpenA and not isOpenB):

        if (countA > 0 and countB < 0):
            # CreateClosedCountA -> Check Win
            if(abs(countA >= 4)):
                returnVal, returnWin = getHeuristicValue(True,False,countA)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

            # BlockClosedCountB
            returnVal, returnWin = getHeuristicValue(False, False, countB)
            maxPlayerValue += returnVal
            hasWin = hasWin or returnWin

        elif (countA > 0 and countB > 0):
            # CreateClosedCount(A+B) -> Check Win
            if(abs(countA + countB) >= 4):
                returnVal, returnWin = getHeuristicValue(True,False,countA + countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

        elif (countA < 0 and countB < 0):
            # BlockClosedCountA
            returnVal, returnWin = getHeuristicValue(False, False, countA)
            maxPlayerValue += returnVal
            hasWin = hasWin or returnWin
            # BlcokClosedCountB
            returnVal, returnWin = getHeuristicValue(False, False, countB)
            maxPlayerValue += returnVal
            hasWin = hasWin or returnWin
        elif (countA < 0 and countB > 0):
            # BlockClosedCountA
            returnVal, returnWin = getHeuristicValue(False, False, countA)
            maxPlayerValue += returnVal
            hasWin = hasWin or returnWin
            # CreateClosedCountB -> Check Win
            if(abs(countB) >= 4):
                returnVal, returnWin = getHeuristicValue(True,False,countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

    if (not isOpenA and isOpenB):
        if (countA > 0 and countB >= 0):
            if (countB == 0):
                # CreateClosedCountA
                returnVal, returnWin = getHeuristicValue(True, False, countA)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin
            else:
                # CreateClosedCount (A + B)
                returnVal, returnWin = getHeuristicValue(True, False, countA + countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

        elif (countA < 0 and countB <= 0):
            if (countB == 0):
                # BlockClosedCountA
                returnVal, returnWin = getHeuristicValue(False, False, countA)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin
            else:
                # BlockClosedCountA
                returnVal, returnWin = getHeuristicValue(False, False, countA)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

                # BlockOpenCountB
                returnVal, returnWin = getHeuristicValue(False, True, countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

        elif (countA > 0 and countB <= 0):
            if (countB == 0):
                # CreateClosedCountA
                returnVal, returnWin = getHeuristicValue(True, False, countA)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

            else:
                # BlockOpenCountB
                returnVal, returnWin = getHeuristicValue(False, True, countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

                # CreateClosedCountA check win?
                if(abs(countA) >= 4):
                    returnVal, returnWin = getHeuristicValue(True,False,countA)
                    maxPlayerValue += returnVal
                    hasWin = hasWin or returnWin


        elif (countA < 0 and countB >= 0):
            if (countB == 0):
                # BlockClosedCountA
                returnVal, returnWin = getHeuristicValue(False, False, countA)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin
            else:
                # CreateClosedCountB
                returnVal, returnWin = getHeuristicValue(True, False, countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin
                # BlockClosedCountA
                returnVal, returnWin = getHeuristicValue(False, False, countA)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

    if (isOpenA and not isOpenB):
        if (countA >= 0 and countB > 0):
            if (countA == 0):
                # CreateClosedCountB
                returnVal, returnWin = getHeuristicValue(True, False, countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin
            else:
                # createClosedCount (A + B)
                returnVal, returnWin = getHeuristicValue(True, False, countA + countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

        elif (countA >= 0 and countB < 0):
            if (countA == 0):
                # BlockClosedCountB
                returnVal, returnWin = getHeuristicValue(False, False, countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin
            else:
                # BlockClosedCountB
                returnVal, returnWin = getHeuristicValue(False, False, countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin
                # CreateClosedCountA
                returnVal, returnWin = getHeuristicValue(True, False, countA)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

        elif (countA <= 0 and countB > 0):
            if (countA == 0):
                # CreateClosedCountB
                returnVal, returnWin = getHeuristicValue(True, False, countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin
            else:
                # CreateClosedCountB -> win check?
                if(abs(countB) >= 4):
                    returnVal, returnWin = getHeuristicValue(True,False,countB)
                    maxPlayerValue += returnVal
                    hasWin = hasWin or returnWin

                # BlockOpenCountA
                returnVal, returnWin = getHeuristicValue(False, True, countA)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

        elif (countA <= 0 and countB < 0):
            if (countA == 0):
                # blockClosedCountB
                returnVal, returnWin = getHeuristicValue(False, False, countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin
            else:
                # blockClosedCountB
                returnVal, returnWin = getHeuristicValue(False, False, countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

                # BlockOpenCountA
                returnVal, returnWin = getHeuristicValue(False, True, countA)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

    if (isOpenA and isOpenB):
        if (countA >= 0 and countB >= 0):
            # CreateOpenCount(A + B)
            returnVal, returnWin = getHeuristicValue(True, True, countA + countB)
            maxPlayerValue += returnVal
            hasWin = hasWin or returnWin

        elif (countA < 0 and countB >= 0):
            if (countB == 0):
                # BlockOpenCountA
                returnVal, returnWin = getHeuristicValue(False, True, countA)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin
            else:
                # BlockOpenCountA
                returnVal, returnWin = getHeuristicValue(False, True, countA)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

                # CreateClosedCountB
                returnVal, returnWin = getHeuristicValue(True, False, countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

        elif (countA >= 0 and countB < 0):
            if (countA == 0):
                # BlockOpenCountB
                returnVal, returnWin = getHeuristicValue(False, True, countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

            else:
                # BlockOpenCountB
                returnVal, returnWin = getHeuristicValue(False, True, countB)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

                # CreateClosedCountA
                returnVal, returnWin = getHeuristicValue(True, False, countA)
                maxPlayerValue += returnVal
                hasWin = hasWin or returnWin

        elif (countA < 0 and countB < 0):
            # BlockOpenCountA
            returnVal, returnWin = getHeuristicValue(False, True, countA)
            maxPlayerValue += returnVal
            hasWin = hasWin or returnWin

            # BlockOpenCountB
            returnVal, returnWin = getHeuristicValue(False, True, countB)
            maxPlayerValue += returnVal
            hasWin = hasWin or returnWin

        elif (countA < 0 and countB > 0):
            # BlockOpenCountA
            returnVal, returnWin = getHeuristicValue(False, True, countA)
            maxPlayerValue += returnVal
            hasWin = hasWin or returnWin

            # CreateClosedCountB
            returnVal, returnWin = getHeuristicValue(True, False, countB)
            maxPlayerValue += returnVal
            hasWin = hasWin or returnWin

    return maxPlayerValue, hasWin

# Get the connected 8 components got a given cordinate
# Check boundary cases where neighbors of  i,j < 0  and > N(15)
# Do it for all values of i-1 through i+1 and within that for j-1 through j+1
# values i+2 and j+2 are not inclusive in range function
connected8 = lambda i, j: [(x2, y2) for x2 in range(i - 1, i + 2)
                           for y2 in range(j - 1, j + 2)
                           if
                           (0 <= x2 < N and 0 <= y2 < N and (i != x2 or j != y2) and (0 <= x2 < N) and (0 <= y2 < N))]


def findNeighbors(gameboard):
    # printGameBoard(gameboard)
    freeCordinatesList = []

    possibleMoves = 0
    # Get length of gameboard
    N = len(gameboard[0])
    count = 0
    # For each position on board
    for i in range(N):
        for j in range(N):
            if (gameboard[i][j] == '*'):
                gameboard[i][j] = '.'


    for i in range(N):
        for j in range(N):
            # Check if there is a token on the position
            if(gameboard [i][j] == 'b' or gameboard[i][j] == 'w'):
                #find its neighbors
                neighbors = connected8(i, j)
                # for each neighbor
                for k in range(len(neighbors)):
                    x = neighbors[k][0]
                    y = neighbors[k][1]
                    # check if it is a free space and assign X
                    if (gameboard[x][y] == '.'):
                        gameboard[x][y] = '*'
                        possibleMoves += 1

    for i in range(N):
        for j in range(N):
            if (gameboard[i][j] == '*'):
                freeCordinates = {'y': i, 'x': j, 'hValue':0}
                freeCordinatesList.append(freeCordinates)

    # print "Possible moves ",possibleMoves,"\t"
    # printGameBoard(gameboard)
    return freeCordinatesList

# Read the input file as a command line argument
# Store each line in a list -> 'fileLines'

def playMove():

    gameBoardString = "...............,...............,...............,...............,...............,......wb.......,.......bw......,......wwb......,......b........,...............,...............,...............,...............,...............,..............."


    # Separate the commandLines and the game boards lines
    # commandLinesList = fileLines[0:4]
    # gameLinesList = fileLines[4:]
    #
    gameCharLines = []
    # N = len(gameLinesList[0])

    # algo = commandLinesList[0]
    # playerNumber = commandLinesList[1]
    # cutoffdepth = int(commandLinesList[2])
    # boardsize = commandLinesList[3]

    print gameBoardString.split()
    #
    # for line in range(0,len(gameLinesList)):
    #     gameCharLines.append(list(gameLinesList[line]))
    #
    # player=''
    # opponent=''
    #
    #
    #
    # if(playerNumber == '1'):
    #     player = 'b'
    #     opponent = 'w'
    # else:
    #     player = 'w'
    #     opponent ='b'
    #
    # # printGameBoard(gameCharLines)
    #
    #
    # if(algo == '1'):
    #     resultBoard = getGreedyBoard(gameCharLines,player,opponent)
    # elif(algo == '2'):
    #     resultBoard = getMinMax(gameCharLines,player,opponent,cutoffdepth,cutoffdepth)
    #     return resultBoard
    # elif(algo == '3'):
    #     resultBoard = getMinMaxAlphaBeta(gameCharLines,player,opponent,0,cutoffdepth )
    #     return resultBoard




# makeTree(gameCharLines,player,opponent,depth)
# else

playMove()

