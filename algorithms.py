import random
from datetime import datetime

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
    envHight = len(testGrid)
    envWidth = len(testGrid[0])
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
            print('time of work BFS:', endTime - startTime)
            print('path:', queue)
            return reconstructPath(visited,p[0],p[1])
  
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

def UCS(maze,startX,startY,endX,endY):
    startX = int(startX)
    startY = int(startY)
    endX = int(endX)
    endY = int(endY)

    queue = []
    queueWeight = []

    field,visited = randomizeWeights(maze)
    queue.append((startX,startY))
    queueWeight.append(0)

    # for i in range(len(field)):
    #     print(field[i])

    startNode = None
    nodeList = []
    nodeList.append(startNode)
    a = []
    #print(queue[0][0])
    while len(queue)>0:
        startNode = Node(node[0],node[1],startNode)
        minIndex = queueWeight.index(min(queueWeight))
        node = queue.pop(minIndex)
        
        visited[node[0]][node[1]] = 1
        
        # startNode = Node(pathNode.X,pathNode.Y,pathNode.Node)
        nodeList.append(startNode)

        #if we find endpoint
        if node[0] == endX and node[1] == endY:
            # print(startNode.name(a))
            break
        weightNode = queueWeight.pop(minIndex)

        he = []   
        heind = []
        if node[0]-2>=0 and visited[node[0]-2][node[1]] != 1:
            he.append((node[0]-2,node[1]))
            heind.append(weightNode+field[node[0]-1][node[1]])
        if node[1]-2>=0 and visited[node[0]][node[1]-2] != 1:
            he.append((node[0],node[1]-2))
            heind.append(weightNode+field[node[0]][node[1]-1])
        if node[0]+2<len(field) and visited[node[0]+2][node[1]] != 1:
            he.append((node[0]+2,node[1]))
            heind.append(weightNode+field[node[0]+1][node[1]])
        if node[1]+2<len(field[0]) and visited[node[0]][node[1]+2] != 1:
            he.append((node[0],node[1]+2))
            heind.append(weightNode+field[node[0]][node[1]+1])
        

        while len(he)>0:
            
            minIndex = heind.index(min(heind))
            tempNode = he.pop(minIndex)
            queue.append(tempNode)
            queueWeight.append(heind.pop(minIndex))
            
    # back to normal array
    a = []
    for item in queue:
     hehe = queue.pop()
     a.append((int(hehe[0]/2),int(hehe[1]/2)))
    queue = a
    print(queue)
    print(queueWeight)
    for i in range(len(visited)-1):
        if i % 2 == 0:
            print()
            for j in range(len(visited[0])-1):
                if j%2 == 0:
                  print(visited[i][j],end='')
    
    for i in range(len(visited)):
        print(visited[i])
        
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

#reconstruct path to DFS algorithm 
def reconstructPath(maze,x,y):
    stop = True
    envHight = len(maze)
    envWidth = len(maze[0])
    Dir = [[-1, 0], [0, -1], [1, 0],[0, 1]]
    queue = []
    queue.append((x,y))

    #maze[maze == True] = 0
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
     
#trash
# print(UCS(testGrid,2,0,24,20))
# (findPathDFS(testGrid,2,1,0,0))
# (findPathBFS(testGrid,2,1,16,16))