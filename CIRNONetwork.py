import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import pickle

### 
#
# # == Creating Network Optimized for CIRNO == #
#
# The CIRNO Network Requires to locate its current position.
# which means it needs eyes. but, philtabor's implementation
# was just a dense network. might be have some problems while
# testing with feature extraction.
# 
# Since Touhou Project is more visually complex than simple 
# Atari games, I would rather put ConvNet on the system.
#
###

def conv2dCalc(original, kernel_size, stride = 1, padding = 0):
  return ((original - kernel_size + (2*padding)) // stride) + 1


class CIRNO(nn.Module):
  def __init__(self, learningRate, inputDimension, subActions, actions):
    super(CIRNO, self).__init__()

    # RGB - 3 channels
    # ->
    # Machine should check:
    # is Dialogue Box is on? - should press Z to skip
    # current Bullet Location
    # my attacks
    # my Location
    # boss health bar + is in boss fight
    # is in pause menu + current Menu location
    # boss using spell cards
    # am i using spell cards
    #
    # miscellaneous, at least 10.

    self.inputDimension = inputDimension
    self.inputWidth = inputDimension[0]
    self.inputHeight = inputDimension[1]

    currentWidth = self.inputWidth
    currentHeight = self.inputHeight

    self.layer01 = nn.Conv2d(3, 9, kernel_size=8, stride=2)
    currentWidth = conv2dCalc(currentWidth, kernel_size=8, stride=2)
    currentHeight = conv2dCalc(currentHeight, kernel_size=8, stride=2)

    self.layerPool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
    currentWidth /= 2
    currentHeight /= 2

    self.layer01 = nn.Conv2d(9, 18, kernel_size=8)
    currentWidth = conv2dCalc(currentWidth, kernel_size=8)
    currentHeight = conv2dCalc(currentHeight, kernel_size=8)

    self.layer10 = nn.Linear( (currentWidth // 2) * (currentHeight // 2), 120 )

    self.layer11 = nn.Linear( 120, actions)

    self.optimizer = optim.Adam(self.parameters(), lr=learningRate)
    self.loss = nn.MSELoss()

    self.device = T.device(
      "cuda:0" if T.cuda.is_available() else "cpu:0"
    )
    self.to(self.device)
    
  def forward(self, inputData):
    currentState = T.Tensor(inputData).to(self.device).reshape(self.inputDimension)
    x = currentState

    x = F.relu(self.layer00(x))
    x = self.layerPool(x)

    x = F.relu(self.layer01(x))
    x = self.layerPool(x)

    x = x.reshape(x.size(0), -1)

    x = F.relu(self.layer10(x))
    x = self.layer11(x)


    return x


class Agent(object):
    def __init__(self, discountRate, epsilon, learningRate, inputDimension, batchSize, actions,
                 maxMemorySize=1000000, epsilonFinal=0.01, epsilonDecreaseRate=0.996):

        self.gamma = discountRate

        self.epsilon = epsilon
        self.epsilonMinimum = epsilonFinal
        self.epsilonDecreaseRate = epsilonDecreaseRate

        self.inputDimension = inputDimension
        self.learningRate = learningRate

        self.actions = actions
        self.actionSpace = [i for i in range(self.actions)]
        self.QEvaluation = CIRNO(
            learningRate, inputDimension=inputDimension, subActions=256, actions=actions)

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
            # actionValues = np.array(self.actionSpace, dtype=np.bool)
            # actionIndexes = np.dot(actionBatch, actionValues)
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

            # batchIndex = np.arange(self.batchSize, dtype=np.int32)

            targetQ[actionBatch] = rewardBatch + \
                self.gamma*T.max(nextQ, dim=1)[0]*terminalBatch

            self.epsilon = self.epsilon * \
                self.epsilonDecreaseRate if self.epsilon > self.epsilonMinimum else self.epsilonMinimum

            loss = self.QEvaluation.loss(
                targetQ, evaluationQ).to(self.QEvaluation.device)
            loss.backward()

            self.QEvaluation.optimizer.step()

    def save(self, fileLocation):
        file = open(fileLocation, "wb")
        pickle.dump(self, file)
        file.close()

    @staticmethod
    def load(fileLocation):
        file = open(fileLocation, "rb")
        tmp = pickle.load(file)
        tmp.device = T.device("cuda:0" if T.cuda.is_available() else "cpu:0")
        file.close()
        return tmp
