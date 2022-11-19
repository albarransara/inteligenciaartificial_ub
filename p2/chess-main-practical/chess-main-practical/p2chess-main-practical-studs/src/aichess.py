#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:22:03 2022
@author: ignasi
"""
import copy

import chess
import numpy as np
import sys
import queue
from typing import List

RawStateType = List[List[List[int]]]

from itertools import permutations


class Aichess():
    """
    A class to represent the game of chess.
    ...
    Attributes:
    -----------
    chess : Chess
        represents the chess game
    Methods:
    --------
    startGame(pos:stup) -> None
        Promotes a pawn that has reached the other side to another, or the same, piece
    """

    def __init__(self, TA, myinit=True):

        if myinit:
            self.chess = chess.Chess(TA, True)
        else:
            self.chess = chess.Chess([], False)

        self.listNextStates = []
        self.listVisitedStates = []
        self.pathToTarget = []
        self.currentStateW = self.chess.boardSim.currentStateW;
        self.currentStateB = self.chess.boardSim.currentStateB;
        self.depthMax = 8;
        self.checkMate = False
        self.turn = True # If true White's turn, else Black's turn

    def getCurrentState(self):

        return self.myCurrentStateW

    def getListNextStatesW(self, myState):

        self.chess.boardSim.getListNextStatesW(myState.currentStateW)
        self.listNextStates = self.chess.boardSim.listNextStates.copy()

        return self.listNextStates

    def getListNextStatesB(self, myState):

        self.chess.boardSim.getListNextStatesB(myState.currentStateB)
        self.listNextStates = self.chess.boardSim.listNextStates.copy()

        return self.listNextStates

    def isSameState(self, a, b):

        isSameState1 = True
        # a and b are lists
        for k in range(len(a)):

            if a[k] not in b:
                isSameState1 = False

        isSameState2 = True
        # a and b are lists
        for k in range(len(b)):

            if b[k] not in a:
                isSameState2 = False

        isSameState = isSameState1 and isSameState2
        return isSameState

    def isVisited(self, mystate):

        if (len(self.listVisitedStates) > 0):
            perm_state = list(permutations(mystate))

            isVisited = False
            for j in range(len(perm_state)):

                for k in range(len(self.listVisitedStates)):

                    if self.isSameState(list(perm_state[j]), self.listVisitedStates[k]):
                        isVisited = True

            return isVisited
        else:
            return False

    def isCheckMate(self, mystate):
        if self.turn:
            # We get our possible next moves
            myMoves = self.getListNextStatesW(mystate);

            # We get our king's possible moves
            myKing = []
            for move in myMoves:
                for position in move:
                    if position[2] == 6 and [position[0],position[1]] not in myKing:
                        myKing.append(position[:2])

            # We check the enemies possible next moves, if any of them match with our king's possible moves
            # We will delate it from them, since it won't be no longer a possibility
            enemyMoves = self.getListNextStatesB(mystate);
            for move in enemyMoves:
                for position in move:
                    if position[:2] in myKing:
                        myKing.remove([position[0],position[1]])

            # If our king doesn't have any possible move, then, we are in a checkmate situation
            if len(myKing) == 0:
                # We need to consider if the situation is possible to be avoided by moving another of our pieces
                # First we check if we have our rook on the board
                if len(myMoves[0]) > 1:
                    # We get its possible moves
                    myRook = []
                    for move in myMoves:
                        for position in move:
                            if position[2] == 2 and [position[0], position[1]] not in myRook:
                                myRook.append(position[:2])
                    # We check if any possible move of our rook matches one of the enemies pieces position or
                    # can block the enemies tower

                    # First we get the position on the board where our rook will be blocking the other one properly
                    # This has to be the position next to our king, on the side where there's the enemies rook threat

                    #We get the position of our king and the enemies rook
                    myKing = []
                    eRook = []
                    pos = []
                    for piece in mystate.currentStateW:
                        if piece[2] == 6:
                            myKing = piece
                    for piece in mystate.currentStateB:
                        if piece[2] == 8:
                            eRook = piece

                    # If they're on the same row
                    if eRook[0] == myKing[0]:
                        #If the rook is on the right
                        if eRook[1] > myKing[1]:
                            pos = [myKing[0], myKing[1]+1]
                        # Else, it's on the left
                        else:
                            pos = [myKing[0], myKing[1]-1]
                    # If they are on the same column
                    elif eRook[1] ==  myKing[1]:
                        # If the rook is over our king
                        if eRook[0] < myKing[0]:
                            pos = [myKing[0]-1, myKing[1]]
                        # Else, the tower is over
                        else:
                            pos = [myKing[0]+1, myKing[1]]

                    # Once we have the position, we check if our tower can avoid the checkmate
                    for position in myRook:
                        if position == pos or position == [eRook[0],eRook[1]]:
                            return False

                    return True

                else:
                    return True
            # If our king still has possible movements, there is no checkmate
            else:
                return False

        
'''
    def DepthFirstSearch(self, currentState, depth):
    
        # Your Code here
 
    def BreadthFirstSearch(self, currentState):
            
        # Your Code here
    def BestFirstSearch(self, currentState):
            
        # Your Code here
                
                
                
    def AStarSearch(self, currentState):
            
        # Your Code here
        
'''

def translate(s):
    """
    Translates traditional board coordinates of chess into list indices
    """

    try:
        row = int(s[0])
        col = s[1]
        if row < 1 or row > 8:
            print(s[0] + "is not in the range from 1 - 8")
            return None
        if col < 'a' or col > 'h':
            print(s[1] + "is not in the range from a - h")
            return None
        dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        return (8 - row, dict[col])
    except:
        print(s + "is not in the format '[number][letter]'")
        return None


if __name__ == "__main__":
    #   if len(sys.argv) < 2:
    #       sys.exit(usage())

    # intiialize board
    TA = np.zeros((8, 8))
    # white pieces
    # TA[0][0] = 2
    # TA[2][4] = 6
    # # black pieces
    # TA[0][4] = 12

    # white pieces
    TA[3][7] = 2
    TA[7][4] = 6
    # black pieces
    TA[7][7] = 8
    TA[5][4] = 12

    # initialise board
    print("stating AI chess... ")
    aichess = Aichess(TA, True)
    currentState = aichess.chess.board

    print("printing board")
    aichess.chess.boardSim.print_board()

    # get list of next states for current state
    print("current State", currentState)

    # it uses board to get them... careful

    # Prova checkmate
    print("Is checkmate:",aichess.isCheckMate(currentState))

    #   aichess.getListNextStatesW([[7,4,2],[7,4,6]])
    print("list next states ", aichess.listNextStates)

    # starting from current state find the end state (check mate) - recursive function
    # aichess.chess.boardSim.listVisitedStates = []
    # find the shortest path, initial depth 0
    depth = 0
    #aichess.BreadthFirstSearch(currentState)
    #aichess.DepthFirstSearch(currentState, depth)

    # MovesToMake = ['1e','2e','2e','3e','3e','4d','4d','3c']

    # for k in range(int(len(MovesToMake)/2)):

    #     print("k: ",k)

    #     print("start: ",MovesToMake[2*k])
    #     print("to: ",MovesToMake[2*k+1])

    #     start = translate(MovesToMake[2*k])
    #     to = translate(MovesToMake[2*k+1])

    #     print("start: ",start)
    #     print("to: ",to)

    #     aichess.chess.moveSim(start, to)

    # aichess.chess.boardSim.print_board()
    print("#Move sequence...  ", aichess.pathToTarget)
    print("#Visited sequence...  ", aichess.listVisitedStates)
    print("#Current State...  ", aichess.chess.board.currentStateW)
