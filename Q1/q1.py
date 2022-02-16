import sys
import heapq


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
heuristicDict = {}
for i in range(1, len(heuristic)):
    heuristicDict[heuristic[i][0]] = int(heuristic[i][1])
actualDict = {}
for i in range(1, len(actual)):
    actualDict[(actual[i][0] + actual[i][1])] = int(actual[i][2])
    actualDict[(actual[i][1] + actual[i][0])] = int(actual[i][2])
goal = set()
for location, distance in heuristicDict.items():
    if distance == 0:
        goal.add(location)
# assumption: start location is 'S'
currentLocation = 'S'
currentPath = 'S'
pathDistanceTravelled = 0
fringe = []  # heapq
while currentLocation not in goal:
    currentNameLength = len(currentLocation)
    for locations, distance in actualDict.items():
        if locations[:currentNameLength] == currentLocation:
            possibleNextLocation = locations[currentNameLength:]
            possiblePath = currentPath + possibleNextLocation
            possibleAStar = pathDistanceTravelled + distance + heuristicDict[possibleNextLocation]
            possiblePathDistanceTravelled = pathDistanceTravelled + distance
            heapq.heappush(fringe, (possibleAStar, (possibleNextLocation, (possiblePathDistanceTravelled, possiblePath))))
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
