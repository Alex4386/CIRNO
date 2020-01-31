import collections
import random

Transition = collections.namedtuple('Transition',
        ('state', 'action', 'next_state', 'reward'))

class ReplayMemory(object):
  def __init__(self, capacity):
    self.capacity = capacity
    self.memory = []
    self.position = 0

  def push(self, *args):
    if len(self.memory) < self.capacity:
      # if memory not full, add more memory section
      self.memory.append(None)
    self.memory[self.position] = Transition(*args)

    # next position, if memory full, then cycle back.
    self.position = (self.position + 1) % self.capacity

  def sample(self, batchSize):
    return random.sample(self.memory, batchSize)
  
  # override len
  def __len__(self):
    return len(self.memory)
