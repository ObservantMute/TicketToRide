def main():
    connections = [csvfile] #dont worry about this
    posConns = [34]
    posConnsList = [[0], [1, 47, 69], [61], [31], [73]]
    path = ['Vancouver', 'Seattle', 'Portland', 'San Francisco', 'Los Angeles', 'El Paso']
    distance = 16
    backtrackAndProceedToNextCity(path, distance, posConns, posConnsList, connections)

def backtrackAndProceedToNextCity(path, distance, posConns, posConnsList, connections):
    while True:
        distance -= connections[posConnsList[-1][0]][2]
        path.pop() 
        posConns = posConnsList[-1]
        posConnsList.pop()
        posConns.pop(0) #backtrack initially, then check if there are paths forward after deleting most recent connection
        if len(posConnsList) == 0:
            return 0
        if len(posConns) > 0:
            break
    if connections[posConns[0]][0] != path[-1]: #Find which one of the cities in the "connections" index is the next city
        nextCity = connections[posConns[0]][0]
    else:
        nextCity = connections[posConns[0]][1]
    path.append(nextCity)
    posConnsList.append(posConns)
    #return path, distance, posConns, posConnsList

if __name__ == '__main__':
    main()

My knowledge of how functions work is that if you pass a variable in through the arguments and change the variable's value, those changes will be reflected in the variable outside the function. 
path and posConnsList follow this assumption, however distance and posConns do not. Why? For example, after the function runs, path and posConnsList are updated as expected, however, posConns reverts to [34] and distance to 16.
