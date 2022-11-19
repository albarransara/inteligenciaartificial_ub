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
from collections import deque
from queue import PriorityQueue

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
        self.currentStateW = self.chess.boardSim.currentStateW;
        self.depthMax = 7
        self.checkMate = False
        self.checkMatestates = ([[0, 0, 2], [2, 4, 6]], [[0, 1, 2], [2, 4, 6]], [[0, 2, 2], [2, 4, 6]], [[0, 6, 2], [2, 4, 6]], [[0, 7, 2], [2, 4, 6]])

    def getCurrentState(self):

        return self.myCurrentStateW

    def getListNextStatesW(self, myState):

        self.chess.boardSim.getListNextStatesW(myState)
        self.listNextStates = self.chess.boardSim.listNextStates.copy()

        return self.listNextStates

    def getListNextStatesB(self, myState):

        self.chess.boardSim.getListNextStatesB(myState)
        self.listNextStates = self.chess.boardSim.listNextStates.copy()

        return self.listNextStates

    #ALGORISME MINIMAX
    def minimax(self, currentStateW):
        v = self.maxValue(currentStateW)
        # Return best action with value v.
        return v[0] # un cop ens quedem amb quin moviment triar, haurem de fer currentState = v[0]

    # OBTENIR EL FILL MÉS GRAN
    def maxValue(self, currentStateW):
        # si no té fills retornem el valor del node actual
        if self.checkIfLeafW(currentStateW):
            return self.utility(currentStateW)
        # inicialitzem value amb -infinit
        v = (currentStateW, float('-inf'))
        # recorrem tots els fills buscant el de valor màxim
        for state in self.getListNextStatesW(currentStateW):
            #si és més gran que el màxim que teniem, actualitzem
            if self.minValue(state) > v[1]:
                #guardem en una tupla el taulell que tenim(per després saber per on anar) i el valor
                v = (state, self.minValue(state))
        return v

    # OBTENIR EL FILL MÉS PETIT
    def minValue(self, currentStateB):
        # si no té fills retornem el valor del node actual
        if self.checkIfLeafB(currentStateB):
            return self.utility(currentStateB)
        # inicialitzem value amb infinit
        v = (currentStateB, float('inf'))
        # recorrem tots els fills buscant el de valor mínim
        for state in self.getListNextStatesB(currentStateB):
            # si és més petit que el mínim que teniem, actualitzem
            if self.maxValue(state) < v[1]:
                # guardem en una tupla el taulell que tenim(per després saber per on anar) i el valor
                v = (state, self.maxValue(state))
        return v

    # ALGORISME ALFA-BETA
    def AlfaBetaPoda(self, currentStateW):
        v = self.maxPoda(currentStateW, float('-inf'), float('inf'))
        # Return best action with value v.
        return v[0] # un cop ens quedem amb quin moviment triar, haurem de fer currentState = v[0]

    # OBTENIR EL FILL MÉS GRAN
    def maxPoda(self, currentStateW, a, b):
        # si no té fills retornem el valor del node actual
        if self.checkIfLeafW(currentStateW):
            return self.utility(currentStateW)
        # inicialitzem value amb -infinit
        v = (currentStateW, float('-inf'))
        # recorrem tots els fills buscant el de valor màxim
        for state in self.getListNextStatesW(currentStateW):
            # si és més gran que el màxim que teniem, actualitzem
            if self.minPoda(state, a, b) > v[1]:
                v = (state, self.minPoda(state, a, b))
            # si el valor que trobem és més gran o igual que Beta podem
            if v >= b:
                return v
            # Actualitzem Alfa
            a = max(a, v)
        return v

    def minPoda(self, currentStateB, a, b):
        # si no té fills retornem el valor del node actual
        if self.checkIfLeafB(currentStateB):
            return self.utility(currentStateB)
        # inicialitzem value amb infinit
        v = (currentStateB, float('inf'))
        # recorrem tots els fills buscant el de valor mínim
        for state in self.getListNextStatesW(currentStateB):
            # si és més petit que el mínim que teniem, actualitzem
            if self.minPoda(state, a, b) < v[1]:
                v = (state, self.maxPoda(state, a, b))
            # si el valor que trobem és més petit o igual que Alfa podem
            if v <= a:
                return v
            # Actualitzem Beta
            b = min(b, v)
        return v

    #Mètode per veure si és un node blanc fulla o no
    def checkIfLeafW(self, currentStateW):
        #Si no té fills retornem True, si en té retornem False
        if not self.chess.boardSim.getListNextStatesW(currentStateW):
            return True
        else:
            return False

    # Mètode per veure si és un node negre fulla o no
    def checkIfLeafB(self, currentStateB):
        # Si no té fills retornem True, si en té retornem False
        if not self.chess.boardSim.getListNextStatesB(currentStateB):
            return True
        else:
            return False

    #Mètode per assignar valors als diferents estats...
    #amenaçar torre/rei +1, matar torre sense perdre fitxa a la prox +50, matar rei + 10000 i en negatiu a l'inrevés?
    def utility(self, currentStateW):  # Funció per a assignar valors
        return 0


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
        if mystate in self.checkMatestates:
            return True
        mystate2 = [mystate[1], mystate[0]]
        if mystate2 in self.checkMatestates:
            return True

        return False

    """
    Funcio auxiliar per a reconstruir les solucions, els camins al check mate

    Parametres d'entrada:
        . currentState: estat del check-mate
        . previous: diccionari on cada key correspon a un node i cada value al seu node pare
    Return:
        . pathToTarget: llista amb la seqüència de nodes recorreguts des de´l'estat inicial fins l'estat de check-mate
    """
    def recunstructPath(self, currentState, previous):
        # Inicialitzem la llista on guardarem el recorregut  fins al checkmate
        pathToTarget = []

        # Obtenim la posicio de les peces en l'estat de checkmate
        state = (tuple(currentState[0]), tuple(currentState[1]))

        # Anem afegint estats des del checkmate fins a arribar a l'estat inicial
        while not (previous[state] == None):
            pathToTarget.insert(0, state)
            state = previous[state]
        pathToTarget.insert(0,state)
        return pathToTarget

    """
    Funció per a recorre l'arbre segons l'algoritme DFS
    
    Parametres d'entrada:
        . currentState =  node inicial
        . depth=  profunditat inicial
    """
    def DepthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW
        """

        #Inicialitzem  com a buida la llista  de nodes visitats
        self.listVisitedStates = []

        # Creem un diccionari on anirem guardant els estats i els seus estats previs, per tal de reconstruir el camí al checkmate
        previous = dict()
        previous[(tuple(currentState[0]), tuple(currentState[1]))] = None

        # Creem un diccionari on anirem guardant els estats amb el depth més baix per a arribar a aquests, l'anirem actualizant a mesura que trobem camins més curts
        costs = dict()
        costs[(tuple(currentState[0]), tuple(currentState[1]))] = depth

        """
        Funcio auxiliar a partir de la qual iterarem recursivament per l'arbre
        
        Parametres entrada:
            . currentState =  un node donat de l'arbre
            . depth = profunditat del node donat
        
        Return:
            . True si es dona situació de checkmate
            . False si no el node rebut no es checkmate
        """
        def dfs_aux(currentState,depth):

            # Afegim el node a la llista de visitats
            self.listVisitedStates.append(currentState)
            # Guradem el node amb el seu depth actual
            costs[(tuple(currentState[0]), tuple(currentState[1]))] = depth

            # Comprovem si correspon a un estat de checkmate
            if self.isCheckMate(currentState):
                # Si ho es, podem dir que hem trobat un checkmate i sortim de la recurrencia
                # Guardem la solució trobada en la variable pathToTarget
                self.pathToTarget = self.recunstructPath(currentState, previous)
                self.checkMate = True
                return True

            # Si no ens hem passat del depth màxim
            if depth < self.depthMax:
                # Obtenim la llista de nous estats possibles des del nostre estat actual
                for state in reversed(self.getListNextStatesW(currentState)):
                    # Si l'estat ha sigut visitat previament pero amb un depth superior, l'esborrarem de la llista de visitats,
                    # ja que volem considerar l'estat amb depth menor
                    if state in self.listVisitedStates:
                        if costs[(tuple(state[0]),tuple(state[1]))] > depth + 1:
                            self.listVisitedStates.remove(state)
                    # Per cada possible següent estat que no hagi estat visitat anteriorment
                    if state not in self.listVisitedStates:
                        # Si les dos peces no estan a la mateixa posició (hem trobat problemes amb això, per aquest motiu em ficat aquesta condició)
                        if state[0][:2] != state[1][:2]:
                            # Guardem els estats al diccionari amb el seu estat previ
                            previous[(tuple(state[0]), tuple(state[1]))] = (tuple(currentState[0]), tuple(currentState[1]))
                            # Cridem recursivament a la funció amb els fills del node actual
                            if dfs_aux(state,depth+1):
                                # Si un dels fills es estat de check mate, aturarem la recursió
                                return True
            return False

        #Cridem a la funció auxiliar, passant-li el node i depth inicials
        dfs_aux(currentState,depth)

        # Mostrem per pantalla els resultats obtinguts
        if self.checkMate:
            print('Check mate!')
            print("Depth: ", len(self.pathToTarget))
            print("Path: ", self.pathToTarget)

    """
        Funció per a recorre l'arbre segons l'algoritme BFS

        Parametres d'entrada:
            . currentState =  node inicial
            . depth=  profunditat inicial
    """
    def BreadthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW
        """

        #Incialitem la cua on guardarem els possibles nous estats
        queue = deque()

        #Creem un diccionari on anirem guardant els estats i els seus estats previs, per tal de reconstruir el camí al checkmate
        previous = dict()
        previous[(tuple(currentState[0]),tuple(currentState[1]))] = None

        #Guardarem el estats com a tuples, on indicarem el seu nivell dins l'arbre
        currentState = (0,currentState)

        #Abans de començar l'iteració ens assegurem que la llista de visitats està buida
        self.listVisitedStates = []

        # Mentres no trobem cap estat de check-mate, continuem iterant per l'arbre
        while not self.checkMate:

            # Comprovem que l'estat actual no hagi estat visitat previament
            if self.isVisited(currentState[1]):
                # Si hi ha més estas per visitar a la cua, passem al següent estat d'aquesta
                if queue:
                    currentState = queue.popleft()
                # Si no hi ha més nodes per visitar i cap ha sigut checkmate, podem dir que arribar a checkmate no es possible amb les peces actuals del tauler
                else:
                    print("There's no possibility of checkmate.1")
                    break

            # Si no ha estat visitat
            else:
                # Obtenim el depth i les posicions de les peces blanques(variable data)
                depth = currentState[0]
                data = currentState[1]

                 # Afegim l'estat actual a les posicions ja visitades
                self.listVisitedStates.append(data)

                # Iterem pels diferents nivells de l'arbre, sempre i quan no siguin superiors o iguals al maxim depth
                if depth <= self.depthMax:

                    # Comprovem si correspon a un estat de checkmate
                    if self.isCheckMate(data):
                        # Si ho es, podem dir que hem trobat un checkmate i sortim del bucle
                        # Guardem la solució trobada en la variable pathToTarget
                        self.pathToTarget = self.recunstructPath(data, previous)
                        self.checkMate = True

                    # Obtenim la llista de nous estats possibles
                    for state in reversed(self.getListNextStatesW(data)):
                        # Per cada possible següent estat que no hagi estat visitat anteriorment
                        if state not in self.listVisitedStates:
                            # Si les dos peces no estan a la mateixa posició (hem trobat problemes amb això, per aquest motiu em ficat aquesta condició)
                            if state[0][:2] != state[1][:2]:
                                # Afegim a la cua aquells que no hagin estat visitats previament i siguin vàlids
                                queue.append((depth+1,state))
                                # Guardem els estats al diccionari amb el seu estat previ
                                if not (tuple(state[0]),tuple(state[1])) in previous:
                                    previous[(tuple(state[0]),tuple(state[1]))] = (tuple(data[0]),tuple(data[1]))

                    # Si encara podem visitar més estats, agafem el primer de la cua
                    if queue:
                        currentState = queue.popleft()
                    # Si no hi ha més estats a visitar acabem el BFS i considerem que no hi ha possibilitat de checkmate
                    else:
                        print("There is no possibility of check mate.2")
                        break

                # Si em superat el depth màxim, considerem que no hi ha possibilitat de checkmate i acabem l'iteració
                else:
                    print("There is no possibility of check mate.3")
                    break

        # Mostrem per pantalla els resultats obtinguts
        if self.checkMate:
            print('Check mate!')
            print("Depth: ", len(self.pathToTarget))
            print("Path: ", self.pathToTarget)

    """
    Funcio heuristica per a *A
    
    Parametres d'entrada:
        . currentState: un node concret de l'arbre
    Return:
        . min: distancia mínima entre el node i un estat de check mate
    """
    def fun_heuristica(self,currentState):
        """
        Retorna el cost estimat des de l'estat donat per parámetre fins l'estat objectiu.

        Considerarem aquest cost el mínim de les distancies Manhatan de l'estat actual amb tots els possibles estats de checkmate

        """
        # La variable min ens servirà per anar gaurdant la distancia més petita trobada en cada moment.
        # L'inicialitzem a 17 ja que al tauler, al ser 8x8, mai tindrem una distància Manhatan superior a 16
        min = 17

        # Si el current state es part de les possibles posicions de check mate, retornem distancia 0
        if self.isCheckMate(currentState):
            return 0

        # Si no, trobem la distancia mínima
        for targetState in self.checkMatestates:
            for pieceT in targetState:
                for piece in currentState:
                    x = abs(piece[0] - pieceT[0]) + abs(piece[1] - pieceT[1]) # Distancia Manhatan
                    if x < min:
                        min = x

        # Retornem la distancia minima trobada
        return min


    """
        Funcio de búsqueda informada *A

        Parametres d'entrada:
            . currentState =  node inicial
            . depth=  profunditat inicial
    """
    def searchA(self, currentState, depth):

        #Inicialitzem la cua prioritaria on anirem guardant els estats
        queue = PriorityQueue()

        #Abans de començar l'iteració ens assegurem que la llista de visitats està buida
        self.listVisitedStates = []

        # Cada estat serà una tupla, on:
        #   - El primer valor serà el valor de la funció d'evaluació f(n) = h(n)+g(n)
        #   - El segón el cost d'arribar a l'objectiu des d'aquell estat, en aquest cas, equivaldrà al depth o número de moviments fets per arribar allà
        #   - El tercer serà la llista amb la posició de les peces blanques al tauler
        currentState = (self.fun_heuristica(currentState),0,currentState)

        # Creem un diccionari on anrirem guardant els estats i els seus estats previs, per tal de reconstruir el camí al checkmate
        previous = dict()
        previous[(tuple(currentState[2][0]), tuple(currentState[2][1]))] = None

        # Creem un diccionari on anirem guardant els estats amb el cost més baix per a arribar a aquests, l'anirem actualizant a mesura que trobem camins més curts
        costs = dict()
        costs[(tuple(currentState[2][0]), tuple(currentState[2][1]))] = currentState[0]

        #Mentres no trobem estat de checkmate anirem iterant per l'arbre
        while not self.checkMate:

            #Comprovem que l'estat actual no hagi estat visitat previament
            if  self.isVisited(currentState[2]):
                #Si hi ha més estat per a visitar, passem al següent de la cua amb prioritat
                if queue:
                    currentState = queue.get()
                #Si no hi ha més nodes per visitar i cap ha sigut checkmate, podem dir que arribar a checkmate no es possible amb les peces actuals del tauler
                else:
                    print("There's no possibility of checkmate.1")
                    break

            #Si no ha estat visitat
            else:
                #Obtenim el depth i les posicions de les peces blanques
                cost = currentState[0]
                depth = currentState[1]
                data = currentState[2]

                #Afegim l'estat actual a les posicions ja visitades
                self.listVisitedStates.append(data)

                #Comprovem si correspon a un estat de checkmate
                if self.isCheckMate(data):
                    #Si ho és, podem dir que hem trobat un checkmate i sortir del bucle
                    # Guardem la solució trobada en la variable pathToTarget
                    self.pathToTarget = self.recunstructPath(data, previous)
                    self.checkMate = True


                else:
                    # Obtenim la llista de nous estats possibles
                    for state in reversed(self.getListNextStatesW(data)):
                        if state not in self.listVisitedStates:
                            if state[0][:2] != state[1][:2]:
                                # Afegim a la cua aquells que no hagin estat visitats previament i siguin vàlids
                                #Primer calculem el valor de la funció d'evaluació
                                f = self.fun_heuristica(state) + depth + 1
                                queue.put((f, depth+1, state))
                                # Guradem el node amb el seu cost
                                costs[(tuple(state[0]), tuple(state[1]))] = f
                                # Guardem els estats al diccionari amb el seu estat previ
                                if not (tuple(state[0]), tuple(state[1])) in previous:
                                    previous[(tuple(state[0]), tuple(state[1]))] = (tuple(data[0]), tuple(data[1]))
                        # Si el node ja ha estat visitat
                        else:
                            # Calculem el valor de la funció d'evaluació actual
                            f = self.fun_heuristica(state) + depth + 1
                            # Si aquesta es menor que el cost de l'anterior que el vam visitar
                            if f < costs[(tuple(state[0]), tuple(state[1]))] :
                                # Actualitzem el seu cost
                                costs[(tuple(state[0]), tuple(state[1]))] = f
                                # Actualitzem també el seu node previ
                                previous[(tuple(state[0]), tuple(state[1]))] = (tuple(data[0]), tuple(data[1]))

                    # Si encara podem visitar més estats, agafem el primer de la cua de prioritat
                    if queue:
                        currentState = queue.get()

                    # Si no hi ha més estats a visitar acabem la recerca i considerem que no hi ha possibilitat de checkmate
                    else:
                        print("There is no possibility of check mate.2")
                        break

        # Mostrem per pantalla els resultats obtinguts
        if self.checkMate:
            print('Check mate!')
            print("Depth: ", len(self.pathToTarget))
            print("Path: ", self.pathToTarget)

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
    aichess.checkMate = False
    print("DFS Search")
    depth = 0
    aichess.DepthFirstSearch(currentState, depth)
    #Imprimim per pantalla el tauler resultant
    TA = np.zeros((8, 8))
    TA[0][4] = 12
    result = aichess.pathToTarget[-1]
    if result[0][2] == 2:
        TA[result[0][0]][result[0][1]] = 2
        TA[result[1][0]][result[1][1]] = 6
    else:
        TA[result[0][0]][result[0][1]] = 6
        TA[result[1][0]][result[1][1]] = 2
    aichess2 = Aichess(TA, True)
    aichess2.chess.boardSim.print_board()
    print("DFS End")

    # Per tal de trobar check mate amb BFS, tornem a posar valor False a la seva variable
    aichess.checkMate = False

    # starting from current state find the end state (check mate) - recursive function
    # find the shortest path, initial depth 0
    print("BFS Search")
    depth = 0
    aichess.BreadthFirstSearch(currentState, depth)
    print(aichess.listVisitedStates[-1])
    # Imprimim per pantalla el tauler resultant
    TA = np.zeros((8, 8))
    TA[0][4] = 12
    result = aichess.pathToTarget[-1]
    if result[0][2] == 2:
        TA[result[0][0]][result[0][1]] = 2
        TA[result[1][0]][result[1][1]] = 6
    else:
        TA[result[0][0]][result[0][1]] = 6
        TA[result[1][0]][result[1][1]] = 2
    aichess2 = Aichess(TA, True)
    aichess2.chess.boardSim.print_board()
    print("BFS End")

    aichess.checkMate = False

    print("*A Search")
    depth = 0
    aichess.searchA(currentState,depth)
    print(aichess.listVisitedStates[-1])
    # Imprimim per pantalla el tauler resultant
    TA = np.zeros((8, 8))
    TA[0][4] = 12
    result = aichess.pathToTarget[-1]
    if result[0][2] == 2:
        TA[result[0][0]][result[0][1]] = 2
        TA[result[1][0]][result[1][1]] = 6
    else:
        TA[result[0][0]][result[0][1]] = 6
        TA[result[1][0]][result[1][1]] = 2
    aichess2 = Aichess(TA, True)
    aichess2.chess.boardSim.print_board()
    print("*A End")


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
