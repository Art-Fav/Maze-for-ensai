import random

class Q_learning_eps():
  def __init__(self):
    pass

  @staticmethod
  def initialisation():
    """
    Return:
      r dict: Q_table initialisé à l'état 0 
    """
    return {0: {"down": 0, "right": 0, "up": 0, "left": 0}}
  
  @staticmethod
  def next(Q_table: dict, state: int, epsilon=0.9):
    """
    Description:
      Choix de la prochaine action selon la méthode implémentée
    Args:
      Q_table dict: Q_table contenant les q_value pour les actions à chaque état
      state int: numéro de l'action joué
      epsilon float: paramètre pour différencié exploration et exploitation
    Return:
      command str: prochaine action déterminée par la méthode
    """
    if random.uniform(0,1) > epsilon:
      command = random.choice(list(Q_table[state].keys()))
    else:
      command = min(Q_table[state], key=Q_table[state].get)
    return command

  @staticmethod
  def update(Q_table: dict, state: int, command: str, reward: int, alpha=0.2, gamma=0.5):
    """
    Description:
      Mise à jour de la Q_table selon l'action décidée
    Args:
      Q_table dict: Q_table contenant les q_value pour les actions à chaque état
      state int: numéro de l'action joué
      command str: action déterminée par la méthode
      reward int: reward de l'action déterminée
      alpha float: paramètre déterminant l'importance des effets à court terme
      gamma float: paramètre déterminant l'importance des effets à long terme
    Return:
      Q_table dict: Q_table contenant les q_value pour les actions à chaque état mise à jour
    """
    Q_table[state+1] = Q_table.setdefault(state+1,{"down": 0, "right": 0, "up": 0, "left": 0})
    Q_table[state][command] = (1-alpha)*Q_table[state][command]+alpha*(reward+gamma*min(Q_table[state+1].values()))
    return Q_table
