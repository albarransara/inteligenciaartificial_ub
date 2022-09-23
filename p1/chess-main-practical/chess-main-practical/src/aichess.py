#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:22:03 2022
@author: ignasi
"""

import chess
import numpy as np
import sys

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

    """
    Funció per inicialitzar un objecte de la classe aichess
        TA = matriu representant un tauler dona't
        myinit = bool que indica si li donem un tauler ja amb fitxes o crea un per defecte
    """

    def __init__(self, TA, myinit=True):

        if myinit:
            self.chess = chess.Chess(TA, True)
        else:
            self.chess = chess.Chess([], False)

        # Inicialitzem totes les variables que necessitarem
        self.listNextStates = []
        self.listVisitedStates = []
        self.pathToTarget = []
        self.queueStates = []
        self.currentStateW = self.chess.boardSim.currentStateW;
        self.depthMax = 8;
        self.checkMate = False

    def getCurrentState(self):

        return self.myCurrentStateW

    def getListNextStatesW(self, myState):

        self.chess.boardSim.getListNextStatesW(myState)
        self.listNextStates = self.chess.boardSim.listNextStates.copy()

        return self.listNextStates

    # Funció per comprovar si dos llistes d'estats son iguals
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

    # Funió per comprovar si un estat ja estat visitsat
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
        checkMatestates = (
        [[0, 0, 2], [2, 4, 6]], [[0, 1, 2], [2, 4, 6]], [[0, 2, 2], [2, 4, 6]], [[0, 3, 2], [2, 4, 6]],
        [[0, 5, 2], [2, 4, 6]], [[0, 6, 2], [2, 4, 6]], [[0, 7, 2], [2, 4, 6]])
        if mystate in checkMatestates:
            return True
        mystate2 = [mystate[1], mystate[0]]
        if mystate2 in checkMatestates:
            return True

        return False

    def DepthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW
        """
        # your code here

        if self.checkMate:
            print(currentState)
            print(self.pathToTarget)
            print("Check mate.")
            print("Depth: ", depth)

        # Comrpovem que el node ja no hagi estat visitat
        elif self.isVisited(currentState):
            # Passem al següent estat de la llista d'estats següents
            if self.queueStates:
                self.DepthFirstSearch(self.queueStates.pop(0), depth)
            # Si no hi ha més estats a visitar acabem el DFS
            else:
                print("There is no possibility of check mate.")

        else:
            # Afegim l'estat actual com a visitat
            self.listVisitedStates.append(currentState)

            # Si es check mate, imprimim un missatge i acabem la partida
            if self.isCheckMate(currentState):
                if depth < 8 :
                    depth += 1
                    self.checkMate = True
                    self.DepthFirstSearch(currentState,depth)

            # Si no es checkmate, afegim els seus estats següents, si no estan visitats, estats a la pila
            else:

                nextStates = []

                for state in reversed(self.getListNextStatesW(currentState)):
                    if state not in self.listVisitedStates:
                        if state[0][:2] != state[1][:2]:
                            nextStates.append(state)
                            self.queueStates.insert(0,state)

                if nextStates:
                    self.pathToTarget.append(currentState)
                    depth += 1
                    for state in nextStates:
                        if self.queueStates:
                            if depth < 8:
                                self.queueStates.insert(0, state)
                                self.DepthFirstSearch(self.queueStates.pop(0), depth)
                        else:
                            print(currentState)
                            print("There is no possibility of check mate.:)")

                    self.pathToTarget.remove(currentState)
                    depth -= 1
                    if self.queueStates:
                        self.DepthFirstSearch(self.queueStates.pop(0), depth)
                        # Si no hi ha més estats a visitar acabem el DFS
                    else:
                        print("There is no possibility of check mate.")

                else:
                    # Passem al següent estat de la llista d'estats següents
                    if self.queueStates:
                        self.DepthFirstSearch(self.queueStates.pop(0), depth)
                    # Si no hi ha més estats a visitar acabem el DFS
                    else:
                        print("There is no possibility of check mate.")


                """
                # Obtenim la llista de nous estats
                for state in reversed(self.getListNextStatesW(currentState)):
                    if state not in self.listVisitedStates:
                        if state[0][:2] != state[1][:2]:
                            self.queueStates.insert(0, state)

                # Apliquem la recurrencia del dfs amb el següent estat de la pila
                # Passem al següent estat de la llista d'estats següents
                if self.queueStates:
                    self.DepthFirstSearch(self.queueStates.pop(0), depth)
                # Si no hi ha més estats a visitar acabem el DFS
                else:
                    print("There is no possibility of check mate.")
                """

    def BreadthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW
        """
        # your code
        """
                Check mate from currentStateW
                """
        # your code here

        # Comrpovem que el node ja no hagi estat visitat
        if self.isVisited(currentState):
            # Passem al següent estat de la llista d'estats següents
            if self.queueStates:
                self.DepthFirstSearch(self.queueStates.pop(0), depth)
            # Si no hi ha més estats a visitar acabem el DFS
            else:
                print("There is no possibility of check mate.")

        else:
            # Afegim l'estat actual com a visitat
            self.listVisitedStates.append(currentState)

            # Si es check mate, imprimim un missatge i acabem la partida
            if self.isCheckMate(currentState):
                print("Check mate.")

            # Si no es checkmate, afegim els seus estats següents, si no estan visitats, estats a la cua
            else:
                # Obtenim la llista de nous estats
                for state in reversed(self.getListNextStatesW(currentState)):
                    if state not in self.listVisitedStates:
                        if state[0][:2] != state[1][:2]:
                            self.queueStates.append(state)

                # Apliquem la recurrencia del dfs amb el següent estat de la pila
                # Passem al següent estat de la llista d'estats següents
                if self.queueStates:
                    self.DepthFirstSearch(self.queueStates.pop(0), depth)
                # Si no hi ha més estats a visitar acabem el DFS
                else:
                    print("There is no possibility of check mate.")


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
    TA[7][0] = 2
    TA[7][4] = 6
    TA[0][4] = 12

    # initialise board
    print("stating AI chess... ")
    aichess = Aichess(TA, True)
    currentState = aichess.chess.board.currentStateW.copy()

    print("printing board")
    aichess.chess.boardSim.print_board()

    # get list of next states for current state
    print("current State", currentState)

    # it uses board to get them... careful
    aichess.getListNextStatesW(currentState)
    print("list next states ", aichess.pathToTarget)

    # starting from current state find the end state (check mate) - recursive function
    # find the shortest path, initial depth 0
    depth = 0
    aichess.DepthFirstSearch(currentState, depth)
    print(aichess.listVisitedStates[-1])
    print("DFS End")

    # starting from current state find the end state (check mate) - recursive function
    # find the shortest path, initial depth 0
    depth = 0
    aichess.BreadthFirstSearch(currentState, depth)
    print(aichess.listVisitedStates[-1])
    print("BFS End")

    # example move piece from start to end state
    MovesToMake = ['1e', '2e']
    print("start: ", MovesToMake[0])
    print("to: ", MovesToMake[1])

    start = translate(MovesToMake[0])
    to = translate(MovesToMake[1])

    print("start: ", start)
    print("to: ", to)

    aichess.chess.moveSim(start, to)

    # aichess.chess.boardSim.print_board()
    print("#Move sequence...  ", aichess.pathToTarget)
    print("#Visited sequence...  ", aichess.listVisitedStates)

    print("#Current State...  ", aichess.chess.board.currentStateW)