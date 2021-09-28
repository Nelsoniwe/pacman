import random
from datetime import datetime
import sys
import tabulate
import numpy as np

testGrid =      ((1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,),
                 (1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,1,),
                 (1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,),
                 (1,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,1,),
                 (1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,),
                 (0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,),
                 (0,0,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,),
                 (0,0,0,1,0,1,0,0,1,0,0,1,0,1,0,0,0,),
                 (1,1,1,1,1,1,0,3,3,3,0,1,1,1,1,1,1,),
                 (0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,),
                 (0,0,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,),
                 (0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,),
                 (1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,),
                 (1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,1,),
                 (1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,),
                 (0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,),
                 (1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,),
                 (1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,),
                 (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,))


#BFS
def findPathBFS(maze,startX,startY,endX,endY):
    startTime = datetime.now()
    startX = int(startX)
    startY = int(startY)
    endX = int(endX)
    endY = int(endY)

    queue = []
    queue.append((startX,startY))
    envHight = len(maze)
    envWidth = len(maze[0])
    Dir = [[-1, 0], [0, -1], [1, 0],[0, 1]]
    weight = 1

    visited = []
    for i in range(len(maze)):
        visited.append([])
        for j in range(len(maze[i])):
            if(maze[i][j]!=0):
                visited[-1].append(0)
            else:
                visited[-1].append(True)

    visited[startX][startY] = 1
    oldCount = 1
    newCount = 0
    while len(queue)>0:
        
        p = queue[0]
        queue.pop(0)

        if (p[0] == endX and p[1]== endY):
            endTime = datetime.now()
            queue = reconstructPath(visited,p[0],p[1])
            print('time of work BFS:', endTime - startTime)
            print('path:', queue)
            return queue
  
        for item in range(4):
            # using the direction array
            a = p[0] + Dir[item][0]
            b = p[1] + Dir[item][1]

            # not blocked and valid
            if(a >= 0 and b >= 0 and a < envHight and b < envWidth and visited[a][b] == 0 and visited[a][b] != True) :       
                visited[a][b]= weight + 1   
                queue.append((a, b))
                newCount += 1
        
        oldCount -= 1
        if(oldCount <= 0):
            oldCount = newCount
            newCount = 0
            weight+=1
    
    return queue

#DFS algorithm
def findPathDFS(maze,startX,startY,endX,endY):
    startTime = datetime.now()
    startX = int(startX)
    startY = int(startY)
    endX = int(endX)
    endY = int(endY)

    allPath = []
    queue = []

    visited = []
    for i in range(len(maze)):
        visited.append([])
        for j in range(len(maze[i])):
            if(maze[i][j]!=0):
                visited[-1].append(0)
            else:
                visited[-1].append(1)
 
    goTo(startX,startY,endX,endY,visited,queue,allPath)
    endTime = datetime.now()
    print('time of work DFS:', endTime - startTime)
    print('path:', allPath[0])
    return allPath[0]

#DFS algorithm
def goTo(startX,startY,endX,endY,visited,queue,allPath):
    queue, visited
    if startX < 0 or startY < 0 or startX > len(visited)-1 or startY > len(visited[0])-1:
        return
    if (startX, startY) in queue or visited[startX][startY] > 0:
        return
    queue.append((startX, startY))
    visited[startX][startY] = 2
    if (startX, startY) == (endX, endY):
        allPath.append(queue.copy())
        queue.pop()
        return
    else:
        goTo(startX - 1, startY,endX,endY,visited,queue,allPath)  # up
        goTo(startX + 1, startY,endX,endY,visited,queue,allPath)  # down
        goTo(startX, startY + 1,endX,endY,visited,queue,allPath)  # right
        goTo(startX, startY - 1,endX,endY,visited,queue,allPath)  # left
    queue.pop()
    return

# manhattan
def heuristic(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])

# euclidean
def euclidean(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

# euclidean Squared
def euclideanSquared(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

def UCS(maze, startX, startY, endX, endY):
   
    startX = int(startX)*2
    startY = int(startY)*2
    endX = int(endX)*2
    endY = int(endY)*2

    # list of Nodes (with coordinates)
    nodesList = []
    # Nodes weights
    nodesWeightsList = []

    nodesList.append(Node(startX, startY, None))
    nodesWeightsList.append(0)

    # randomize weights for fields
    field, visited = randomizeWeights(maze)

    startTime = datetime.now()
    startNode = None

    while len(nodesList) > 0:
        minIndex = nodesWeightsList.index(min(nodesWeightsList))
        print(nodesWeightsList)
        node = nodesList[minIndex]
        weightNode = nodesWeightsList[minIndex]
        field[node.X][node.Y] = weightNode 
        nodesWeightsList[minIndex] = sys.maxsize

        startNode = Node(node.X, node.Y, startNode)
        visited[node.X][node.Y] = 1

        # if we find endpoint
        if node.X == endX and node.Y == endY:
            endTime = datetime.now()
            print('time of work UCS:', endTime - startTime)
            queue = reconstructPathForUCS(node)
            print('path:', queue)
            return queue, field

        tempArray = []
        tempWeightIndexesArray = []
        if node.X - 2 >= 0 and visited[node.X - 2][node.Y] != 1:
            tempArray.append(Node(node.X - 2, node.Y,node))
            asd = field[node.X - 1][node.Y]
            tempWeightIndexesArray.append(weightNode + field[node.X - 1][node.Y])
        if node.Y - 2 >= 0 and visited[node.X][node.Y - 2] != 1:
            tempArray.append(Node(node.X, node.Y - 2,node))
            asd = field[node.X][node.Y - 1] 
            tempWeightIndexesArray.append(weightNode + field[node.X][node.Y - 1])
        if node.X + 2 < len(field) and visited[node.X + 2][node.Y] != 1:
            tempArray.append(Node(node.X + 2, node.Y,node))
            asd = field[node.X + 1][node.Y]
            tempWeightIndexesArray.append(weightNode + field[node.X + 1][node.Y])
        if node.Y + 2 < len(field[0]) and visited[node.X][node.Y + 2] != 1:
            print("len field = " + str(len(field[0])))
            tempArray.append(Node(node.X, node.Y + 2,node))
            asd = field[node.X][node.Y + 1]
            tempWeightIndexesArray.append(weightNode + field[node.X][node.Y + 1])

        while len(tempArray) > 0:
            tempNode = tempArray.pop()
            nodesList.append(tempNode)
            nodesWeightsList.append(tempWeightIndexesArray.pop())
        
def Astar(maze, startX, startY, endX, endY, heuristic):
   
    startX = int(startX)*2
    startY = int(startY)*2
    endX = int(endX)*2
    endY = int(endY)*2

    # list of Nodes (with coordinates)
    nodesList = []
    # Nodes weights
    nodesWeightsList = []

    nodesList.append(Node(startX, startY, None))
    nodesWeightsList.append(0)

    # randomize weights for fields
    field, visited = randomizeWeights(maze)


    startTime = datetime.now()
    startNode = None
    # nodeList = []
    # nodeList.append(startNode)

    while len(nodesList) > 0:
        minIndex = nodesWeightsList.index(min(nodesWeightsList))
        node = nodesList[minIndex]
        weightNode = nodesWeightsList[minIndex]
        field[node.X][node.Y] = weightNode 
        nodesWeightsList[minIndex] = sys.maxsize

        startNode = Node(node.X, node.Y, startNode)
        visited[node.X][node.Y] = 1

        # startNode = Node(pathNode.X,pathNode.Y,pathNode.Node)
        # nodeList.append(startNode)

        # if we find endpoint
        if node.X == endX and node.Y == endY:
            # endTime = datetime.now()
            # print('time of work Astar:', endTime - startTime)
            
            queue = reconstructPathForUCS(node)
            # print('path:', queue)
            return queue, field

        tempArray = []
        tempWeightIndexesArray = []
        if node.X - 2 >= 0 and visited[node.X - 2][node.Y] != 1:
            tempArray.append(Node(node.X - 2, node.Y,node))
            asd = field[node.X - 1][node.Y] 
            tempWeightIndexesArray.append(weightNode + field[node.X - 1][node.Y]+ heuristic((node.X - 1,node.Y),(endX,endY)))
        if node.Y - 2 >= 0 and visited[node.X][node.Y - 2] != 1:
            tempArray.append(Node(node.X, node.Y - 2,node))
            asd = field[node.X][node.Y - 1] 
            tempWeightIndexesArray.append(weightNode + field[node.X][node.Y - 1]+ heuristic((node.X,node.Y - 1),(endX,endY)))
        if node.X + 2 < len(field) and visited[node.X + 2][node.Y] != 1:
            tempArray.append(Node(node.X + 2, node.Y,node))
            asd = field[node.X + 1][node.Y]
            tempWeightIndexesArray.append(weightNode + field[node.X + 1][node.Y]+ heuristic((node.X + 1,node.Y),(endX,endY)))
        if node.Y + 2 < len(field[0]) and visited[node.X][node.Y + 2] != 1:
            tempArray.append(Node(node.X, node.Y + 2,node))
            asd = field[node.X][node.Y + 1]
            tempWeightIndexesArray.append(weightNode + field[node.X][node.Y + 1]+ heuristic((node.X,node.Y + 1),(endX,endY)))

        while len(tempArray) > 0:
            tempNode = tempArray.pop()
            nodesList.append(tempNode)
            nodesWeightsList.append(tempWeightIndexesArray.pop())
        
    # back to normal array
    a = []
    for item in nodesList:
        hehe = nodesList.pop()
        a.append((int(hehe[0] / 2), int(hehe[1] / 2)))
    queue = a
    print(queue)
    print(nodesWeightsList)
    for i in range(len(field) - 1):
        if i % 2 == 0:
            print()
            for j in range(len(field[0]) - 1):
                if j % 2 == 0:
                    print(field[i][j], end='')

    for i in range(len(visited)):
        print(visited[i])

def range_sum(row):
    # summing in range element
    return sum([abs(sub[1] - sub[0]) for sub in row if sub[0] > i and sub[0] < j and sub[1] > i and sub[1] < j])

def multyAStar(maze, startX, startY, endX, endY,pointsArr, heuristic):
    path = []
    temp = []
    # temp.insert(0,(startX*32,startY*32))
    for item in pointsArr:
        temp.append((item.rect[0],item.rect[1]))
    sorted(temp , key=lambda k: [k[1], k[0]])
    # (startX*32,startY*32)
    
    # for item in pointsArr:
    #     arra, field  = Astar(maze,startX,startY,item.rect[1]/32,item.rect[0]/32,heuristic)
    #     startX = item.rect[1]/32
    #     startY = item.rect[0]/32
    #     path.append(arra)
    for item in temp:
        arra, field  = Astar(maze,startX,startY,item[1]/32,item[0]/32,heuristic)
        startX = int(item[1]/32)
        startY = int(item[0]/32)
        path.append(arra)
    if endX != None:
        arra, field  = Astar(maze,startX,startY,endX,endY,heuristic)
        path.append(arra)
    return path,field
    
def randomizeWeights(field):
    newField = []
    visitedFieldBig = []
    r = random

    for i in range(len(field)*2 - 1):
        row = []
        clearRow = []
        for j in range(len(field[0])*2 - 1):
            if (i % 2 == 0) and (j % 2 == 0):
                row.append(field[int(i/2)][int(j/2)])
                if(field[int(i/2)][int(j/2)] == 1):
                    clearRow.append(0)
                elif(field[int(i/2)][int(j/2)] == 2):
                    clearRow.append(0)
                else:
                    clearRow.append(1)
            elif(i % 2 != 0) and (j % 2 != 0):
                row.append(0)
                clearRow.append(1)
            else:
                row.append(random.randint(4,9))
                clearRow.append(0)
        newField.append(row)
        visitedFieldBig.append(clearRow)

    return newField,visitedFieldBig

def reconstructPathForUCS(node):
    queue = []
    while(node != None):
        queue.append((node.X/2,node.Y/2))
        node = node.Node
    return queue


#reconstruct path to DFS algorithm 
def reconstructPath(maze,x,y):
    stop = True
    envHight = len(maze)
    envWidth = len(maze[0])
    Dir = [[-1, 0], [0, -1], [1, 0],[0, 1]]
    queue = []
    queue.append((x,y))

    newArr = []
    for i in range(len(maze)):
        newArr.append([])
        for j in range(len(maze[i])):
            if(maze[i][j] == True):
                newArr[-1].append(0)
            else:
                newArr[-1].append(maze[i][j])
    
    maze = newArr

    while stop:
        p = queue[len(queue)-1]
        for item in range(4):
            # using the direction array
            a = p[0] + Dir[item][0]
            b = p[1] + Dir[item][1]

            # not blocked and valid
            if(a >= 0 and b >= 0 and a < envHight and b < envWidth and maze[a][b] != 0 and maze[a][b] < maze[p[0]][p[1]]) :           
                queue.append((a, b))
                #print(maze[a][b])
                break
        if(maze[p[0]][p[1]]==2):
            stop = False
    return (queue)

class Node:
    def __init__(self, x, y, bNode = None):
        self.X = x
        self.Y = y
        self.Node = bNode
    def name(self,b):
        if self.Node != None:
          b.append(self.Node)
          print(self.X," ", self.Y)
          return self.name(b)
        else:
            return b
    