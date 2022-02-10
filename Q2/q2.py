import sys
import numpy
from collections import deque
from graph import Graph


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
    # test = 0
    while True:
        # print(queue)
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
    test = 'test'
    gStart = Graph()
    for key in keyLocations:
        gStart.add_vertex(key)
    gStart.add_vertex(doorLocation)
    # starting location -> current location
    # loop
        # (minimum spanning trees of all remaining keys - possible next key) + distance to next possible key
        # select next key for mst with lowest weight
        # go to next key/door with bfs

# don't forget to store the number of paths expanded
