import csv
import numpy as np
import pygame
from Agent import Agent
from game import Game, WHITE
from maxalgs import FindNearestPoint
from objects import Ellipse

ACTIONS = 4 # Number of Actions.  Acton istelf is a scalar: 0:Up, 1:Down,2:right,3:down
STATECOUNT = 6 # Size of State [ PlayerXPos, PlayerYPos, GhostXpoz, GhostYpoz, FoodCordsX, FoodCordsY]
GAME_Cycles = 2000

testGrid =      ((1,1,1,1,1,),
                 (1,0,0,0,1,),
                 (1,1,1,1,1,),
                 (1,0,0,0,1,),
                 (1,1,1,1,1,))

testGridWithItems =      ((5,5,5,5,5,),
                 (5,0,0,0,5,),
                 (5,5,4,5,5,),
                 (5,0,0,0,5,),
                 (5,5,2,5,5,))

def CaptureNormalisedState(PlayerXPos, PlayerYPos, GhostXpoz, GhostYpoz, NearestFoodX,NearestFoodY):
    gstate = np.zeros([STATECOUNT])
    gstate[0] = PlayerXPos / 10.0
    gstate[1] = PlayerYPos / 10.0
    gstate[2] = GhostXpoz / 10.0
    gstate[3] = GhostYpoz / 10.0
    gstate[4] = NearestFoodX / 10.0
    gstate[5] = NearestFoodY / 10.0
    return gstate

SCREENWIDTH = 160
SCREENHEIGHT = 160

# Main Experiment Method
def PlayExperiment():
    GameTime = 0
    GameHistory = []

    #  Create our Agent (including DQN based Brain)
    TheAgent = Agent(STATECOUNT, ACTIONS)

    # 0:Up, 1:Down,2:right,3:down
    BestAction = 0
    dotsGroup = pygame.sprite.Group()

    for i, row in enumerate(testGridWithItems):
        for j, item in enumerate(row):
            if item == 5:
                dotsGroup.add(Ellipse(j * 32 + 12, i * 32 + 12, WHITE, 8, 8))

    nearestFood = FindNearestPoint([2, 4],dotsGroup)
    #[ PlayerXPos, PlayerYPos, GhostXpoz, GhostYpoz, nearestFoodX, nearestFoodY]
    GameState = CaptureNormalisedState(2, 4, 2, 2,nearestFood[0],nearestFood[1])
    globalScore = 0

    for gtime in range(GAME_Cycles):
        pygame.init()
        screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption("PACMAN")
        # fps variable
        clock = pygame.time.Clock()

        # done game variable
        done = False
        # Create a game object
        game = Game()
        game.__init__()
        game.gameOver = False
        # game
        while not done:
            # input handler
            done = game.inputHandler()

            canToMove = not game.player.isGoingByGame
            if(canToMove):
                BestAction = TheAgent.Act(GameState)
                [ReturnScore, PlayerXPos, PlayerYPos, nearestEnemy, nearestFood] = game.PlayNextMove(BestAction)
                globalScore += ReturnScore

                NextState = CaptureNormalisedState(PlayerXPos, PlayerYPos, nearestEnemy[0], nearestEnemy[1], nearestFood[0],nearestFood[1])

                #  S, A, R, S_
                TheAgent.CaptureSample((GameState, BestAction, globalScore, NextState))
                TheAgent.Process()
                GameState = NextState

                print(f"ReturnScore: {globalScore} EPSILON:  {TheAgent.epsilon}")

                with open('trainingHistory.csv', 'a', encoding='UTF8') as file:
                    data = ["score: ",globalScore,"epsilon: ", TheAgent.epsilon]
                    writer = csv.writer(file)
                    writer.writerow(data)
            if(game.gameOver and game.isWin):
                globalScore+=400
            elif(game.gameOver and not game.isWin):
                globalScore -= 100

            game.logic()
            # draw frame
            game.displayFrame(screen)
            # 30 frames per second
            clock.tick(3000)

PlayExperiment()