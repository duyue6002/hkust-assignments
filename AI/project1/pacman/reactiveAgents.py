# reactiveAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from game import Directions
from game import Agent
from game import Actions
import util
import time
import search
import pandas as pd
import numpy as np
import os


class NaiveAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        sense = state.getPacmanSensor()
        if sense[7]:
            return Directions.STOP
        else:
            return Directions.WEST


class PSAgent(Agent):
    "An agent that follows the boundary using production system."

    def getAction(self, state):
        ''' Your code goes here! '''
        sense = state.getPacmanSensor()
        x = [0, 0, 0, 0]
        x[0] = sense[1] or sense[2]
        x[1] = sense[3] or sense[4]
        x[2] = sense[5] or sense[6]
        x[3] = sense[0] or sense[7]
        toNorth = x[3] and (not x[0]) or (
            not x[0] and not x[1] and not x[2] and not x[3])
        toEast = x[0] and (not x[1])
        toSouth = x[1] and (not x[2])
        toWest = x[2] and (not x[3])
        if toNorth:
            return Directions.NORTH
        elif toSouth:
            return Directions.SOUTH
        elif toEast:
            return Directions.EAST
        elif toWest:
            return Directions.WEST
        else:
            return Directions.STOP


class ECAgent(Agent):
    "An agent that follows the boundary using error-correction."

    def __init__(self):
        self.north_perceptron = self.generatePerceptron('north')
        self.east_perceptron = self.generatePerceptron('east')
        self.south_perceptron = self.generatePerceptron('south')
        self.west_perceptron = self.generatePerceptron('west')

    def generatePerceptron(self, ptype):
        script_dir = os.path.dirname(__file__)
        file_name = '../' + ptype + '.csv'
        file_path = os.path.join(script_dir, file_name)
        df = pd.read_csv(file_path, header=None)
        data = np.array(df.iloc[:, :])
        X_train, D_train = data[:, :-1], data[:, -1]
        perceptron = Model(data)
        perceptron.error_correction(X_train, D_train)
        return perceptron

    def getAction(self, state):
        ''' Your code goes here! '''
        sense = state.getPacmanSensor()
        if self.north_perceptron.score(sense) == 1:
            return Directions.NORTH
        elif self.east_perceptron.score(sense) == 1:
            return Directions.EAST
        elif self.south_perceptron.score(sense) == 1:
            return Directions.SOUTH
        elif self.west_perceptron.score(sense) == 1:
            return Directions.WEST
        else:
            return Directions.NORTH


class Model:
    def __init__(self, data):
        self.w = np.zeros(len(data[0])-1, dtype=np.float32)
        self.theta = 0
        self.rate = 0.1

    def error_correction(self, X_train, D_train):
        flag = False
        while not flag:
            wrong_count = 0
            for i in range(len(X_train)):
                x = X_train[i]
                d = D_train[i]
                output = 1 if (np.dot(x, self.w) >= self.theta) else 0
                if d != output:
                    self.w = self.w + self.rate*np.dot(d - output, x)
                    self.theta = self.theta + self.rate*(output - d)
                    wrong_count += 1
            if wrong_count == 0:
                flag = True

    def score(self, x_test):
        return 1 if (np.dot(x_test, self.w) >= self.theta) else 0
