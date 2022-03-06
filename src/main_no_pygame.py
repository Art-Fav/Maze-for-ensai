from math import gamma
import time
import random
import matplotlib.pyplot as plt
import numpy as np
import datetime
import logging

import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from game.maze import Maze
from learning.Q_learning_ucb import Q_learning_ucb

import parametrage as param

# Initialisation du jeu
maze = Maze()
maze.mazing(reward_table=param.reward_table
            , obstacles=param.obstacles
            , bonus=param.bonus)

# Initialisation de la Q_table
Q_table = Q_learning_ucb.initialisation()

# Paramètres d'affichage
color_table = param.color_table

# Initialize pygame
# pygame.init()

# Epoque et état de l'apprentissage
epoch = 0
state = 0
arrived = False
alpha = 0.3
gamma_ = 0.7
c = 5
method = "UCB"

# Logs
logs = {"state": [], "epoch": [], "rewards": [], "actions": [], "arrived": []}
logs_to_log = { "param": {"c": c, "alpha": alpha, "gamma": gamma_}}

# Tant que l'apprentissage n'est pas fini
while epoch < 10000:
    t = time.time()

    if maze.running:
        command = Q_learning_ucb.next(Q_table=Q_table
                                    , state=state
                                    , c=c)
            
        reward = maze.move(command=command)
        if reward == param.reward_table["0"]:
            reward = reward * 5 * state
            logs_to_log["param"]["0"] = "reward * 5 * state"
        elif reward == param.reward_table["#"]:
            reward = reward * 5
            logs_to_log["param"]["#"] = "reward * 5"
        elif reward == param.reward_table["*"]:
            reward = reward * 5
            logs_to_log["param"]["*"] = "reward * 5"
        elif reward == param.reward_table["@"]:
            arrived = True

        Q_table = Q_learning_ucb.update(Q_table=Q_table
                                    , state=state
                                    , command=command
                                    , reward=reward
                                    , alpha=alpha
                                    , gamma=gamma_)      
        state += 1
        h = 50*maze.row + (maze.row+1)
        w = 50*maze.col + (maze.col+1)
    
    else:
        logs["state"].append(state)
        logs["epoch"].append(epoch)
        logs["rewards"].append(reward)
        logs["actions"].append(np.argmin(Q_table[state]["values"]))
        if epoch in [k * 1000 for k in range(1, 10)]:
            print("Epoch : {}".format(epoch))
        if arrived:
            logs["arrived"].append(epoch)
        moves = maze.get_moves()
        keep = random.randint(0, len(moves)-1)
        moves = moves[:keep]
        state = keep
        maze.mazing(reward_table=param.reward_table
                    , obstacles=param.obstacles
                    , bonus=param.bonus
                    , pre_moves=moves)
        epoch += 1
        maze.help()
        mat = maze.get_state()

logs_to_log["arrived"] = len(logs["arrived"])

logging.basicConfig(filename="logs/logs.log", level=logging.INFO)
logging.info(str(datetime.datetime.now()) + " - methode :" + method + "\n logs : " + str(logs_to_log))

if logs["arrived"]:
    print("L'algo à terminé {} fois.".format(len(logs["arrived"])))
    epoch_arrived = []
    for i, x in enumerate(logs["arrived"]):
        break
        if x:
            pass
else:
    print("L'algo n'a pas trouvé de chemin.")
#print(logs["arrived"])

"""plt.figure("state")
plt.hist(logs["state"], label="longeur des chemins par nombre d'itérations")
#plt.figure("rewards")
# plt.plot("nombre d'itérations", "valeur des récompenses", data=logs["rewards"])
plt.show()"""