import time

import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from maze import Maze
from Q_learning import Q_learning

import parametrage as param

# Initialisation du jeu
maze = Maze()
maze.mazing(reward_table=param.reward_table
            , obstacles=param.obstacles
            , bonus=param.bonus)

# Initialisation de la Q_table
Q_table = Q_learning.initialisation()

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
        command = Q_learning.next(Q_table=Q_table
                                    , state=state
                                    , epsilon=0.9)
        reward = maze.move(command=command)
        Q_table = Q_learning.update(Q_table=Q_table
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
        maze.mazing(reward_table=param.reward_table
                    , obstacles=param.obstacles
                    , bonus=param.bonus)
        epoch += 1
        state = 0
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

