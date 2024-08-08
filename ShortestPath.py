#Finding alternate shortest paths of same distance?

def main():
    connections = []
    extractData(r'C:\Users\willi\OneDrive\Documents\VSCode Projects\Personal Projects\TicketToRide\TTR_Connections.csv', connections)
    path, distance = shortestPath('Vancouver', 'Miami', connections)
    print(path, distance)

def extractData(path, outputList):
    with open(path) as file:
        dataRaw = file.readlines()[1:]
        for data in dataRaw:
            dataAttributes = data.strip().split(',')
            for i in range(2, len(dataAttributes)):
                dataAttributes[i] = int(dataAttributes[i])
            outputList.append(dataAttributes)

def shortestPath(departure, destination, connections):
    shortestPath = [] #List of indexes from 'connections' of the shortest confirmed path
    posConnsList = [] #list of lists of  indexes of possible connections to be made from each connecting city; Used while pathfinding
    path = [departure] #Initialize path to sta rt at departure, used while pathfinding
    distance = 0 #distance traveled on current path
    shortestDistance = 100 #Constant guaranteed to be longer than shortest path

    while True:
        path, distance, posConnsList = findRoute(path, distance, posConnsList, destination, connections, shortestDistance)
        if(len(posConnsList) != 0): #OPT
            shortestDistance = distance
            shortestPath = path.copy()
        
        while((len(posConnsList) > 1 and len(posConnsList[-1]) == 1) or destination in path):
            path, distance, posConnsList = backtrackAndProceedToNextCity(path, distance, posConnsList, connections, shortestDistance) 
            if(destination in path):
                shortestDistance = distance
                shortestPath = path.copy()
        if(len(posConnsList) == 0):
            break
    return shortestPath, shortestDistance

def findRoute(path, distance, posConnsList, destination, connections, shortestDistance):
    while not(destination in path):
        posConns = [] #list of indexes of possible connections from the last city in path list
        
        for i in range(0, len(connections)): #Find all possible paths which dont cause a loop
            if path[-1] in connections[i] and cityNotInPath(path, connections[i]): #last city is part of the connection and the other city in the connection is not already part of the path
                posConns.append(i)
        
        if len(posConns) == 0: #If no routes forward, backtrack
            path, distance, posConnsList = backtrackAndProceedToNextCity(path, distance, posConnsList, connections, shortestDistance)
        else:
            distance += connections[posConns[0]][2] #Increment distance traveled on current path

            if connections[posConns[0]][0] != path[-1]: #Find which one of the cities in the "connections" index is the next city
                nextCity = connections[posConns[0]][0]
            else:
                nextCity = connections[posConns[0]][1]
            path.append(nextCity)
            posConnsList.append(posConns)

            if(distance > shortestDistance): #if new distance is greater than established shortest path, backtrack
                path, distance, posConnsList = backtrackAndProceedToNextCity(path, distance, posConnsList, connections, shortestDistance)
        if(len(posConnsList) == 0 and len(posConns) == 0): #OPT
            break
    return path, distance, posConnsList

def cityNotInPath(path, connection): #checks if connection causes a loop (going to a city already in the path)
    for item in connection:
        if item != path[-1] and item in path:
            return False
    return True

def backtrackAndProceedToNextCity(path, distance, posConnsList, connections, shortestDistance):
    while True:
        while True:
            distance -= connections[posConnsList[-1][0]][2] #Subtracts the distance of the last used path
            path.pop()
            posConns = posConnsList[-1]
            posConnsList.pop()
            posConns.pop(0) #backtrack initially, then check if there are paths forward after deleting most recent connection
            if len(posConns) > 0 or len(posConnsList) == 0:
                break
        if(len(posConnsList) == 0 and len(posConns) == 0): #OPT
            break
        if connections[posConns[0]][0] != path[-1]: #Find which one of the cities in the "connections" index is the next city
            nextCity = connections[posConns[0]][0]
        else:
            nextCity = connections[posConns[0]][1]
        path.append(nextCity)
        distance += connections[posConns[0]][2]
        posConnsList.append(posConns)
        if(distance < shortestDistance):
            break
    return path, distance, posConnsList

if __name__ == '__main__':
    main()
