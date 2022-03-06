import time
import random

import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

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
maze.help()
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
        pygame.display.flip()

# Epoque et état de l'apprentissage
epoch = 0
state = 0

# Tant que l'apprentissage n'est pas fini
while epoch < 10000:
    t = time.time()
    
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    if maze.running:
        command = Q_learning_eps.next(Q_table=Q_table
                                    , state=state
                                    , epsilon=1-0.1)
        reward = maze.move(command=command)
        Q_table = Q_learning_eps.update(Q_table=Q_table
                                    , state=state
                                    , command=command
                                    , reward=reward)      
        state += 1
        h = 50*maze.row + (maze.row+1)
        w = 50*maze.col + (maze.col+1)
        color = color_table[mat[maze.row][maze.col]]
        surf = pygame.Surface((50, 50))
        surf.fill(color)
        rect = surf.get_rect()
        screen.blit(surf, (w,h))
        pygame.display.flip()

    else:
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
        
        for i in range(12):
            for j in range(12):
                h = 50*i + (i+1)
                w = 50*j + (j+1)
                color = color_table[mat[i][j]]
                surf = pygame.Surface((50, 50))
                surf.fill(color)
                rect = surf.get_rect()
                screen.blit(surf, (w,h))
                pygame.display.flip()
                
    while time.time()-t < 0.02:
        pass
