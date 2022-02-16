import sys
import heapq

# taken from stack overflow, used to import CSV tables
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


# main

fileName = sys.argv[1]
with open(fileName, 'r') as f:
    heuristic = extract_table(f)
    actual = extract_table(f)
# the dictionary containing heuristic distances between locations
heuristicDict = {}
for i in range(1, len(heuristic)):
    heuristicDict[heuristic[i][0]] = int(heuristic[i][1])
# the dictionary containing actual distances between locations
actualDict = {}
for i in range(1, len(actual)):
    actualDict[(actual[i][0] + actual[i][1])] = int(actual[i][2])
    actualDict[(actual[i][1] + actual[i][0])] = int(actual[i][2])
# the set of locations that are goals
goal = set()
for location, distance in heuristicDict.items():
    if distance == 0:
        goal.add(location)
# assumption: start location is 'S'
currentLocation = 'S'
currentPath = 'S'
pathDistanceTravelled = 0
fringe = []  # heapq
# check if we have arrived at a goal location
while currentLocation not in goal:
    currentNameLength = len(currentLocation)
    # add the next iteration to the fringe based on the process described in class
    for locations, distance in actualDict.items():
        if locations[:currentNameLength] == currentLocation:
            possibleNextLocation = locations[currentNameLength:]
            possiblePath = currentPath + possibleNextLocation
            possibleAStar = pathDistanceTravelled + distance + heuristicDict[possibleNextLocation]
            possiblePathDistanceTravelled = pathDistanceTravelled + distance
            heapq.heappush(fringe, (possibleAStar, (possibleNextLocation, (possiblePathDistanceTravelled, possiblePath))))
    # pop the next shortest possible path from the fringe
    fromFringe = heapq.heappop(fringe)
    currentLocation = fromFringe[1][0]
    currentPath = fromFringe[1][1][1]
    pathDistanceTravelled = fromFringe[1][1][0]
# print(currentPath)
# print(currentLocation)
# print(pathDistanceTravelled)

fileName = fileName[:-4]
fileName += '_solution.txt'
prepend = './Solutions/'
fileName = prepend + fileName

output = '[\'' + currentPath + '\', ' + str(pathDistanceTravelled) + ']'
# output = [currentPath, pathDistanceTravelled]

f = open(fileName, "w")
f.write(output)
f.close()
