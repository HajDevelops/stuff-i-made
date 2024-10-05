import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE
FPS = 60
COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Font for rendering
FONT = pygame.font.SysFont('Arial', 40)

# Game Class
class Game:
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.add_tile()
        self.add_tile()

    def add_tile(self):
        empty_tiles = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.grid[i][j] = random.choice([2, 4])

    def draw(self, screen):
        screen.fill((187, 173, 160))
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.grid[i][j]
                pygame.draw.rect(screen, COLORS[value], (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if value != 0:
                    text = FONT.render(str(value), True, (255, 255, 255))
                    text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                    screen.blit(text, text_rect)

    def compress(self):
        new_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            pos = 0
            for j in range(GRID_SIZE):
                if self.grid[i][j] != 0:
                    new_grid[i][pos] = self.grid[i][j]
                    pos += 1
        self.grid = new_grid

    def merge(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 1):
                if self.grid[i][j] == self.grid[i][j + 1] and self.grid[i][j] != 0:
                    self.grid[i][j] *= 2
                    self.grid[i][j + 1] = 0

    def reverse(self):
        new_grid = []
        for i in range(GRID_SIZE):
            new_grid.append([])
            for j in range(GRID_SIZE - 1, -1, -1):
                new_grid[i].append(self.grid[i][j])
        self.grid = new_grid

    def transpose(self):
        new_grid = [[self.grid[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
        self.grid = new_grid

    def move(self, direction):
        if direction == 'left':
            self.compress()
            self.merge()
            self.compress()
        elif direction == 'right':
            self.reverse()
            self.compress()
            self.merge()
            self.compress()
            self.reverse()
        elif direction == 'up':
            self.transpose()
            self.compress()
            self.merge()
            self.compress()
            self.transpose()
        elif direction == 'down':
            self.transpose()
            self.reverse()
            self.compress()
            self.merge()
            self.compress()
            self.reverse()
            self.transpose()
        self.add_tile()

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('2048 Game')
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move('left')
                elif event.key == pygame.K_RIGHT:
                    game.move('right')
                elif event.key == pygame.K_UP:
                    game.move('up')
                elif event.key == pygame.K_DOWN:
                    game.move('down')

        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
