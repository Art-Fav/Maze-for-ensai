import time
import random
import matplotlib.pyplot as plt
import numpy as np

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

# Logs
logs = {"state": [], "epoch": [], "rewards": [], "actions": []}

# Tant que l'apprentissage n'est pas fini
while epoch < 10000:
    t = time.time()

    if maze.running:
        command = Q_learning_ucb.next(Q_table=Q_table
                                    , state=state
                                    , c=2)
            
        reward = maze.move(command=command)
        if reward == param.reward_table["0"]:
            reward = reward * state

        elif reward == param.reward_table["#"]:
            reward = reward * 1.5

        Q_table = Q_learning_ucb.update(Q_table=Q_table
                                    , state=state
                                    , command=command
                                    , reward=reward)      
        state += 1
        h = 50*maze.row + (maze.row+1)
        w = 50*maze.col + (maze.col+1)
    
    else:
        logs["state"].append(state)
        logs["epoch"].append(epoch)
        logs["rewards"].append(reward)
        logs["actions"].append(np.argmin(Q_table[state]["values"]))
        if epoch in [k*1000 for k in range(1, 10)]:
            print(epoch)
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

plt.hist(logs["state"])
plt.show()
