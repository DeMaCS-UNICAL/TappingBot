import os

import cv2
import mahotas
import numpy as np

from setup import RESOURCES_PATH
from src.model.CandyGraph import CandyGraph, PX, PY, ID, TYPE
from src.model.DLVClass import Node, Edge

SPRITE_PATH = os.path.join(RESOURCES_PATH, 'sprites')  # The resource folder path
SPRITES = {}


def getImg(file):
    try:
        im = cv2.imread(file)
        return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    except:
        raise Exception(f"NO {file} FOUND. \n")


for file in os.listdir(SPRITE_PATH):
    img = getImg(os.path.join(SPRITE_PATH, file))
    typeCandy = os.path.basename(file)
    SPRITES[typeCandy] = img


class MatchingCandy:
    def __init__(self, fileLocation):
        self.__matrix = getImg(fileLocation)
        self.__methodName = 'cv2.TM_CCOEFF_NORMED'
        self.__method = eval(self.__methodName)
        self.__graph = CandyGraph()

    def __searchByName(self, typeCandy) -> None:
        # execute template match
        res = cv2.matchTemplate(self.__matrix, SPRITES[typeCandy], self.__method)

        # find local maxElem
        locMax = mahotas.regmax(res)

        # modify this to change the algorithm precision
        threshold = 0.90
        loc = np.where((res * locMax) >= threshold)

        # take candy sprites value
        height, width, _ = SPRITES[typeCandy].shape
        self.__graph.setDifference((width, height))

        # add node and edge
        for pt in zip(*loc[::-1]):
            self.__graph.addNode(pt[PX], pt[PY], typeCandy)

    def search(self) -> CandyGraph:
        for typeCandy in SPRITES.keys():
            self.__searchByName(typeCandy)

        return self.__graph


def getNodes(graph: CandyGraph) -> [Node]:
    nodes = []
    for node in graph.getNodes():
        nodes.append(Node(node[ID], node[TYPE]))

    return nodes


def getEdges(self, graph: CandyGraph) -> [Edge]:
    edges = []
    for n, nbrs in self.__graph.getGraph():
        for nbr, eattr in nbrs.items():
            edges.append(Edge(n[ID], nbr[ID], graph.getPosition(n, nbr)))