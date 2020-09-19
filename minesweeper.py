import pygame
from random import randint
import time


def refresh():
    pygame.display.flip()


class Display:
    def __init__(self, width, height):
        self.resolution = (width, height)
        self.object = pygame.display.set_mode(self.resolution)

    def fill(self, color):
        self.object.fill(color)


class Square:
    def __init__(self, marked, opened, is_mine, x, y, size):
        self.marked = marked
        self.opened = opened
        self.size = size
        self.isMine = is_mine
        self.x = x
        self.y = y
        self.object = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen_var, color):
        pygame.draw.rect(screen_var, color, self.object)

    def blit(self, screen_var, variant):
        if self.opened:
            if self.isMine:
                screen_var.blit(pygame.image.load("mine.png"), (self.x, self.y))
            else:
                screen_var.blit(pygame.image.load("opened_" + str(variant) + ".png"), (self.x, self.y))
        elif self.marked:
            screen_var.blit(pygame.image.load("marked.png"), (self.x, self.y))
        elif not self.opened:
            screen_var.blit(pygame.image.load("closed.png"), (self.x, self.y))

    def clear(self, squares_already_cleared):
        x = int(self.x / SQUARE_SIZE)
        y = int((self.y - MENU_SIZE) / SQUARE_SIZE)
        from_x = x - 1
        if from_x < 0:
            from_x = 0
        to_x = x + 1
        if to_x > SQUARES_X:
            to_x = x
        from_y = y - 1
        if from_y < 0:
            from_y = 0
        to_y = y + 1
        if to_y > SQUARES_Y:
            to_y = y
        surrounding_squares = []
        surrounding_square_rows = board.object[from_y:to_y + 1]
        for row in surrounding_square_rows:
            surrounding_squares.append(row[from_x:to_x + 1])
        number_of_mines = 0
        for row in surrounding_squares:
            number_of_mines += len([square for square in row if square.isMine])
        self.opened = True
        squares_already_cleared.append(self)
        self.blit(SCREEN.object, number_of_mines)
        if number_of_mines == 0:
            for row in surrounding_squares:
                for square in row:
                    if square not in squares_already_cleared:
                        square.opened = True
                        square.blit(SCREEN.object, number_of_mines)
                        squares_already_cleared.append(square)
                        square.clear(squares_already_cleared)

    def click(self):
        if not self.opened:
            if not self.marked:
                if self.isMine:
                    self.opened = True
                    self.blit(SCREEN.object, None)
                    return True
                else:
                    self.clear([])
        return False


class Board:
    def __init__(self, start_x, start_y, square_amount_x, square_amount_y, square_size, bomb_amount):
        self.mines = []
        self.object = [[0 for i in range(square_amount_x)] for j in range(square_amount_y)]
        for i in range(bomb_amount):
            while True:
                y = randint(0, square_amount_y - 1)
                x = randint(0, square_amount_x - 1)
                if self.object[y][x] != 1:
                    self.object[y][x] = 1
                    break
        amount_drawn_x = 0
        amount_drawn_y = 0
        new_board = []
        for rows in self.object:
            new_board_row = []
            for obj in rows:
                x = start_x + amount_drawn_x * square_size
                y = start_y + amount_drawn_y * square_size
                is_mine = obj == 1
                square = Square(False, False, is_mine, x, y, square_size)
                if is_mine:
                    self.mines.append(square)
                new_board_row.append(square)
                amount_drawn_x += 1
            new_board.append(new_board_row)
            amount_drawn_y += 1
            amount_drawn_x = 0
        self.object = new_board

    def draw_new(self, screen_var):
        for rows in self.object:
            for square in rows:
                square.blit(screen_var, None)


class Menu:
    def __init__(self, height, width,  color, font, time_coord, score_coord):
        self.height = height
        self.width = width
        self.color = color
        self.font = font
        self.time_coord = time_coord
        self.score_coord = score_coord
        self.object = pygame.Rect(0, 0, width, height)

    def update_score(self, screen_var, score_var):
        pygame.draw.rect(screen_var, self.color, self.object)
        score_text = MENU_FONT.render(str(score_var), False, RED)
        SCREEN.object.blit(score_text, self.score_coord)

    def update_time(self, screen_var, time_var):
        pygame.draw.rect(screen_var, self.color, self.object)
        time_text = MENU_FONT.render(str(time_var), False, RED)
        SCREEN.object.blit(time_text, self.time_coord)

    def update_both(self, screen_var, score_var, time_var):
        pygame.draw.rect(screen_var, self.color, self.object)
        score_text = MENU_FONT.render(str(score_var), False, RED)
        time_text = MENU_FONT.render(str(time_var), False, RED)
        if not IN_GAME:
            game_over_text = GAME_OVER_FONT.render("Game over! Press 'r' to restart", False, RED)
            SCREEN.object.blit(game_over_text, GAME_OVER_COORDINATES)
        SCREEN.object.blit(time_text, self.time_coord)
        SCREEN.object.blit(score_text, self.score_coord)


def click(mouse_pos):
    x = int(mouse_pos[0] / SQUARE_SIZE)
    y = int((mouse_pos[1] - MENU_SIZE) / SQUARE_SIZE)
    clicked_square = board.object[y][x]
    game_over = clicked_square.click()
    return game_over


def right_click(mouse_pos, bombs):
    x = int(mouse_pos[0] / SQUARE_SIZE)
    y = int((mouse_pos[1] - MENU_SIZE) / SQUARE_SIZE)
    clicked_square = board.object[y][x]
    if not clicked_square.opened:
        if clicked_square.marked:
            clicked_square.marked = False
            bombs += 1
        else:
            clicked_square.marked = True
            bombs -= 1
        clicked_square.blit(SCREEN.object, None)
    return bombs


RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (125, 125, 125)
BLACK = (0, 0, 0)
SQUARE_SIZE = 21
SQUARES_X = 20
SQUARES_Y = 20
# SCREEN_WIDTH = 1920
# SCREEN_HEIGHT = 1080
# SQUARES_X = int(SCREEN_WIDTH / SQUARE_SIZE)
# SQUARES_y = int(SCREEN_HEIGHT / SQUARE_SIZE)
pygame.font.init()
MENU_FONT = pygame.font.SysFont('Comic Sans MS', 15)
GAME_OVER_FONT = pygame.font.SysFont('Comic Sans MS', 20)
MENU_SIZE = 40
MENU_COLOR = WHITE
SCORE_COORDINATES = (5, 0)
TIME_COORDINATES = (50, 0)
GAME_OVER_COORDINATES = (70, 5)
MENU = Menu(MENU_SIZE, SQUARE_SIZE*SQUARES_X, MENU_COLOR, MENU_FONT, TIME_COORDINATES, SCORE_COORDINATES)
BOMB_AMOUNT = randint(10, 15)
SCREEN = Display(SQUARES_X * SQUARE_SIZE, MENU_SIZE + SQUARES_Y * SQUARE_SIZE)
MINIMUM_BOMBS = 100
MAXIMUM_BOMBS = 100

START_X = 0
LEFT_CLICK = 1
RIGHT_CLICK = 3
IN_GAME = True
WIN = False
while True:
    BOMB_AMOUNT = randint(MINIMUM_BOMBS, MAXIMUM_BOMBS)
    board = Board(START_X, MENU_SIZE, SQUARES_X, SQUARES_Y, SQUARE_SIZE, BOMB_AMOUNT)
    board.draw_new(SCREEN.object)
    START_TIME = time.perf_counter()
    while IN_GAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    IN_GAME = not click(pygame.mouse.get_pos())
                if event.button == RIGHT_CLICK:
                    BOMB_AMOUNT = right_click(pygame.mouse.get_pos(), BOMB_AMOUNT)
        TIME = int((time.perf_counter() - START_TIME))
        MENU.update_both(SCREEN.object, BOMB_AMOUNT, TIME)
        if all(mine.marked for mine in board.mines) and BOMB_AMOUNT == 0:
            WIN = True
            IN_GAME = False
        refresh()
    if WIN:
        for rw in board.object:
            for sqr in rw:
                if not sqr.opened:
                    sqr.clear([])
        pygame.quit()
        quit()
    else:
        TIME = int((time.perf_counter() - START_TIME))
        IN_ANIMATION = True
        mines = (mine for mine in board.mines)
        while not IN_GAME:
            if IN_ANIMATION:
                try:
                    mine = next(mines)
                    mine.opened = True
                    mine.blit(SCREEN.object, None)
                    if not mine.marked:
                        BOMB_AMOUNT -= 1
                    MENU.update_both(SCREEN.object, BOMB_AMOUNT, TIME)
                except StopIteration:
                    IN_ANIMATION = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        SCREEN.fill(BLACK)
                        IN_ANIMATION = False
                        IN_GAME = True
            refresh()
            time.sleep(0.01)
