import pygame

from maze import Maze
from Q_learning import Q_learning

import parametrage as param

maze = Maze()
maze.mazing(reward_table=param.reward_table
            , obstacles=param.obstacles
            , bonus=param.bonus)

Q_table = Q_learning.initialisation()

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 613
SCREEN_HEIGHT = 613

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Fill the screen with white
screen.fill((0, 0, 0))

# Variable to keep the main loop running
epoch = 0
state = 0

# Main loop
while epoch < 1000:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    # Affichage du jeu
    color_table = param.color_table
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

    if maze.running:
        command = Q_learning.next(Q_table=Q_table
                                    , state=state)
        reward = maze.move(command=command)
        Q_table = Q_learning.update(Q_table=Q_table
                                    , state=state
                                    , command=command
                                    , reward=reward)      
        state += 1

    else:
        maze.mazing(reward_table=param.reward_table
                    , obstacles=param.obstacles
                    , bonus=param.bonus)
        epoch += 1
        state = 0
