import torch.nn as nn
import torch.nn.functional as F
from Utils.ConvNet import conv2DOutsize

# The Network Configuration for CIRNO

class CIRNONetwork(nn.Module):
    def __init__(self, w, h, actions):
        super(CIRNONetwork, self).__init__()

        self.conv1 = nn.Conv2d(3, 12, kernel_size=5, stride=2)
        self.bn1 = nn.BatchNorm2d(12)
        self.conv2 = nn.Conv2d(12, 32, kernel_size=5, stride=2)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32, 32, kernel_size=5, stride=2)
        self.bn3 = nn.BatchNorm2d(32)
        
        convHeight = conv2DOutsize(
          conv2DOutsize(
            conv2DOutsize(
              h, kernel_size=5, stride=2
            ), kernel_size=5, stride=2
          ), kernel_size=5, stride=2
        )

        convWidth = conv2DOutsize(
          conv2DOutsize(
            conv2DOutsize(
              w, kernel_size=5, stride=2
            ), kernel_size=5, stride=2
          ), kernel_size=5, stride=2
        )

        self.dense1 = nn.Linear(convHeight*convWidth*32, 512)
        self.dense2 = nn.Linear(512, actions)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = self.head(x.view(x.size(0), -1))
        x = F.relu(self.dense1(x))
        x = self.dense2(x)
        return x
