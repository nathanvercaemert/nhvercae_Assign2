import sys
import numpy
from collections import deque
from graph import Graph
import math
import heapq
from collections import deque
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_simulated_annealing


def distance(u, v):
    xSquared = (int(u[0]) - int(v[0])) ** 2
    ySquared = (int(u[1]) - int(v[1])) ** 2
    return math.sqrt(xSquared + ySquared)


def minSpanTreeWeight(remainingAfterKeyRemoved, doorLocation, distances):
    includingDoor = remainingAfterKeyRemoved.copy()
    includingDoor.add(doorLocation)
    edges = []
    for u in includingDoor:
        for v in includingDoor:
            heapq.heappush(edges, (distances[(u, v)], (u, v)))
            heapq.heappush(edges, (distances[(v, u)], (v, u)))
    weight = 0
    mst = set()
    while includingDoor:
        nextEdge = heapq.heappop(edges)
        vertices = nextEdge[1]
        u = vertices[0]
        v = vertices[1]
        if (u == v):
            # not really an edge
            continue
        if u not in mst or v not in mst:
            weight += nextEdge[0]
            mst.add(u)
            mst.add(v)
        includingDoor.discard(u)
        includingDoor.discard(v)
    # print(weight)
    return weight


def distToMST(remainingAfterKeyRemoved, keyLocation, distances):
    distancesToKey = []
    for remaining in remainingAfterKeyRemoved:
        dist = distances[keyLocation, remaining]
        heapq.heappush(distancesToKey, dist)
    return heapq.heappop(distancesToKey)


def harryBfs(currentLocation, nextLocation, isNavigable, isVisited, pathsExplored):
    possibleCurrentLocation = currentLocation
    possibleCurrentRow = currentLocation[0]
    possibleCurrentColumn = currentLocation[1]
    possiblePath = []
    mazeShape = isNavigable.shape
    numRows = mazeShape[0]
    numCols = mazeShape[1]
    queue = deque()
    isFailed = False
    test = 0
    while True:
        test += 1
        if isFailed:
            print('failure')
            sys.exit()
        pathsExplored += 1
        if possibleCurrentLocation == nextLocation:
            isVisited.fill(0)
            return (len(possiblePath), possiblePath)
        if not isVisited[possibleCurrentRow, possibleCurrentColumn]:
            isVisited[possibleCurrentRow, possibleCurrentColumn] = True
            leftCol = possibleCurrentColumn
            if leftCol > 0:
                leftCol -= 1
                if not isNavigable[possibleCurrentRow, leftCol]:
                    leftCol = possibleCurrentColumn
            left = (possibleCurrentRow, leftCol)
            leftPath = possiblePath.copy()
            leftPath.append(left)
            queue.append((left, leftPath))
            rightCol = possibleCurrentColumn
            if rightCol < (numCols - 1):
                rightCol += 1
                if not isNavigable[possibleCurrentRow, rightCol]:
                    rightCol = possibleCurrentColumn
            right = (possibleCurrentRow, rightCol)
            rightPath = possiblePath.copy()
            rightPath.append(right)
            queue.append((right, rightPath))
            upRow = possibleCurrentRow
            if upRow > 0:
                upRow -= 1
                if not isNavigable[upRow, possibleCurrentColumn]:
                    upRow = possibleCurrentRow
            up = (upRow, possibleCurrentColumn)
            upPath = possiblePath.copy()
            upPath.append(up)
            queue.append((up, upPath))
            downRow = possibleCurrentRow
            if downRow < (numRows - 1):
                downRow += 1
                if not isNavigable[downRow, possibleCurrentColumn]:
                    downRow = possibleCurrentRow
            down = (downRow, possibleCurrentColumn)
            downPath = possiblePath.copy()
            downPath.append(down)
            queue.append((down, downPath))
        if queue:
            # if test > 7 and test < 9:
            #     print(queue[0])
            currentTest = queue.popleft()
            possibleCurrentLocation = currentTest[0]
            possiblePath = currentTest[1]
            possibleCurrentRow = possibleCurrentLocation[0]
            possibleCurrentColumn = possibleCurrentLocation[1]
        else:
            isFailed = True


def harryAstar(currentLocation, nextLocation, isNavigable, isVisited, pathsExplored):
    possibleCurrentLocation = currentLocation
    possibleCurrentRow = possibleCurrentLocation[0]
    possibleCurrentColumn = possibleCurrentLocation[1]
    possiblePath = []
    mazeShape = isNavigable.shape
    numRows = mazeShape[0]
    numCols = mazeShape[1]
    fringe = []
    isFailed = False
    test = 0
    while not possibleCurrentLocation == nextLocation:
        if isFailed:
            print('failure')
            sys.exit()
        if not isVisited[possibleCurrentRow, possibleCurrentColumn]:
            isVisited[possibleCurrentRow, possibleCurrentColumn] = True
            leftCol = possibleCurrentColumn
            if leftCol > 0:
                leftCol -= 1
                if not isNavigable[possibleCurrentRow, leftCol]:
                    leftCol = possibleCurrentColumn
            left = (possibleCurrentRow, leftCol)
            leftPath = possiblePath.copy()
            leftPath.append(left)
            possibleAStar = len(leftPath) + distance(left, nextLocation)
            heapq.heappush(fringe, (possibleAStar, (left, leftPath)))
            rightCol = possibleCurrentColumn
            if rightCol < (numCols - 1):
                rightCol += 1
                if not isNavigable[possibleCurrentRow, rightCol]:
                    rightCol = possibleCurrentColumn
            right = (possibleCurrentRow, rightCol)
            rightPath = possiblePath.copy()
            rightPath.append(right)
            possibleAStar = len(rightPath) + distance(right, nextLocation)
            heapq.heappush(fringe, (possibleAStar, (right, rightPath)))
            upRow = possibleCurrentRow
            if upRow > 0:
                upRow -= 1
                if not isNavigable[upRow, possibleCurrentColumn]:
                    upRow = possibleCurrentRow
            up = (upRow, possibleCurrentColumn)
            upPath = possiblePath.copy()
            upPath.append(up)
            possibleAStar = len(upPath) + distance(up, nextLocation)
            heapq.heappush(fringe, (possibleAStar, (up, upPath)))
            downRow = possibleCurrentRow
            if downRow < (numRows - 1):
                downRow += 1
                if not isNavigable[downRow, possibleCurrentColumn]:
                    downRow = possibleCurrentRow
            down = (downRow, possibleCurrentColumn)
            downPath = possiblePath.copy()
            downPath.append(down)
            possibleAStar = len(downPath) + distance(down, nextLocation)
            heapq.heappush(fringe, (possibleAStar, (down, downPath)))
        if fringe:
            fromFringe = heapq.heappop(fringe)
            possibleCurrentLocation = fromFringe[1][0]
            possibleCurrentRow = possibleCurrentLocation[0]
            possibleCurrentColumn = possibleCurrentLocation[1]
            possiblePath = fromFringe[1][1]
        else:
            isFailed = True
    isVisited.fill(0)
    return (len(possiblePath), possiblePath)


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


# main
with open(sys.argv[1], 'r') as f:
    maze = extract_table(f)
mazeWidth = len(maze[0])
mazeHeight = len(maze)
isVisited = numpy.zeros((mazeHeight, mazeWidth), dtype=bool)
isNavigable = numpy.zeros((mazeHeight, mazeWidth), dtype=bool)
isDoor = numpy.zeros((mazeHeight, mazeWidth), dtype=bool)
doorLocation = ()
isKey = numpy.zeros((mazeHeight, mazeWidth), dtype=bool)
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
search = sys.argv[2]
if search == 'dfs':
    isFailed = False
    stack = deque()
    # test = 0
    while True:
        # print(stack)
        # print(currentPath)
        # test += 1
        # if test > 6:
        #     break
        if isFailed:
            print('failure')
            break
        pathsExplored += 1
        if isDoor[currentRow, currentColumn]:
            print(currentPath)
            print(pathsExplored)
            break
        if not isVisited[currentRow, currentColumn]:
            isVisited[currentRow, currentColumn] = True
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
    isFailed = False
    queue = deque()
    while True:
        if isFailed:
            print('failure')
            break
        pathsExplored += 1
        if isDoor[currentRow, currentColumn]:
            print(currentPath)
            print(pathsExplored)
            break
        if not isVisited[currentRow, currentColumn]:
            isVisited[currentRow, currentColumn] = True
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
    gStart = Graph()
    for key in keyLocations:
        gStart.add_vertex(key)
    dummyPathsExplored = 0
    vertices = gStart.vertices()
    distances = {}
    index = 3
    indexNames = {}
    indexNames[1] = currentLocation
    indexNames[2] = doorLocation
    largeNumber = 1000000
    for u in vertices:
        for v in vertices:
            dist = harryAstar(u, v, isNavigable, isVisited, dummyPathsExplored)
            dist = dist[0]
            distances[(u, v)] = dist
            distances[(v, u)] = dist
        indexNames[index] = u
        index += 1
    for u in vertices:
        dist = harryAstar(u, currentLocation, isNavigable, isVisited, dummyPathsExplored)
        dist = dist[0]
        distances[(u, currentLocation)] = dist
        distances[(currentLocation, u)] = dist
    for u in vertices:
        dist = harryAstar(u, doorLocation, isNavigable, isVisited, dummyPathsExplored)
        dist = dist[0]
        distances[(u, doorLocation)] = dist
        distances[(doorLocation, u)] = dist
    # start to end
    dist = harryAstar(currentLocation, doorLocation, isNavigable, isVisited, dummyPathsExplored)
    dist = dist[0]
    distances[(currentLocation, doorLocation)] = dist
    distances[(doorLocation, currentLocation)] = dist

    # make connector index 0
    # make start index 1
    # make end index 2
    # make start and end only connect on each other and solve tsp

    arraySize = len(vertices) + 3
    distance_matrix = numpy.zeros((arraySize, arraySize))
    distance_matrix[0][1] = 1
    distance_matrix[1][0] = distance_matrix[0][1]
    distance_matrix[0][2] = 1
    distance_matrix[2][0] = distance_matrix[0][2]
    for i in range(3, arraySize):
        distance_matrix[0][i] = largeNumber
        distance_matrix[i][0] = largeNumber
    keys = indexNames.keys()
    for i in range(arraySize):
        for j in range(arraySize):
            if i in keys and j in keys:
                if not i == j:
                    distance_matrix[i][j] = distances[(indexNames[i], indexNames[j])]
    # print(distance_matrix)
    # permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
    permutation, tspDistance = solve_tsp_simulated_annealing(distance_matrix)
    pathFromTSP = deque()
    for u in permutation:
        if u == 0:
            continue
        pathFromTSP.append(indexNames[u])
    currentLoc = pathFromTSP.popleft()
    finalPath = []
    finalPath.append(currentLoc)
    while pathFromTSP:
        nextLoc = pathFromTSP.popleft()
        astarAgain = harryAstar(currentLoc, nextLoc, isNavigable, isVisited, pathsExplored)
        for tup in astarAgain[1]:
            finalPath.append(tup)
        currentLoc = nextLoc
        
    if not finalPath[0] == (0, 0):
        finalPath.reverse()

    tspKeyOrder = []
    for loc in finalPath:
        if loc in keyLocations:
            tspKeyOrder.append(loc)

    print(tspKeyOrder)
    print(tspDistance - 2)
    print(finalPath)
    

    #rever for maze5
