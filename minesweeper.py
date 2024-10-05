import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
TILE_SIZE = 40
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
FPS = 30
NUM_MINES = 10

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 24)

# Game Variables
game_over = False
game_start_time = 0

# Tile Class
class Tile:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def reveal(self):
        self.is_revealed = True

    def flag(self):
        self.is_flagged = not self.is_flagged

# Minesweeper Class
class Minesweeper:
    def __init__(self):
        self.board = [[Tile() for _ in range(COLS)] for _ in range(ROWS)]
        self.place_mines()
        self.calculate_adjacency()

    def place_mines(self):
        mine_count = 0
        while mine_count < NUM_MINES:
            r = random.randint(0, ROWS - 1)
            c = random.randint(0, COLS - 1)
            if not self.board[r][c].is_mine:
                self.board[r][c].is_mine = True
                mine_count += 1

    def calculate_adjacency(self):
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c].is_mine:
                    continue
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if 0 <= r + dr < ROWS and 0 <= c + dc < COLS:
                            if self.board[r + dr][c + dc].is_mine:
                                self.board[r][c].adjacent_mines += 1

    def reveal_tile(self, r, c):
        if self.board[r][c].is_revealed or self.board[r][c].is_flagged:
            return

        self.board[r][c].reveal()

        if self.board[r][c].is_mine:
            global game_over
            game_over = True
            return

        if self.board[r][c].adjacent_mines == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if 0 <= r + dr < ROWS and 0 <= c + dc < COLS:
                        self.reveal_tile(r + dr, c + dc)

    def flag_tile(self, r, c):
        self.board[r][c].flag()

    def draw(self, screen):
        for r in range(ROWS):
            for c in range(COLS):
                tile = self.board[r][c]
                rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                if tile.is_revealed:
                    color = WHITE
                    if tile.is_mine:
                        color = RED
                    pygame.draw.rect(screen, color, rect)
                    if tile.adjacent_mines > 0 and not tile.is_mine:
                        text = FONT.render(str(tile.adjacent_mines), True, BLACK)
                        screen.blit(text, (c * TILE_SIZE + 10, r * TILE_SIZE + 5))
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                    if tile.is_flagged:
                        pygame.draw.circle(screen, BLACK, rect.center, TILE_SIZE // 4)

                pygame.draw.rect(screen, BLACK, rect, 1)

# Function to reset the game
def reset_game():
    global game_over, game_start_time
    game_over = False
    game_start_time = time.time()
    return Minesweeper()

def main():
    global game_over, game_start_time
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Minesweeper')
    minesweeper = reset_game()

    while True:
        screen.fill(WHITE)
        minesweeper.draw(screen)

        if game_over:
            text = FONT.render("Game Over!", True, BLACK)
            screen.blit(text, (WIDTH // 2 - 60, HEIGHT // 2 - 20))
            # Show time taken
            time_taken = int(time.time() - game_start_time)
            time_text = FONT.render(f"Time: {time_taken} seconds", True, BLACK)
            screen.blit(time_text, (WIDTH // 2 - 80, HEIGHT // 2 + 10))
            restart_text = FONT.render("Press R to Restart", True, BLACK)
            screen.blit(restart_text, (WIDTH // 2 - 90, HEIGHT // 2 + 40))
        else:
            # Display elapsed time
            elapsed_time = int(time.time() - game_start_time)
            timer_text = FONT.render(f"Time: {elapsed_time}", True, BLACK)
            screen.blit(timer_text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                if event.button == 1:  # Left click
                    minesweeper.reveal_tile(row, col)
                elif event.button == 3:  # Right click
                    minesweeper.flag_tile(row, col)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:  # Restart game
                    minesweeper = reset_game()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()