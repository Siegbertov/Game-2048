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

    def board_has_at_least_one_zero(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return True
        return False

    # TODO                                            CREATING RANDOM NUM
    def all_free_ceils_with_zero(self):
        free_ceils = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    free_ceils.append([r, c])
        return free_ceils

    def add_new_num_in_random_position(self):
        if self.board_has_at_least_one_zero():
            all_possible_position = self.all_free_ceils_with_zero()
            rand_pos = random.choice(all_possible_position)
            r, c = rand_pos[0], rand_pos[1]
            self.board[r][c] = 2

    # TODO                                             DRAWING WINDOW
    def draw_border(self):
        pygame.draw.rect(self.SCREEN, self.BLACK, (0, 0, self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT), 4)

    def draw_table(self):
        self.draw_border()
        for i in range(1, self.size):
            pygame.draw.line(self.SCREEN, self.BLACK, (0 , i * self.ceil_width ), (self.DISPLAY_WIDTH, i * self.ceil_width), 4)
            pygame.draw.line(self.SCREEN, self.BLACK, (i * self.ceil_width,0), (i * self.ceil_width,self.DISPLAY_HEIGHT), 4)

    def draw_blur_ceil(self):
        for r in range(self.size):
            for c in range(self.size):
                num = int(self.board[r][c])
                s = pygame.Surface((self.ceil_width, self.ceil_width))
                s.set_alpha(220)
                if num == 0:
                    s.fill(self.COLORS[num])
                    self.SCREEN.blit(s, (r * self.ceil_width, c * self.ceil_width))
                else:
                    col_pos = int(math.log2(num))
                    s.fill(self.COLORS[col_pos])
                    self.SCREEN.blit(s, (r * self.ceil_width, c * self.ceil_width))

    def draw_numbers(self):
        for r in range(self.size):
            for c in range(self.size):
                num = int(self.board[r][c])
                if num != 0:
                    text_surface = self.num_font.render(str(num), True, self.BLACK)
                    text_rect = text_surface.get_rect()
                    text_rect.center = (r * self.ceil_width + self.ceil_width//2, c * self.ceil_width + self.ceil_width//2)
                    self.SCREEN.blit(text_surface, text_rect)

    def redraw_screen(self):
        self.SCREEN.fill(self.WHITE)
        self.draw_blur_ceil()
        self.draw_numbers()
        self.draw_table()
        if not self.possible_to_make_any_move():
            self.show_score()
            
    #  TODO                                                    METHODS for MOVING
    @staticmethod
    def delete_zeros_in_array(arr):
        result = []
        for element in arr:
            if element != 0:
                result.append(element)
        return result

    @staticmethod
    def moving_elements(arr):
        result = []
        pos = 0
        while pos < len(arr) - 1:
            left = arr[pos]
            right = arr[pos + 1]
            if left == right:
                result.append(left + right)
                pos += 1
            elif left != right:
                result.append(left)
            pos += 1

        nums = Game_2048.last_elem_repeat(arr)

        if nums % 2 != 0:
            result.append(arr[-1])

        return result

    @staticmethod
    def last_elem_repeat(some_array):
        last_result = some_array[-1]
        nums = 0
        length_arr = len(some_array)
        for i in range(length_arr):
            pos = length_arr - i - 1
            if some_array[pos] == last_result:
                nums += 1
            else:
                break
        return nums

    @staticmethod
    def return_zeros_to_array(arr, num):
        num -= len(arr)
        for i in range(num):
            arr.append(0)
        return arr

    @staticmethod
    def combined_function(your_array):
        length_of_your_array = len(your_array)
        no_zero_array = Game_2048.delete_zeros_in_array(your_array)
        if not no_zero_array:
            return your_array
        else:
            moved_array = Game_2048.moving_elements(no_zero_array)
            return_zeros_array = Game_2048.return_zeros_to_array(moved_array, length_of_your_array)
            return return_zeros_array