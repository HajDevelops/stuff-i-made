import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1919, 1020
FPS = 60
GRAVITY = 0.25
JUMP_STRENGTH = 10
PIPE_WIDTH = 300
PIPE_GAP = 500

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Bird Class
class Bird:
    def __init__(self):
        self.rect = pygame.Rect(100, HEIGHT // 2, 30, 30)
        self.y_velocity = 0

    def jump(self):
        self.y_velocity = -JUMP_STRENGTH

    def move(self):
        self.y_velocity += GRAVITY
        self.rect.y += self.y_velocity

# Pipe Class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, HEIGHT - 100 - PIPE_GAP)
        self.rect_top = pygame.Rect(self.x, self.height - HEIGHT, PIPE_WIDTH, HEIGHT)
        self.rect_bottom = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT)

    def move(self):
        self.x -= 5
        self.rect_top.x = self.x
        self.rect_bottom.x = self.x

    def is_off_screen(self):
        return self.x < -PIPE_WIDTH

# Game Class
class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.clock = pygame.time.Clock()
        self.frames = 0
        self.game_over = False

    def spawn_pipe(self):
        self.pipes.append(Pipe(WIDTH))

    def draw(self, screen):
        screen.fill(BLUE)
        pygame.draw.rect(screen, GREEN, self.bird.rect)
        for pipe in self.pipes:
            pygame.draw.rect(screen, GREEN, pipe.rect_top)
            pygame.draw.rect(screen, GREEN, pipe.rect_bottom)

        font = pygame.font.SysFont('Arial', 36)
        score_surface = font.render(str(self.score), True, WHITE)
        screen.blit(score_surface, (WIDTH // 2, 10))

        if self.game_over:
            over_surface = font.render("Game Over! Press R to Restart", True, WHITE)
            screen.blit(over_surface, (WIDTH // 2 - 150, HEIGHT // 2))

    def update(self):
        if not self.game_over:
            self.bird.move()

            if self.frames % 60 == 0:
                self.spawn_pipe()

            for pipe in self.pipes:
                pipe.move()
                if pipe.is_off_screen():
                    self.pipes.remove(pipe)
                    self.score += 1

    def check_collision(self):
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.rect_top) or self.bird.rect.colliderect(pipe.rect_bottom):
                return True
        return self.bird.rect.top < 0 or self.bird.rect.bottom > HEIGHT

    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.frames = 0
        self.game_over = False

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Flappy Bird Clone')
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.bird.jump()
                if game.game_over and event.key == pygame.K_r:
                    game.reset()

        game.update()
        game.draw(screen)

        if game.check_collision():
            game.game_over = True

        pygame.display.flip()
        game.clock.tick(FPS)
        game.frames += 1

if __name__ == "__main__":
    main()
