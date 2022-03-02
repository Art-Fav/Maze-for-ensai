import numpy as np

class Game():
  def __init__(self):
    self.state = None
    self.range = [i for i in range(10)]
    self.reward = None
    self.pos = None
    self.over = None

  def get_state(self):
    return self.state

  def get_reward(self):
    if self.pos[0] in self.range and self.pos[1] in self.range :
      pos_state = self.state[self.pos]
      self.over = True if pos_state in [1,3,5] else False
      self.state[self.pos] = 1 if pos_state == 0 else pos_state
    else:
      pos_state = 5
      self.over = True
    return self.reward[pos_state]

  def new(self,reward_table,bonus,obstacles):
    self.state = np.zeros(shape=(10,10))
    self.reward = reward_table
    self.pos = (0,0)
    self.state[(0,0)], self.state[(9,9)] = [1,1]
    for pos in bonus:
      self.state[pos] = 3
    for pos in obstacles:
      self.state[pos] = 5
    self.over = False

  def move(self, command):
    if command == "up":
      self.pos[0] += 1
    elif command == "down":
      self.pos[0] -= 1
    elif command == "right":
      self.pos[1] += 1
    else:
      self.pos[1] -= 1