import random
import numpy as np
from math import sqrt, log

class Q_learning_ucb():
  def __init__(self):
    pass

  @staticmethod
  def initialisation():
    """
    Return:
      r dict: Q_table initialisé à l'état 0 
    """
    return {
        0: {
            "values": np.zeros(4),
            "nb_trials": np.zeros(4)
        }
    }
    
  @staticmethod
  def next(Q_table: dict, state: int, c=2):
    """
    Description:
      Choix de la prochaine action selon la méthode implémentée
    Args:
      Q_table dict: Q_table contenant les q_value pour les actions à chaque état
      state int: numéro de l'action joué
      c float: paramètre de la sélection selon ucb
    Return:
      command str: prochaine action déterminée par la méthode
    """
    tot = int(np.sum(Q_table[state]["nb_trials"]))
    if 0 in Q_table[state]["nb_trials"]:
        i_command = tot
    else:
        vect = [c*sqrt(log(tot)/n) for n in Q_table[state]["nb_trials"]]
        i_command = np.argmin(Q_table[state]["values"] - np.array(vect))
    if i_command == 0:
        return "down"
    elif i_command == 1:
        return "right"
    elif i_command == 2:
        return "up"
    else:
        return "left"

  @staticmethod
  def update(Q_table: dict, state: int, command: str, reward: int, alpha=0.3, gamma=0.7):
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
    if command == "down":
        i_command = 0
    elif command == "right":
        i_command = 1
    elif command == "up":
        i_command = 2
    else:
        i_command = 3
    Q_table[state+1] = Q_table.setdefault(state+1,{"values": np.zeros(4),"nb_trials": np.zeros(4)})
    Q_table[state]["nb_trials"][i_command] += 1
    Q_table[state]["values"][i_command] = (1-alpha)*Q_table[state]["values"][i_command]+alpha*(reward+gamma*np.min(Q_table[state+1]["values"]))
    return Q_table
