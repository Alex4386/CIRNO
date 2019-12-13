import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import pickle

# Create DQN Module

# Deep Q Network Implementation By:
# https://github.com/philtabor/Youtube-Code-Repository/blob/master/ReinforcementLearning/DeepQLearning/simple_dqn_torch.py
#
# Code Manipulated by Alex4386, for easier understanding: of course, for me.


class DeepQNetwork(nn.Module):
    def __init__(self, learningRate, inputDimension, func1Dimension, func2Dimension, actions):
        super(DeepQNetwork, self).__init__()
        self.inputDimension = inputDimension
        self.func1Dimension = func1Dimension
        self.func2Dimension = func2Dimension
        self.actions = actions

        # Layer1 input -> func1Dimension
        self.layer1 = nn.Linear(*self.inputDimension, self.func1Dimension)

        # Layer2 func1Dimensions -> func2Dimension
        self.layer2 = nn.Linear(self.func1Dimension, self.func2Dimension)

        # Layer3 func1Dimensions -> func2Dimension
        self.layer3 = nn.Linear(self.func2Dimension, self.actions)

        self.optimizer = optim.Adam(self.parameters(), lr=learningRate)
        self.loss = nn.MSELoss()

        # pylint: disable=no-member
        self.device = T.device(
            "cuda:0" if T.cuda.is_available() else "cpu:0")
        self.to(self.device)

    def forward(self, observedData):
        # Just a simple known bug by PyTorch, move on.

        state = T.Tensor(observedData).to(self.device)
        x = F.relu(self.layer1(state))
        x = F.relu(self.layer2(x))
        x = self.layer3(x)

        return x


class Agent(object):
    def __init__(self, discountRate, epsilon, learningRate, inputDimension, batchSize, actions,
                 maxMemorySize=1000000, epsilonFinal=0.99, epsilonDecreaseRate=0.996):

        self.gamma = discountRate

        self.epsilon = epsilon
        self.epsilonMinimum = epsilonFinal
        self.epsilonDecreaseRate = epsilonDecreaseRate

        self.inputDimension = inputDimension
        self.learningRate = learningRate

        self.actions = actions
        self.actionSpace = [i for i in range(self.actions)]
        self.QEvaluation = DeepQNetwork(
            learningRate, inputDimension=inputDimension, func1Dimension=256, func2Dimension=256, actions=actions)

        self.memorySize = maxMemorySize
        self.currentStateMemory = np.zeros((self.memorySize, *inputDimension))
        self.newStateMemory = np.zeros((self.memorySize, *inputDimension))
        self.actionMemory = np.zeros(
            (self.memorySize, self.actions), dtype=np.bool)
        self.rewardMemory = np.zeros(self.memorySize)
        self.terminalMemory = np.zeros(self.memorySize, dtype=np.bool)

        self.currentLearningIteration = 0

        self.batchSize = batchSize

    def storeTransition(self, state, action, reward, newState, terminal):
        # get Memory Index via update counter calls
        index = self.currentLearningIteration % self.memorySize

        self.currentStateMemory[index] = state
        actions = np.zeros(self.actions)
        actions[action] = 1.0

        # save to data
        self.actionMemory[index] = actions
        self.rewardMemory[index] = reward
        self.terminalMemory[index] = 1 - terminal
        self.newStateMemory[index] = newState

        self.currentLearningIteration += 1

    def decideAction(self, observedData):
        # pylint: disable=no-member
        rand = np.random.random()

        # if network doesn't know well, = high epsilon value
        # choose random
        if rand < self.epsilon:
            action = np.random.choice(self.actionSpace)
        else:
            actions = self.QEvaluation.forward(observedData)
            action = T.argmax(actions).item()
        return action

    def learn(self):
        if self.currentLearningIteration > self.batchSize:
            self.QEvaluation.optimizer.zero_grad()

            maximumMemory = self.currentLearningIteration if self.currentLearningIteration < self.memorySize else self.memorySize

            batch = np.random.choice(maximumMemory, self.batchSize)

            stateBatch = self.currentStateMemory[batch]
            actionBatch = self.actionMemory[batch]
            actionValues = np.array(self.actionSpace, dtype=np.bool)
            actionIndexes = np.dot(actionBatch, actionValues)
            rewardBatch = self.rewardMemory[batch]
            terminalBatch = self.terminalMemory[batch]
            newStateBatch = self.newStateMemory[batch]

            rewardBatch = T.Tensor(rewardBatch).to(self.QEvaluation.device)
            terminalBatch = T.Tensor(terminalBatch).to(self.QEvaluation.device)

            evaluationQ = self.QEvaluation.forward(
                stateBatch).to(self.QEvaluation.device)
            targetQ = evaluationQ.clone()
            nextQ = self.QEvaluation.forward(
                newStateBatch).to(self.QEvaluation.device)

            batchIndex = np.arange(self.batchSize, dtype=np.int32)

            targetQ[actionBatch] = rewardBatch + \
                self.gamma*T.max(nextQ, dim=1)[0]*terminalBatch

            self.epsilon = self.epsilon * \
                self.epsilonDecreaseRate if self.epsilon > self.epsilonMinimum else self.epsilonMinimum

            loss = self.QEvaluation.loss(
                targetQ, evaluationQ).to(self.QEvaluation.device)
            loss.backward()

            self.QEvaluation.optimizer.step()

    def dumpMe(self, file):
        pickle.dump(self, file)

    @staticmethod
    def load(file):
        tmp = pickle.load(file)
        tmp.device = T.device("cuda:0" if T.cuda.is_available() else "cpu:0")
