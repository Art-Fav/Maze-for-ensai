import random

class Maze():
  def __init__(self):
    self.moves = None
    self.state = None
    self.reward = None
    self.row = None
    self.col = None
    self.running = None

  def get_state(self):
    """
    Return:
      r list: état du jeu
    """
    return self.state
  
  def get_moves(self):
    """
    Return:
      r list: liste des coups joués
    """
    return self.moves

  def mazing(self, reward_table: dict, bonus: list, obstacles: list, pre_moves=[]):
    """
    Args:
      reward dict: dictionnaire des rewards associés à chaque case rencontrée
      bonus list: liste des positions des bonus dans le maze
      obstacles list: liste des positions des obstacles dans le maze
      pre_moves list: liste des premiers coups déjà joués
    """
    self.moves = pre_moves
    self.state = [["0" for j in range(12)] for i in range(12)]
    for row in range(12):
      for col in range(12):
        if row in [0,11] or col in [0,11] or (row,col) in obstacles:
          self.state[row][col] = "#"
        elif (row,col) in bonus:
          self.state[row][col] = "?"
        elif (row,col) in pre_moves:
          self.state[row][col] = "*"
        elif (row,col) == (1,1):
          self.state[row][col] = "*"
        elif (row,col) == (10,10):
          self.state[row][col] = "@"
    self.reward = reward_table
    if pre_moves:
      self.row, self.col = [pre_moves[-1][0],pre_moves[-1][1]]
    else:
      self.row, self.col = [1,1]
    self.running = True
    
  def help(self):
    """
    Génération de bonus aléatoire proches de la sortie pour aider l'algorithme
    """
    for i in range(random.randint(0,3)):
      row = 10-random.randint(0,3)
      col = 10-random.randint(0,3)
      if self.state[row][col] == "0":
        self.state[row][col] = "?"

  def move(self, command: str):
    """
    Args:
      command str: action à exécuter
    Return:
      reward int: reward de l'action exécutée
    """
    if command == "up":
      self.row += 1
    elif command == "down":
      self.row -= 1
    elif command == "right":
      self.col += 1
    else:
      self.col -= 1
    self.moves.append((self.row,self.col))
    pos_state = self.state[self.row][self.col]
    reward = self.reward[pos_state]
    if pos_state in ["#","@","*"]:
      self.running = False
    elif pos_state in ["0","?"]:
      self.state[self.row][self.col] = "*"
    return reward
