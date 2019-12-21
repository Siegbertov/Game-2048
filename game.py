import pygame
import numpy as np
import random
import math
from copy import deepcopy

pygame.init()
pygame.font.init()
pygame.display.set_caption('2048')
logo = pygame.image.load("2048_logo.png")
pygame.display.set_icon(logo)


def quit_game():
    pygame.quit()
    quit()