#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:22:03 2022

@author: ignasi cos
"""

import chess
import numpy as np
import sys


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
        self.currentStateW = self.chess.currentStateW.copy()
        self.depthMax = 4

        self.checkMatestates = ([[0, 0, 2], [2, 4, 6]], [[0, 1, 2], [2, 4, 6]], [[0, 2, 2], [2, 4, 6]], [[0, 6, 2], [2, 4, 6]], [[0, 7, 2], [2, 4, 6]])

        # In this table we will keep updating the Q value of each position and value. One will be for the white pieces and the other for the blacks
        # It will have the size of all the possible combinations
        self.tableQW = np.zeros((10000,10000,2))
        self.tableQB = []
        # Dictionary where will save all the states we visit and its associated index on Q table
        self.dictornaryW = {}
        # This variable gives us the learing rate
        self.alpha = 0.5
        # This variable will give us the discount factor
        self.gamma = 1
        # This varaible will help us determinaiting if we do exploration or exploitation, we are using the epsilon greedy technique
        self.epsilon = 0.8

    def getCurrentState(self):
    
        return self.myCurrentStateW
    
    
    def getListNextStatesW(self, myState):
    
        self.chess.boardSim.getListNextStatesW(myState)
        self.listNextStates = self.chess.boardSim.listNextStates.copy()

        return self.listNextStates


    def isVisited(self, mystate):
    
        if mystate in self.listVisitedStates:
            return True
        else:
            return False

    def isCheckMate1(self, mystate):
        if mystate in self.checkMatestates:
            return True
        mystate2 = [mystate[1], mystate[0]]
        if mystate2 in self.checkMatestates:
            return True

        return False

    # Function that given a state, turns all its data into tuples. Therefor,we will able to index it in a dictionary
    def stateToTuple(self, mystate):
        state = []
        for piece in range(0,len(mystate)):
            state.append(tuple(mystate[piece]))
        return tuple(state)

    # Function that will return us the reward of a given state, thought for the first starting case
    def getReward1(self, mystate):
        if self.isCheckMate1(mystate):
            return 100
        else:
            return 1

    # Auxiliar function that will decide if we do exploitation or exploration
    def getGreedy(self):
        # We generate a random number between 0 and 1
        num = np.random.uniform(0, 1);
        # If the generated number is smaller than our epsilon, we will do Exploitation
        if num <= self.epsilon:
            return True;
        # Else, we will explore
        else:
            return False;

    # Auxiliar function that returns you the future state with maximum Q
    def getMaximumFuture(self, futureStates, currentState, turn):

        maximum = float('-inf')
        future = None
        if currentState in self.dictornaryW:
            i_current = self.dictornaryW[currentState]
        else:
            i_current = self.dictornaryW[(currentState[1], currentState[0])]

        # If it's whites turn
        if turn:
            print('caracola')
            print(futureStates)
            for state in futureStates:
                # We create a tuple version of the state to make it easier to operate with
                tupledState = self.stateToTuple(state)

                # If we haven't seen this state yet, we add it to the table
                if tupledState not in self.dictornaryW:
                    if(tupledState[1],tupledState[0]) not in self.dictornaryW:
                        i = len(self.dictornaryW)
                        self.dictornaryW[tupledState] = i

                if tupledState in self.dictornaryW:
                    i = self.dictornaryW[tupledState]
                else:
                    i  = self.dictornaryW[(tupledState[1],tupledState[0])]

                # We get its main Q value
                if self.tableQW[i_current][i][0] > 0:
                    # We get the value of this state, considering how many times we've been on it
                    value = self.tableQW[i_current][i][1] / self.tableQW[i_current][i][0]
                else:
                    value = self.tableQW[i_current][i][1]

                if value > maximum:
                    maximum = value
                    future = state

        # If the maximum value is 0, this means none of the possible future actions have been tried before
        # Therefor, we don't have information of any. Since we don't have any preference, we will choose a random one
        if maximum == 0:
            i_future = np.random.choice(range(0,len(futureStates)))
            future = futureStates[i_future]

        return future

    # This function returns the path to solution, ussing the Q table
    def constructPath(self, currentState):
        state = currentState
        path = [state]

        while not self.isCheckMate1(state):
            max = float('-inf')

            tupledState = self.stateToTuple(state)
            stateIndex = self.dictornaryW[tupledState]
            nextState = None
            i = 0
            for action in self.tableQW[stateIndex]:
                print(':(',state)
                if action[0] > 0:
                    value = action[1] / action[0]
                else:
                    value = 0
                if value > max:
                    max = value
                    nextState = i
                i += 1
            key_list = list(self.dictornaryW.keys())
            state = key_list[nextState]
            path.append(state)

        return path

    # Q-learing function for question 1
    def Qlearing1(self,currentState):

        loss = 1
        iterations = 0
        state = currentState

        while loss > 0 or iterations < 2:

            state = currentState
            iterations += 1
            print('holaaaaa')
            print(iterations,loss)

            while not self.isCheckMate1(state):
                print('State in', state)

                # We create a tuple version of the state to make it easier to operate with
                tupledState = self.stateToTuple(state)


                # If we haven't seen this state yet, we add it to the table and initialize it
                if tupledState not in self.dictornaryW:
                    if(tupledState[1],tupledState[0]) not in self.dictornaryW:
                        i = len(self.dictornaryW)
                        self.dictornaryW[tupledState] = i

                if tupledState in self.dictornaryW:
                    i_current = self.dictornaryW[tupledState]
                else:
                    i_current  = self.dictornaryW[(tupledState[1],tupledState[0])]

                # We get the possible futre states,that will represent the possible future actions
                # from our current state
                futureStates = self.getListNextStatesW(state)
                # If the current state is on the possible ones we delate it, since it's not a possibility statying in the same place
                if state in futureStates or [state[1],state[0]] in futureStates:
                    futureStates.remove(state)

                # We get the future state that gives us the maximum Q. We first, will get the state (row in the Q table) and then its
                # maximum action(column in max row)
                # We get the best possible future state
                maximum = self.getMaximumFuture(futureStates, tupledState, True)
                tupledMaximum = self.stateToTuple(maximum)
                if tupledMaximum in self.dictornaryW:
                    i_rowMax = self.dictornaryW[tupledMaximum]
                else:
                    i_rowMax = self.dictornaryW[(tupledMaximum[1], tupledMaximum[0])]
                # We get its best action
                max = float('-inf')
                i_columnMax = 0
                i = 0
                for action in self.tableQW[i_rowMax]:
                    if action[1]/action[0] >  max:
                        max = action[1]/action[0]
                        i_columnMax = i
                    i += 1

                # We decide if we do exploitation or exploration
                greedy = self.getGreedy()

                # If exploitation
                if greedy:
                    # We do the action that has a maximum Q, considering how many times we've done this action
                    future = maximum
                    tupledFuture = self.stateToTuple(future)

                # If exploration
                else:
                    # We get a random state from the possible future ones;
                    i_future = np.random.choice(range(0, len(futureStates)))
                    future = futureStates[i_future]
                    tupledFuture = self.stateToTuple(future)

                    # If we haven't seen this state yet, we add it to the table and initialize it
                    if tupledFuture not in  self.dictornaryW:
                        if (tupledState[1], tupledState[0]) not in self.dictornaryW:
                            i = len(self.dictornaryW)
                            self.dictornaryW[tupledFuture] = i

                # We get the reward of the current state
                reward = self.getReward1(future)

                if tupledFuture in self.dictornaryW:
                    i_future = self.dictornaryW[tupledFuture]
                else:
                    i_future = self.dictornaryW[(tupledFuture[1], tupledFuture[0])]

                # We get the mistake of our prediction
                sample = reward + self.gamma * float(self.tableQW[i_rowMax][i_columnMax][1])
                loss = abs(sample - float(self.tableQW[i_current][i_future][1]))

                # We update the Q table
                self.tableQW[i_current][i_future][1] += self.alpha * sample
                self.tableQW[i_current][i_future][0] += 1

                # We update the current state
                state = future.copy()
                print(':)')

                print('State out', state)

        # Once we have updated our Q table, we reconstruct the path to the checkmate
        path = self.constructPath(currentState)
        print('Path to Check-mate: ', path)


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

    # intiialize board
    TA = np.zeros((8, 8))
    # white pieces
    TA[7][0] = 2
    TA[7][4] = 6
    # black pieces
    TA[0][4] = 12

    # initialise board
    print("stating AI chess... ")
    aichess = Aichess(TA, True)

    print("printing board")
    aichess.chess.boardSim.print_board()

    # get list of next states for current state
    print("current State",aichess.currentStateW)
    aichess.getListNextStatesW(aichess.currentStateW)
    print("list next states ",aichess.listNextStates)


    print('Q-Learning case 1');
    aichess.Qlearing1(aichess.currentStateW);
    # starting from current state find the end state (check mate) - recursive function
    aichess.chess.boardSim.listVisitedStates = []
    # find the shortest path, initial depth 0
#    depth = 0

    MovesToMake = ['1e','2e','2e','3e','3e','4d','4d','3c']

    for k in range(int(len(MovesToMake)/2)):

        print("k: ",k)

        print("start: ",MovesToMake[2*k])
        print("to: ",MovesToMake[2*k+1])

        start = translate(MovesToMake[2*k])
        to = translate(MovesToMake[2*k+1])

        print("start: ",start)
        print("to: ",to)

        aichess.chess.moveSim(start, to)


    aichess.chess.boardSim.print_board()
    print("#Move sequence...  ")

    print("#Current State...  ", aichess.chess.board.currentStateW)
