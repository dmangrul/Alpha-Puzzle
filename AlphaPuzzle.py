from random import randint
import pygame
from pygame.locals import *

# initialize pygame module
pygame.init()

# window properties
display_res = (600, 700)
display_surface = pygame.display.set_mode(display_res)
pygame.display.set_caption("Slide Puzzle")

# fonts used for texts
font = pygame.font.SysFont("Kid Games", 80)
font_small = pygame.font.SysFont("Kid Games", 40)
font_smaller = pygame.font.SysFont("Kid Games", 20)

# set events allowed for window
pygame.event.set_allowed(KEYDOWN)  # all keys
pygame.event.set_allowed(QUIT)

# colors for background and text
gray = pygame.Color(195, 195, 195)
bg_color = pygame.Color(124, 179, 128)


class Puzzle:
    box_pos = ['A', 'B', 'C',  # indices 0, 1, 2
               'D', 'E', 'F',  # indices 3, 4, 5
               'G', 'H', ' ']  # indices 6, 7, 8

    # blank side position is at index 8
    blank_pos = 8

    # number of moves
    moves = 0

    def button_pressed(self, swap_pos):
        if (swap_pos == -3 and self.blank_pos in [0, 1, 2]) or (swap_pos == 3 and self.blank_pos in [6, 7, 8]) or (
                swap_pos == -1 and self.blank_pos in [0, 3, 6]) or (swap_pos == 1 and self.blank_pos in [2, 5, 8]):
            return 0

        temp = self.box_pos[self.blank_pos]
        self.box_pos[self.blank_pos] = self.box_pos[self.blank_pos + swap_pos]
        self.box_pos[self.blank_pos + swap_pos] = temp
        self.blank_pos += swap_pos
        self.moves += 1
        return 1

    def shuffle(self):
        i = 100
        while i:
            x = randint(1, 4)
            if x == 1:
                i -= self.button_pressed(1)
            elif x == 2:
                i -= self.button_pressed(-1)
            elif x == 2:
                i -= self.button_pressed(3)
            else:
                i -= self.button_pressed(-3)
        self.moves = 0

    def check_state(self):
        if self.box_pos == ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', ' ']:
            return True
        return False

    def get_box_pos(self):
        return self.box_pos


# create a game object
game = Puzzle()
play_again = True


def update_blocks():
    pos = [1, 101, 199, 199]
    x = 0
    for i in game.get_box_pos():
        pygame.draw.rect(display_surface, gray, pygame.Rect(pos), width=10, border_radius=10)
        display_surface.blit(font.render(i, True, (0, 0, 0)), (pos[0] + 60, pos[1] + 60))

        x += 1
        if x == 3:
            x = 0  # end column and draw rows
            pos[0] = 1
            pos[1] += 199
        else:
            pos[0] += 199


def update_moves():
    display_surface.blit(font_small.render(str("MOVES : "), True, (0, 0, 0)), (200, 25))
    display_surface.blit(font_small.render(str(game.moves), True, (0, 0, 0)), (400, 25))


def play():
    # shuffle puzzle
    game.shuffle()

    while True:
        pygame.draw.rect(display_surface, bg_color, pygame.Rect(0, 100, 600, 600), border_radius=20)
        pygame.draw.rect(display_surface, bg_color, pygame.Rect(0, 0, 600, 100), border_radius=20)

        if game.check_state():

            pygame.draw.rect(display_surface, bg_color, pygame.Rect(0, 0, 600, 700))

            display_surface.blit(font.render("YOU WON!", True, (0, 0, 0)), (160, 300))
            display_surface.blit(font_small.render("MOVES : " + str(game.moves), True, (0, 0, 0)), (235, 450))
            display_surface.blit(font_smaller.render("PRESS ENTER TO PLAY AGAIN!", True, (0, 0, 0)), (200, 600))
            pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            return True
                        elif event.key == pygame.K_ESCAPE:
                            return False
                    else:
                        continue

        update_blocks()
        update_moves()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.moves += game.button_pressed(-3)
                elif event.key == pygame.K_DOWN:
                    game.moves += game.button_pressed(3)
                elif event.key == pygame.K_LEFT:
                    game.moves += game.button_pressed(-1)
                elif event.key == pygame.K_RIGHT:
                    game.moves += game.button_pressed(1)
                elif event.key == pygame.K_ESCAPE:
                    return False


while play_again:
    play_again = play()

pygame.quit()
