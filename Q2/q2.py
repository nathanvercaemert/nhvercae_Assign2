import sys
from collections import deque
from graph import Graph
import heapq

# don't forget to comment code and make a readme

# coping with unreachable keys
largeNumber = 1000000


# heuristic for A*
def distance(u, v):
    # euclidean distance 
    # xSquared = (int(u[0]) - int(v[0])) ** 2
    # ySquared = (int(u[1]) - int(v[1])) ** 2
    # return math.sqrt(xSquared + ySquared)
    
    # use Manhattan distance
    xDiff = abs(u[0] - v[0])
    yDiff = abs(u[1] - v[1])
    return xDiff + yDiff


def harryAstar(currentLocation, nextLocation, isNavigable, isVisited, pathsExplored):
    for i in range(len(isVisited)):
        for j in range (len(isVisited[i])):
            isVisited[i][j] = False
    possibleCurrentLocation = currentLocation
    possibleCurrentRow = possibleCurrentLocation[0]
    possibleCurrentColumn = possibleCurrentLocation[1]
    possiblePath = []
    mazeShape = (len(isNavigable), len(isNavigable[0]))
    numRows = mazeShape[0]
    numCols = mazeShape[1]
    fringe = []
    isFailed = False
    while not possibleCurrentLocation == nextLocation:
        if isFailed:
            return (largeNumber, ('None', [nextLocation]))
        if not isVisited[possibleCurrentRow][possibleCurrentColumn]:
            isVisited[possibleCurrentRow][possibleCurrentColumn] = True
            leftCol = possibleCurrentColumn
            if leftCol > 0:
                leftCol -= 1
                if not isNavigable[possibleCurrentRow][leftCol]:
                    leftCol = possibleCurrentColumn
            left = (possibleCurrentRow, leftCol)
            leftPath = possiblePath.copy()
            leftPath.append(left)
            possibleAStar = len(leftPath) + distance(left, nextLocation)
            heapq.heappush(fringe, (possibleAStar, ('L', (left, leftPath))))
            rightCol = possibleCurrentColumn
            if rightCol < (numCols - 1):
                rightCol += 1
                if not isNavigable[possibleCurrentRow][rightCol]:
                    rightCol = possibleCurrentColumn
            right = (possibleCurrentRow, rightCol)
            rightPath = possiblePath.copy()
            rightPath.append(right)
            possibleAStar = len(rightPath) + distance(right, nextLocation)
            heapq.heappush(fringe, (possibleAStar, ('R', (right, rightPath))))
            upRow = possibleCurrentRow
            if upRow > 0:
                upRow -= 1
                if not isNavigable[upRow][possibleCurrentColumn]:
                    upRow = possibleCurrentRow
            up = (upRow, possibleCurrentColumn)
            upPath = possiblePath.copy()
            upPath.append(up)
            possibleAStar = len(upPath) + distance(up, nextLocation)
            heapq.heappush(fringe, (possibleAStar, ('U', (up, upPath))))
            downRow = possibleCurrentRow
            if downRow < (numRows - 1):
                downRow += 1
                if not isNavigable[downRow][possibleCurrentColumn]:
                    downRow = possibleCurrentRow
            down = (downRow, possibleCurrentColumn)
            downPath = possiblePath.copy()
            downPath.append(down)
            possibleAStar = len(downPath) + distance(down, nextLocation)
            heapq.heappush(fringe, (possibleAStar, ('D', (down, downPath))))
        if fringe:
            fromFringe = []
            fromFringe.append(heapq.heappop(fringe))
            selectedFromFringe = ()
            if fringe:
                while fringe and fringe[0][0] == fromFringe[0][0]:
                    fromFringe.append(heapq.heappop(fringe))
                for movement in fromFringe:
                    # select from fringe based on direction preference if f-values are the same
                    if movement[1][0] == 'U':
                        selectedFromFringe = movement
                    if movement[1][0] == 'L':
                        selectedFromFringe = movement
                    if movement[1][0] == 'D':
                        selectedFromFringe = movement
                    if movement[1][0] == 'R':
                        selectedFromFringe = movement
            else:
                selectedFromFringe = fromFringe[0]
            fromFringe.remove(selectedFromFringe)
            while fromFringe:
                # if there were other equal f-values, add them back to the fringe
                heapq.heappush(fringe, fromFringe.pop())
            possibleCurrentLocation = selectedFromFringe[1][1][0]
            possibleCurrentRow = possibleCurrentLocation[0]
            possibleCurrentColumn = possibleCurrentLocation[1]
            possiblePath = selectedFromFringe[1][1][1]
        else:
            isFailed = True

    # determine direction of first movement for prioritizing directions of equal A* searches
    firstMovement = (0, 0)
    if possiblePath:
        firstMovement = (possiblePath[0][0] - currentLocation[0], possiblePath[0][1] - currentLocation[1])
    firstDirection = 'None'
    if firstMovement == (1, 0):
        firstDirection = 'D'
    if firstMovement == (0, 1):
        firstDirection = 'R'
    if firstMovement == (-1, 0):
        firstDirection = 'U'
    if firstMovement == (0, -1):
        firstDirection = 'L'
    
    return (len(possiblePath), (firstDirection, possiblePath))


def extract_table(f):
    table = []
    for line in f:
        if line[0] == '\n':
            break
        fields = line.split(',')
        for i, word in enumerate(fields):
            fields[i] = word.strip()
        table.append(fields)
    return table


def go_left(isNavigable, location):
    currentRow = location[0]
    newColumn = location[1]
    while (isNavigable[currentRow][newColumn - 1]):
        newColumn -= 1
    return (currentRow, newColumn)


def go_right(isNavigable, location):
    currentRow = location[0]
    newColumn = location[1]
    while (isNavigable[currentRow][newColumn + 1]):
        newColumn += 1
    return (currentRow, newColumn)


def go_up(isNavigable, location):
    newRow = location[0]
    currentColumn = location[1]
    while (isNavigable[newRow - 1][currentColumn]):
        newRow -= 1
    return (newRow, currentColumn)


def go_down(isNavigable, location):
    newRow = location[0]
    currentColumn = location[1]
    while (isNavigable[newRow + 1][currentColumn]):
        newRow += 1
    return (newRow, currentColumn)

def createMatrix(rowCount, colCount, initialize):
    mat = []
    for i in range(rowCount):
        rowList = []
        for j in range(colCount):
            rowList.append(initialize)
        mat.append(rowList)
    return mat


# main
fileName = sys.argv[1]
with open(fileName, 'r') as f:
    maze = extract_table(f)
mazeWidth = len(maze[0])
mazeHeight = len(maze)
isVisited = createMatrix(mazeHeight, mazeWidth, False)
isNavigable = createMatrix(mazeHeight, mazeWidth, False)
isDoor = createMatrix(mazeHeight, mazeWidth, False)
doorLocation = ()
isKey = createMatrix(mazeHeight, mazeWidth, False)
keyLocations = []
numKeys = 0
keyLocations = set()
currentLocation = ()
currentColumn = 0
currentRow = 0
currentPath = []
pathsExplored = 0
for i, row in enumerate(maze):
    for j, col in enumerate(row):
        if col == '0' or col == 'H' or col == 'T' or col == 'D' or col == 'K':
            isNavigable[i][j] = True
        if col == 'T' or col == 'D':
            isDoor[i][j] = True
            doorLocation = (i, j)
        if col == 'K':
            isKey[i][j] = True
            numKeys += 1
            keyLocations.add((i, j))
        if col == 'H':
            currentLocation = (i, j)
            currentColumn = j
            currentRow = i
            currentPath.append(currentLocation)

output = ''
            
search = sys.argv[2]
if search == 'dfs':
    fileName = fileName.split('/')
    fileName = fileName[-1][:-4]
    fileName = './Solutions/DFS/' + fileName + '_solution.txt'
    isFailed = False
    stack = deque()
    while True:
        if isFailed:
            output = 'Not possible'
            break
        pathsExplored += 1
        if isDoor[currentRow][currentColumn]:
            for tuple in currentPath:
                output += '(' + str(tuple[0]) + ', ' + str(tuple[1]) + '),'
            output = output[:-1]
            print(pathsExplored)
            break
        if not isVisited[currentRow][currentColumn]:
            isVisited[currentRow][currentColumn] = True
            down = go_down(isNavigable, currentLocation)
            downPath = currentPath.copy()
            downPath.append(down)
            stack.append((down, downPath))
            up = go_up(isNavigable, currentLocation)
            upPath = currentPath.copy()
            upPath.append(up)
            stack.append((up, upPath))
            right = go_right(isNavigable, currentLocation)
            rightPath = currentPath.copy()
            rightPath.append(right)
            stack.append((right, rightPath))
            left = go_left(isNavigable, currentLocation)
            leftPath = currentPath.copy()
            leftPath.append(left)
            stack.append((left, leftPath))
        if stack:
            currentTest = stack.pop()
            currentLocation = currentTest[0]
            currentPath = currentTest[1]
            currentRow = currentLocation[0]
            currentColumn = currentLocation[1]
        else:
            isFailed = True
if search == 'bfs':
    fileName = fileName.split('/')
    fileName = fileName[-1][:-4]
    fileName = './Solutions/BFS/' + fileName + '_solution.txt'
    isFailed = False
    queue = deque()
    while True:
        if isFailed:
            output = 'Not possible'
            break
        pathsExplored += 1
        if isDoor[currentRow][currentColumn]:
            for tuple in currentPath:
                output += '(' + str(tuple[0]) + ', ' + str(tuple[1]) + '),'
            output = output[:-1]
            print(pathsExplored)
            break
        if not isVisited[currentRow][currentColumn]:
            isVisited[currentRow][currentColumn] = True
            left = go_left(isNavigable, currentLocation)
            leftPath = currentPath.copy()
            leftPath.append(left)
            queue.append((left, leftPath))
            right = go_right(isNavigable, currentLocation)
            rightPath = currentPath.copy()
            rightPath.append(right)
            queue.append((right, rightPath))
            up = go_up(isNavigable, currentLocation)
            upPath = currentPath.copy()
            upPath.append(up)
            queue.append((up, upPath))
            down = go_down(isNavigable, currentLocation)
            downPath = currentPath.copy()
            downPath.append(down)
            queue.append((down, downPath))
        if queue:
            currentTest = queue.popleft()
            currentLocation = currentTest[0]
            currentPath = currentTest[1]
            currentRow = currentLocation[0]
            currentColumn = currentLocation[1]
        else:
            isFailed = True
if search == 'astar':
    fileName = fileName.split('/')
    fileName = fileName[-1][:-4]
    fileName = './Solutions/ASTAR/' + fileName + '_solution.txt'
    gStart = Graph()
    for key in keyLocations:
        gStart.add_vertex(key)
    gStart.add_vertex(doorLocation)
    gStart.add_vertex(currentLocation)
    distances = {}
    for u in gStart.vertices():
        for v in gStart.vertices():
            astarUV = harryAstar(u, v, isNavigable, isVisited, pathsExplored)            
            astarVU = harryAstar(v, u, isNavigable, isVisited, pathsExplored)            
            distances[(u, v)] = astarUV
            distances[(v, u)] = astarVU
    remainingKeyLocations = keyLocations.copy()
    steps = 0
    path = []
    keyOrder = []
    while remainingKeyLocations:
        nextKey = ()
        nextKeyLocation = ()
        nextKeySteps = 0
        nextKeyPath = ()
        nextKeyLocationHeap = []
        for key in remainingKeyLocations:
            heapq.heappush(nextKeyLocationHeap, distances[currentLocation, key])

        # if there are multiple closest keys, choose based on direction preference
        nextClosestKeys = [heapq.heappop(nextKeyLocationHeap)]

        # coping with unreachable key
        tempNextClosestKey = nextClosestKeys[0]
        if tempNextClosestKey[0] == largeNumber:
            steps = -1
            # print(remainingKeyLocations)
            # print(tempNextClosestKey)
            remainingKeyLocations.remove(tempNextClosestKey[1][1][-1])
            continue
        
        nextKeyLocation = ()
        while nextKeyLocationHeap and nextKeyLocationHeap[0][0] == nextClosestKeys[0][0]:
            nextClosestKeys.append(heapq.heappop(nextKeyLocationHeap))
        for key in nextClosestKeys:
            if key[1][0] == 'U':
                nextKeyLocation = key
            if key[1][0] == 'L':
                nextKeyLocation = key
            if key[1][0] == 'D':
                nextKeyLocation = key
            if key[1][0] == 'R':
                nextKeyLocation = key

        nextKeySteps = nextKeyLocation[0]
        nextKeyPath = nextKeyLocation[1][1]
        nextKeyLocation = nextKeyLocation[1][1][-1]
        remainingKeyLocations.remove(nextKeyLocation)
        currentLocation = nextKeyLocation
        steps += nextKeySteps
        path.append(nextKeyPath)
        keyOrder.append(nextKeyLocation)

    astarToDoor = distances[currentLocation, doorLocation]

    finalClosestKeyPath = []
    if not steps == -1:
        steps += astarToDoor[0]
        path.append(astarToDoor[1][1])
        finalClosestKeyPath.append((0, 0))
        for subPath in path:
            for loc in subPath:
                finalClosestKeyPath.append(loc)
    else:
        finalClosestKeyPath = "Not possible"
   
    # print(keyOrder)
    for tuple in keyOrder:
        output += '(' + str(tuple[0]) + ', ' + str(tuple[1]) + '),'
    if not output == '':
        output = output[:-1]
    # print(steps)         
    output += '\n'
    output += (str(steps) + '\n')
    # print(finalClosestKeyPath)
    if not finalClosestKeyPath == 'Not possible':
        for tuple in finalClosestKeyPath:
            output += '(' + str(tuple[0]) + ', ' + str(tuple[1]) + '),'
        output = output[:-1]
    else:
        output += finalClosestKeyPath
    # print(output)

# output
f = open(fileName, "w")
f.write(output)
f.close()
