import pygame
import sys
import random
from pygame.math import Vector2
pygame.init()

cell_size = 40
cell_number = 20
WIN = pygame.display.set_mode(
    (cell_number * cell_size, cell_number * cell_size))
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)


class FRUIT:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = pygame.Vector2(self.x, self.y)
        self.col = (0, 255, 0)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(WIN, self.col, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.col = (255, 0, 0)
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.score = 0

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(
                int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(WIN, self.col, block_rect)

    def move_snake(self):
        if self.new_block == True:
            body_temp = self.body[:]
            body_temp.insert(0, body_temp[0] + self.direction)
            self.body = body_temp
            self.new_block = False
        else:
            body_temp = self.body[:-1]
            body_temp.insert(0, body_temp[0] + self.direction)
            self.body = body_temp

    def grow(self):
        self.new_block = True


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_death()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.score += 1
            self.fruit.randomize()
            self.snake.grow()

    def game_over(self):
        print('Your score is: ' + str(self.snake.score))
        pygame.quit()
        sys.exit()

    def check_death(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()


main_game = MAIN()
clock = pygame.time.Clock()
run = True
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while run:
    WIN.fill(BACKGROUND_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                main_game.snake.direction = Vector2(0, -1)

            if event.key == pygame.K_DOWN:
                main_game.snake.direction = Vector2(0, 1)

            if event.key == pygame.K_RIGHT:
                main_game.snake.direction = Vector2(1, 0)

            if event.key == pygame.K_LEFT:
                main_game.snake.direction = Vector2(-1, 0)
    main_game.draw_elements()
    pygame.display.update()
pygame.quit()
