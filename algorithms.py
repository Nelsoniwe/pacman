import random
from typing import NewType

test_grid =     ((1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,),
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


#class BFS(object):
def findPathBFS(maze,startx,starty,endx,endy):
    startx = int(startx)
    starty = int(starty)
    endx = int(endx)
    endy = int(endy)

    queue = []
    queue.append((startx,starty))
    envhight = len(test_grid)
    envwidth = len(test_grid[0])
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

    visited[startx][starty] = 1
    oldcount = 1
    newCount = 0
    while len(queue)>0:
        
        p = queue[0]
        queue.pop(0)

        if (p[0] == endx and p[1]== endy):
            return reconstructPath(visited,p[0],p[1])
  
        #print(maze[p[0]][p[1]])
        
        for item in range(4):
            # using the direction array
            a = p[0] + Dir[item][0]
            b = p[1] + Dir[item][1]

            
            # not blocked and valid
            if(a >= 0 and b >= 0 and a < envhight and b < envwidth and visited[a][b] == 0 and visited[a][b] != True) :       
                visited[a][b]= weight + 1   
                queue.append((a, b))
                newCount += 1
        
        oldcount -= 1
        if(oldcount <= 0):
            oldcount = newCount
            newCount = 0
            weight+=1
 
    return queue


def findPathDFS(maze,startx,starty,endx,endy):
    startx = int(startx)
    starty = int(starty)
    endx = int(endx)
    endy = int(endy)

    allpath = []

    queue = []
    # queue.append((startx,starty))
    envhight = len(test_grid)
    envwidth = len(test_grid[0])

    visited = []
    for i in range(len(maze)):
        visited.append([])
        for j in range(len(maze[i])):
            if(maze[i][j]!=0):
                visited[-1].append(0)
            else:
                visited[-1].append(1)
 
    go_to(startx,starty,endx,endy,visited,queue,allpath)
    return allpath[0]


def go_to(startx,starty,endx,endy,visited,queue,allpath):
    queue, visited
    if startx < 0 or starty < 0 or startx > len(visited)-1 or starty > len(visited[0])-1:
        return
    # If we've already been there or there is a wall, quit
    if (startx, starty) in queue or visited[startx][starty] > 0:
        return
    queue.append((startx, starty))
    visited[startx][starty] = 2
    if (startx, starty) == (endx, endy):
        # print("Found!", queue)
        allpath.append(queue.copy())
        queue.pop()
        return
    else:
        go_to(startx - 1, starty,endx,endy,visited,queue,allpath)  # check top
        go_to(startx + 1, starty,endx,endy,visited,queue,allpath)  # check bottom
        go_to(startx, starty + 1,endx,endy,visited,queue,allpath)  # check right
        go_to(startx, starty - 1,endx,endy,visited,queue,allpath)  # check left
    queue.pop()
    return

def UCS(maze,startx,starty,endx,endy):
    startx = int(startx)
    starty = int(starty)
    endx = int(endx)
    endy = int(endy)

    queue = []
    queueweight = []

    field,visited = randomizeweights(maze)
    queue.append((startx,starty))
    queueweight.append(0)

    for i in range(len(field)):
        print(field[i])

    startNode = Node(startx,starty)
    Nodelist = []
    Nodelist.append(startNode)
    a = []
    print(queue[0][0])
    while len(queue)>0:
        min_index = queueweight.index(min(queueweight))
        node = queue.pop(min_index)
        
        if node[0] == endx and node[1] == endy:
            print(pathNode.name(a))
            break
        weightnode = queueweight.pop(min_index)

        visited[node[0]][node[1]] = 1
        pathNode = Node(node[0],node[1],startNode)
        startNode = Node(pathNode.X,pathNode.Y,pathNode.Node)
        Nodelist.append(pathNode)

        he = []   
        heind = []
        if node[0]-2>=0 and visited[node[0]-2][node[1]] != 1:
            he.append((node[0]-2,node[1]))
            heind.append(weightnode+field[node[0]-1][node[1]])
        if node[1]-2>=0 and visited[node[0]][node[1]-2] != 1:
            he.append((node[0],node[1]-2))
            heind.append(weightnode+field[node[0]][node[1]-1])
        if node[0]+2<len(field) and visited[node[0]+2][node[1]] != 1:
            he.append((node[0]+2,node[1]))
            heind.append(weightnode+field[node[0]+1][node[1]])
        if node[1]+2<len(field[0]) and visited[node[0]][node[1]+2] != 1:
            he.append((node[0],node[1]+2))
            heind.append(weightnode+field[node[0]][node[1]+1])
        

        while len(he)>0:
            
            min_index = heind.index(min(heind))
            tempNode = he.pop(min_index)
            queue.append(tempNode)
            queueweight.append(heind.pop(min_index))
            
    


    #back to normal array
    a = []
    for item in queue:
     hehe = queue.pop()
     a.append((int(hehe[0]/2),int(hehe[1]/2)))
    queue = a
    print(queue)
    print(queueweight)
    for i in range(len(visited)-1):
        if i % 2 == 0:
            print()
            for j in range(len(visited[0])-1):
                if j%2 == 0:
                  print(visited[i][j],end='')
    
    for i in range(len(visited)):
        print(visited[i])
        
                
    

def randomizeweights(field):
    newField = []
    visitedfieldbig = []
    r = random

    for i in range(len(field)*2 - 1):
        row = []
        clearrow = []
        for j in range(len(field[0])*2 - 1):
            if (i % 2 == 0) and (j % 2 == 0):
                row.append(field[int(i/2)][int(j/2)])
                if(field[int(i/2)][int(j/2)] == 1):
                    clearrow.append(0)
                else:
                    clearrow.append(1)
            elif(i % 2 != 0) and (j % 2 != 0):
                row.append(0)
                clearrow.append(1)
            else:
                row.append(random.randint(4,9))
                clearrow.append(0)
        newField.append(row)
        visitedfieldbig.append(clearrow)

    return newField,visitedfieldbig


def reconstructPath(maze,x,y):
    stop = True
    envhight = len(maze)
    envwidth = len(maze[0])
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
            if(a >= 0 and b >= 0 and a < envhight and b < envwidth and maze[a][b] != 0 and maze[a][b] < maze[p[0]][p[1]]) :           
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
     
     
# a,b = (randomizeweights(test_grid))

# for i in range(len(b)):
#         print(b[i])
# print()
# for i in range(len(a)):
#         print(a[i])
print(UCS(test_grid,2,0,24,20))

# print(findPathDFS(test_grid,2,1,12,10))

# a = Node(1, 2)
# b = Node(3,4,a)
# print(b.Node.xStart)