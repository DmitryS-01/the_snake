from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('The Snake')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Base class"""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 color=None):
        """Init"""
        self.position = position
        self.body_color = color

    def draw(self):
        """Draw game object (need to be updated in sub())"""
        pass


class Apple(GameObject):
    """Apple object"""

    def __init__(self):
        """Init"""
        super().__init__(position=self.randomize_position(), color=APPLE_COLOR)

    def randomize_position(self):
        """Return tuple of random cords for apple"""
        return (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))

    def draw(self):
        """Draw an apple"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Snake object"""

    def __init__(self, length=1, positions=None, direction=RIGHT,
                 next_direction=None, body_color=SNAKE_COLOR):
        if positions is None:
            positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        super().__init__(color=body_color)
        self.positions = positions
        self.length = length
        self.direction = direction
        self.next_direction = next_direction

    def update_direction(self):
        """Updates direction of snake"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, need_to_grow):
        """Moves snake"""
        current_head_x, current_head_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head = (
            current_head_x + delta_x * GRID_SIZE,
            current_head_y + delta_y * GRID_SIZE
        )

        self.positions = [new_head] + self.positions

        if not need_to_grow:
            self.positions.pop()

    def draw(self):
        """Draw a snake"""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Returns snake's head position"""
        return self.positions[0]

    def reset(self):
        """Resets snake"""
        self.__init__()


def handle_keys(game_object):
    """Handles user's input"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Main"""
    pygame.init()

    snake = Snake()
    apple = Apple()
    snake.draw()
    apple.draw()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        snake.update_direction()
        if snake.get_head_position() == apple.position:
            need_to_grow = True
            apple = Apple()
        else:
            need_to_grow = False
        snake.move(need_to_grow)
        if snake.get_head_position() in snake.positions:
            snake.reset()

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
