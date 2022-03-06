from math import gamma
import time
import random
import datetime
import logging

"""import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)"""

from game.maze import Maze
from learning.Q_learning_eps import Q_learning_eps

import parametrage as param

# Initialisation du jeu
maze = Maze()
maze.mazing(reward_table=param.reward_table
            , obstacles=param.obstacles
            , bonus=param.bonus)

# Initialisation de la Q_table
Q_table = Q_learning_eps.initialisation()
"""
# Paramètres d'affichage
color_table = param.color_table

# Initialize pygame
pygame.init()

# Taille de l'affichage
SCREEN_WIDTH = 613
SCREEN_HEIGHT = 613

# Création de l'affichage
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Fond noir
screen.fill((0, 0, 0))

# Affichage du jeu
# maze.help()
mat = maze.get_state()
for i in range(12):
    for j in range(12):
        h = 50*i + (i+1)
        w = 50*j + (j+1)
        color = color_table[mat[i][j]]
        surf = pygame.Surface((50, 50))
        surf.fill(color)
        rect = surf.get_rect()
        screen.blit(surf, (w,h))
        pygame.display.flip()"""

# Epoque et état de l'apprentissage
epoch = 0
state = 0
epsilon = 1 - 0.2 / (1 + epoch / 100)
alpha = 0.3
gamma_ = 0.7
method = "Epsilon greedy"

arrived = False

# Logs
logs_to_log = { "param": {"alpha": alpha, "gamma": gamma_}, "arrived": []}

# Tant que l'apprentissage n'est pas fini
while epoch < 10000:
    t = time.time()
    
    """for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False"""

    if maze.running:
        command = Q_learning_eps.next(Q_table=Q_table
                                    , state=state
                                    , epsilon=epsilon)
        reward = maze.move(command=command)

        if reward == param.reward_table["0"]:
            reward = reward * (state + 1)
            logs_to_log["param"]["0"] = "reward * 5 * state"
        
        elif reward == param.reward_table["@"]:
            arrived = True

        Q_table = Q_learning_eps.update(Q_table=Q_table
                                    , state=state
                                    , command=command
                                    , reward=reward
                                    , alpha=alpha
                                    , gamma=gamma_)      
        state += 1
        h = 50*maze.row + (maze.row+1)
        w = 50*maze.col + (maze.col+1)
        """color = color_table[mat[maze.row][maze.col]]
        surf = pygame.Surface((50, 50))
        surf.fill(color)
        rect = surf.get_rect()
        screen.blit(surf, (w,h))
        pygame.display.flip()"""

    else:
        if arrived:
            logs_to_log["arrived"].append(epoch)
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
        
        """for i in range(12):
            for j in range(12):
                h = 50*i + (i+1)
                w = 50*j + (j+1)
                color = color_table[mat[i][j]]
                surf = pygame.Surface((50, 50))
                surf.fill(color)
                rect = surf.get_rect()
                screen.blit(surf, (w,h))
                pygame.display.flip()"""

    while time.time()-t < 0.000000000000000002:
        pass

logs_to_log["arrived"] = len(logs_to_log["arrived"])

logging.basicConfig(filename="logs/logs.log", level=logging.INFO)
logging.info(str(datetime.datetime.now()) + " - methode :" + method + "\n logs : " + str(logs_to_log))
