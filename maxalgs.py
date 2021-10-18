
import random
from numpy import fabs, newaxis
from numpy.core.fromnumeric import around
import pygame
import algorithms
import labirinthalg
import enum
import sys


class MaxNode:
    def __init__(self,parent, x,y, isMax,Value = None):
        self.X = x
        self.Y = y
        self.Parent = parent
        self.Nodes = []
        self.Value = Value
        self.isMax = isMax
        self.Allpoints = 0


def minimax(field,player,enemies,foodList):
    playerCords = ((player.rect.bottomright[1]-16)/32,(player.rect.bottomright[0]-16)/32)
    enemiesList = []
    for ghost in enemies:
        enemiesList.append(((ghost.rect.bottomright[1]-16)/32,(ghost.rect.bottomright[0]-16)/32))

    playerCoordsNextList = GetRoadCordsAroundPoint(field,playerCords[0],playerCords[1])
    enemiesListNextList = []

    nearestEnemy = enemiesList[0]

    for item in enemiesList:
        if algorithms.heuristic(((playerCords[0]),(playerCords[1])),(item[0],item[1])) < algorithms.heuristic(((playerCords[0]),(playerCords[1])),(nearestEnemy[0],nearestEnemy[1])):
          nearestEnemy = item

    enemyAroundPoints = GetRoadCordsAroundPoint(field,nearestEnemy[0],nearestEnemy[1])

    nearestFood = FindNearestPoint((playerCords[0],playerCords[1]),foodList,field)

    sourceNode = MaxNode(None,None,None,True)
    for item in playerCoordsNextList:
        sourceNode.Nodes.append(MaxNode(sourceNode,item[0],item[1],False))

    for playerMoves in sourceNode.Nodes:
        for ghostMoves in enemyAroundPoints:
            disToGhost = algorithms.euclideanSquared(((playerMoves.X),(playerMoves.Y)),(ghostMoves[0],ghostMoves[1]))
            disToFood = algorithms.euclideanSquared(((playerMoves.X),(playerMoves.Y)),(nearestFood[0],nearestFood[1]))*1000
            if disToGhost <= 1:
                playerMoves.Nodes.append(MaxNode(playerMoves,ghostMoves[0],ghostMoves[1],False,-99999))
            elif disToFood == 0:
                playerMoves.Nodes.append(MaxNode(playerMoves,ghostMoves[0],ghostMoves[1],False,9999+disToGhost-disToFood))
            else:
                playerMoves.Nodes.append(MaxNode(playerMoves,ghostMoves[0],ghostMoves[1],False,disToGhost-disToFood))


    for playerMoves in sourceNode.Nodes:
        oldValue = sys.maxsize
        for ghostMoves in playerMoves.Nodes:
            if ghostMoves.Value < oldValue:
              oldValue = ghostMoves.Value
              playerMoves.Value = oldValue

    finishNode = -sys.maxsize
    finishCords = None
    for playerMoves in sourceNode.Nodes:
        if playerMoves.Value > finishNode:
          finishNode = playerMoves.Value
          finishCords = playerMoves



    return finishCords


def expectimax(field,player,enemies,foodList):
    playerCords = ((player.rect.bottomright[1]-16)/32,(player.rect.bottomright[0]-16)/32)
    enemiesList = []
    for ghost in enemies:
        enemiesList.append(((ghost.rect.bottomright[1]-16)/32,(ghost.rect.bottomright[0]-16)/32))

    playerCoordsNextList = GetRoadCordsAroundPoint(field,playerCords[0],playerCords[1])
    enemiesListNextList = []

    nearestEnemy = enemiesList[0]

    for item in enemiesList:
        if algorithms.heuristic(((playerCords[0]),(playerCords[1])),(item[0],item[1])) < algorithms.heuristic(((playerCords[0]),(playerCords[1])),(nearestEnemy[0],nearestEnemy[1])):
          nearestEnemy = item

    enemyAroundPoints = GetRoadCordsAroundPoint(field,nearestEnemy[0],nearestEnemy[1])

    nearestFood = FindNearestPoint((playerCords[0],playerCords[1]),foodList,field)

    sourceNode = MaxNode(None,None,None,True)
    for item in playerCoordsNextList:
        sourceNode.Nodes.append(MaxNode(sourceNode,item[0],item[1],False))

    for playerMoves in sourceNode.Nodes:
        for ghostMoves in enemyAroundPoints:
            disToGhost = algorithms.euclideanSquared(((playerMoves.X),(playerMoves.Y)),(ghostMoves[0],ghostMoves[1]))
            disToFood = algorithms.euclideanSquared(((playerMoves.X),(playerMoves.Y)),(nearestFood[0],nearestFood[1]))*100
            if disToGhost <= 1:
                playerMoves.Nodes.append(MaxNode(playerMoves,ghostMoves[0],ghostMoves[1],False,-99999))
            # elif disToFood == 0:
            #     playerMoves.Nodes.append(MaxNode(playerMoves,ghostMoves[0],ghostMoves[1],False,99999+disToGhost-disToFood))
            else:
                playerMoves.Nodes.append(MaxNode(playerMoves,ghostMoves[0],ghostMoves[1],False,disToGhost-disToFood))


    for playerMoves in sourceNode.Nodes:
        oldValue = 0
        count = 0
        for ghostMoves in playerMoves.Nodes:
            oldValue += ghostMoves.Value
            count+=1
        playerMoves.Value = oldValue/count

    finishNode = -sys.maxsize
    finishCords = None
    for playerMoves in sourceNode.Nodes:
        if playerMoves.Value > finishNode:
          finishNode = playerMoves.Value
          finishCords = playerMoves



    return finishCords

def FindNearestPoint(pacmanPoint,listOfPoints,field = None):
    pacmanPoint = (int(pacmanPoint[0]),int(pacmanPoint[1]))
    oldDist = sys.maxsize
    cord = None
    listEqCords = []
    for item in listOfPoints:
        newDist = algorithms.euclideanSquared(((pacmanPoint[0]),(pacmanPoint[1])),((((item.rect.y-12)/32),(item.rect.x-12)/32)))
        #newDist = len(algorithms.findPathBFS(field,(pacmanPoint[1]),(pacmanPoint[0]),(item.rect.y-12)/32,(item.rect.x-12)/32))
        if newDist <= oldDist:
          oldDist = newDist
          cord = item
    nearest = ((((cord.rect.y-12)/32),(cord.rect.x-12)/32))
    return nearest


def GetRoadCordsAroundPoint(field,x,y):
    x = int(x)
    y = int(y)
    envHight = len(field)
    envWidth = len(field[0])

    cords = []

    if x + 1 < envHight and field[x+1][y] > 0:
        cords.append((x+1,y))
    if x - 1 >= 0 and field[x-1][y] > 0:
      cords.append((x-1,y))
    if y + 1 < envWidth and field[x][y+1] > 0:
      cords.append((x,y+1))
    if y - 1 >= 0 and field[x][y-1] > 0:
      cords.append((x,y-1))

    return cords
