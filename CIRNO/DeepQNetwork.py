import math
import torch
import torch.optim as optim
import torch.nn.functional as F
from CIRNO.CIRNONetwork import CIRNONetwork
from CIRNO.ReplayMemory import ReplayMemory, Transition

#
# Deep Q Network:
# Environment change -> expectation
#
# Goal: Train a policyNetwork that have
#       most Discounted Cumulative Reward
#
# discount parameter -> makes sum converge
#
# Q function : State * Action -> expects
#              returns NextState
# 
# Goal: make neural network to approximate Q function
#  -> Q function will get action, state and will give
#     approximate results.
#
#    -> We can now use this function to have maximum
#       award because Q function can expect next state
# 

class DeepQNetwork():
    def __init__(self, screenWidth, screenHeight, batchSize, gamma, epsilonStart, epsilonEnd, epsilonDecay, targetUpdate, actions):
        
        # hyperparameters
        self.batchSize = batchSize
        self.gamma = gamma
        self.epsilonStart = epsilonStart
        self.epsilonEnd = epsilonEnd
        self.epsilonDecay = epsilonDecay
        self.targetUpdate = targetUpdate

        # save actions
        self.actions = actions

        # screen configuration
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        # device setup
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        # policy network setup
        self.policyNetwork = CIRNONetwork(screenWidth, screenHeight, actions)

        # target network setup
        self.targetNetwork = CIRNONetwork(screenWidth, screenHeight, actions)
        self.targetNetwork.load_state_dict(self.policyNetwork.state_dict())
        self.targetNetwork.eval()

        # optimizer
        self.optimizer = optim.RMSprop(self.policyNetwork.parameters())

        # replay memory
        self.memory = ReplayMemory(10000)

        # current steps
        self.currentStep = 0

        # epsilonThreshold saver
        self.epsilonThreshold = 0

        # episodeDuration
        self.episodeDuration = []

    def selectAction(self, state):

        sample = random.random()
        self.epsilonThreshold = self.epsilonEnd + \
            (self.epsilonStart - self.epsilonEnd) * \
            math.exp(-1. * self.currentStep / self.epsilonDecay)
        
        self.currentStep += 1

        if sample > epsilonThreshold:
            with torch.no_grad():
                return self.policyNetwork(state).max(1)[1].view(1,1)
        else:
            return torch.tensor([random.randrange(self.actions)], device=self.device, dtype=torch.long)

    def train(self):
        if len(self.memory) < self.batchSize:
            return
        
        # sample memory then, save to transitions -> batch
        transitions = self.memory.sample(self.batchSize)
        batch = Transition(*zip(*transitions))

        # calculate nonFinalMask

        # get tensor where s is none -> next_state
        nonFinalMask = torch.tensor(
            tuple(
                map(
                    lambda s: s is not None, batch.next_state
                )
            ),
            device=self.device,
            dtype=torch.uint8
        )
        
        # next_state when that next_state is not none
        nonFinalNextStates = torch.cat(
            [s for s in batch.next_state if s is not None]
        )
        stateBatch = torch.cat(batch.state)
        actionBatch = torch.cat(batch.action)
        rewardBatch = torch.cat(batch.reward)

        # policy Network's Q expectation Results.
        stateActionValues = self.policyNetwork(stateBatch).gather(1, actionBatch)

        # next State Actions are calculated by prev targetNetwork.
        nextStateValues = torch.zeros(self.batchSize, device=self.device)
        # get the best one.
        nextStateValues[nonFinalMask] = self.targetNetwork(nonFinalNextStates).max(1)[0].detach()

        expectedQValues = (nextStateValues * self.gamma) + rewardBatch

        loss = F.smooth_l1_loss(stateActionValues,
        expectedQValues.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()

        for parameter in self.policyNetwork.parameters():
            parameter.grad.data.clamp_(-1,1)
        
        self.optimizer.step()
        
        



