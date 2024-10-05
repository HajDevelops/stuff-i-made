import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
ROWS, COLS = HEIGHT // BLOCK_SIZE, WIDTH // BLOCK_SIZE
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (255, 255, 0),  # Yellow
    (128, 0, 128),  # Purple
]

# Shapes
SHAPES = [
    [[[1, 1, 1, 1]]],  # I
    [[[1, 1, 1], [0, 1, 0]]],  # T
    [[[1, 1, 0], [0, 1, 1]]],  # Z
    [[[0, 1, 1], [1, 1, 0]]],  # S
    [[[1, 1], [1, 1]]],  # O
    [[[1, 0, 0], [1, 1, 1]]],  # L
    [[[0, 0, 1], [1, 1, 1]]],  # J
]

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tetris')

# Class for the Tetris game
class Tetris:
    def __init__(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.game_over = False
        self.current_shape, self.current_color = self.new_shape()
        self.current_position = [0, COLS // 2 - 1]
        self.score = 0

    def new_shape(self):
        index = random.randint(0, len(SHAPES) - 1)
        return list(SHAPES[index][0]), COLORS[index]  # Store shape as a list and color separately

    def rotate_shape(self):
        # Store the original shape to validate the rotation
        original_shape = self.current_shape.copy()
        # Rotate the shape
        self.current_shape = [list(row) for row in zip(*self.current_shape[::-1])]

        # Check if the new shape is valid
        if not self.valid_move(self.current_shape, (0, 0)):
            # If not valid, revert to the original shape
            self.current_shape = original_shape

    def valid_move(self, shape, offset):
        for r, row in enumerate(shape):
            for c, value in enumerate(row):
                if value:
                    new_r = self.current_position[0] + r + offset[0]
                    new_c = self.current_position[1] + c + offset[1]
                    if new_r < 0 or new_r >= ROWS or new_c < 0 or new_c >= COLS or self.board[new_r][new_c]:
                        return False
        return True

    def merge_shape(self):
        for r, row in enumerate(self.current_shape):
            for c, value in enumerate(row):
                if value:
                    self.board[self.current_position[0] + r][self.current_position[1] + c] = self.current_color

    def clear_lines(self):
        lines_to_clear = []
        for r in range(ROWS):
            if all(self.board[r]):
                lines_to_clear.append(r)
        for r in lines_to_clear:
            del self.board[r]
            self.board.insert(0, [0 for _ in range(COLS)])
            self.score += 100

    def drop_shape(self):
        if self.valid_move(self.current_shape, (1, 0)):
            self.current_position[0] += 1
        else:
            self.merge_shape()
            self.clear_lines()
            self.current_shape, self.current_color = self.new_shape()
            self.current_position = [0, COLS // 2 - 1]
            if not self.valid_move(self.current_shape, (0, 0)):
                self.game_over = True

    def draw_board(self):
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c]:
                    pygame.draw.rect(screen, self.board[r][c], (c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_current_shape(self):
        for r, row in enumerate(self.current_shape):
            for c, value in enumerate(row):
                if value:
                    pygame.draw.rect(screen, self.current_color, ((self.current_position[1] + c) * BLOCK_SIZE, (self.current_position[0] + r) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def main():
    clock = pygame.time.Clock()
    tetris = Tetris()
    drop_time = 0

    while not tetris.game_over:
        screen.fill(BLACK)
        drop_time += clock.get_time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and tetris.valid_move(tetris.current_shape, (0, -1)):
                    tetris.current_position[1] -= 1
                if event.key == pygame.K_RIGHT and tetris.valid_move(tetris.current_shape, (0, 1)):
                    tetris.current_position[1] += 1
                if event.key == pygame.K_DOWN:
                    tetris.drop_shape()
                if event.key == pygame.K_UP:
                    tetris.rotate_shape()  # Rotate shape

        if drop_time > 1000:  # Drop every second
            tetris.drop_shape()
            drop_time = 0

        tetris.draw_board()
        tetris.draw_current_shape()
        pygame.display.flip()
        clock.tick(FPS)

    print("Game Over! Your score:", tetris.score)
    pygame.quit()


if __name__ == "__main__":
    main()
