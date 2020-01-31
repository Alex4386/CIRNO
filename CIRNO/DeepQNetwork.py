import torch
from CIRNO.CIRNONetwork import CIRNONetwork

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

        
