# Default Imports

import torch
import torch.nn as nn
import torch.nn.functional as F


# Creating a Model
class SampleModel(nn.Module):
  def __init__(self):
    super(self, SampleModel).__init__()

    inputSize = 256
    self.layer0 = nn.Linear(inputSize, 128)
    self.layer1 = nn.Linear(128, 24)
    self.layer2 = nn.Linear(24, 9)

  def forward(self, x):
    x = F.relu(self.layer0(x))
    x = F.relu(self.layer1(x))
    x = F.softmax(self.layer2(x))

    return x

    
