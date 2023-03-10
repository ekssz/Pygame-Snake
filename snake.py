import pygame
import time
import random
import sys

# initialization / ініціалізація

pygame.init()

# colors / кольори

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# screen size / розмір екрану

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# blocks size / розмір блоків

BLOCK_SIZE = 10

# game screen / екран для гри

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змійка")


def display_text(text, color, x, y, size):
    font = pygame.font.Font(None, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

# function to create new apples / функція для створення нових яблук

def create_apple():
    apple_x = random.randrange(0, SCREEN_WIDTH-BLOCK_SIZE+1, BLOCK_SIZE)
    apple_y = random.randrange(0, SCREEN_HEIGHT-BLOCK_SIZE+1, BLOCK_SIZE)
    return apple_x, apple_y

# snake / змійка

class Snake:
    def __init__(self):
        self.length = 2
        self.positions = [(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.speed = 1 # початкова швидкість
        self.counter = 0 # кількість зібраних яблук

    def change_direction(self, direction):
        if direction[0] * -1 == self.direction[0] or direction[1] * -1 == self.direction[1]:
            return
        else:
            self.direction = direction

    def move(self):
        cur_x, cur_y = self.positions[0]
        x_change, y_change = self.direction
        new_x = cur_x + (x_change * BLOCK_SIZE)
        new_y = cur_y + (y_change * BLOCK_SIZE)
        if new_x >= SCREEN_WIDTH or new_x < 0 or new_y >= SCREEN_HEIGHT or new_y < 0:
            return True
        elif (new_x, new_y) in self.positions[1:]:
            return True
        else:
            self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()

        self.counter += 1
        if self.counter % 1 == 0: #збільшується швидкість за кожне яблуко
            self.speed += 1 #збільшення швидкості
        
    def increase_length(self):
        self.length += 1
        

    def draw(self):
        for position in self.positions:
            pygame.draw.rect(screen, GREEN, pygame.Rect(
                position[0], position[1], BLOCK_SIZE, BLOCK_SIZE))


    # constants

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

    # snake and apple / створення змійки і яблука

snake = Snake()
apple_x, apple_y = create_apple()

    # score
score = 0

    # main
    
while True:
    
    # events
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(RIGHT)

    game_over = snake.move()

    # зіткнення

    if snake.positions[0] == (apple_x, apple_y):
        snake.increase_length()
        apple_x, apple_y = create_apple()
        score += 10

    # clear

    screen.fill(BLACK)

    # відображення змійки

    snake.draw()
    pygame.draw.rect(screen, RED, pygame.Rect(
        apple_x, apple_y, BLOCK_SIZE, BLOCK_SIZE))

    # відображення рахунку гри на екрані

    display_text(f"Рахунок: {score}", WHITE, 10, 10, 20)

    # game end

    if game_over:
        display_text("Гра закінчена!", WHITE, SCREEN_WIDTH /
                     2-50, SCREEN_HEIGHT/2-10, 30)
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # update

    pygame.display.update()

    # animation

    pygame.time.delay(50)
