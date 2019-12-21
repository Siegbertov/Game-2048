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


class Metadata:
    DISPLAY_WIDTH = 600
    DISPLAY_HEIGHT = 600

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    LIGHT_GREEN = (0, 200, 0)
    COLORS = [(230, 230, 230), (250, 231, 224), (237, 224, 200), (242, 177, 121), (245, 149, 99),  # 16
              (246, 124, 95), (246, 94, 59), (250, 209, 119), (249, 208, 103), (249, 202, 88),  # 512
              (226, 184, 18), (253, 195, 48), (249, 99, 117), (241, 76, 98), (224, 70, 68),  # 16384
              (188, 143, 143), (173, 216, 230), (102, 205, 170), (0, 128, 128), (128, 128, 0),  # 524288
              (186, 85, 211), (112, 128, 144), (107, 204, 26), (255, 78, 255), (223, 214, 66)]  # 16777216
    num_font = pygame.font.SysFont('arialblack', 30)
    record_font = pygame.font.SysFont('arialblack', 200)
    options_font = pygame.font.SysFont('arialblack', 25)


class Game_2048(Metadata):
    def __init__(self, size):
        self.size = size
        self.board = np.zeros((self.size, self.size))
        self.ceil_width = self.DISPLAY_WIDTH // self.size
        self.add_new_num_in_random_position()
        self.SCREEN = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.run = True
        self.show_record = False