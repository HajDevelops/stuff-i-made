import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
BALL_SPEED = 5
PADDLE_SPEED = 10
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_ROWS = 5
BRICK_COLS = 10

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

def random_color():
    """Generate a random color."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Ball Class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 15, 15)
        self.dx = BALL_SPEED
        self.dy = -BALL_SPEED

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top <= 0:
            self.dy = -self.dy
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx = -self.dx

# Paddle Class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 30, 100, 10)

    def move(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Brick Class
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = random_color()  # Assign a random color to the brick

# Game Class
class Game:
    def __init__(self):
        self.ball = Ball()
        self.paddle = Paddle()
        self.bricks = self.create_bricks()
        self.score = 0
        self.game_over = False

    def create_bricks(self):
        bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = col * BRICK_WIDTH
                y = row * BRICK_HEIGHT + 50  # Offset for the top margin
                bricks.append(Brick(x, y))
        return bricks

    def draw(self, screen):
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, self.paddle.rect)
        pygame.draw.ellipse(screen, RED, self.ball.rect)

        for brick in self.bricks:
            pygame.draw.rect(screen, brick.color, brick.rect)  # Use brick's random color

        font = pygame.font.SysFont('Arial', 36)
        score_surface = font.render(f'Score: {self.score}', True, (0, 0, 0))
        screen.blit(score_surface, (10, 10))

        if self.game_over:
            over_surface = font.render("Game Over! Press R to Restart", True, (0, 0, 0))
            screen.blit(over_surface, (WIDTH // 2 - 150, HEIGHT // 2))

    def update(self):
        if not self.game_over:
            self.ball.move()

            # Ball and paddle collision
            if self.ball.rect.colliderect(self.paddle.rect):
                # Calculate hit position
                hit_pos = (self.ball.rect.centerx - self.paddle.rect.left) / self.paddle.rect.width
                self.ball.dx = (hit_pos - 0.5) * 2 * BALL_SPEED  # Change direction based on hit position
                self.ball.dy = -BALL_SPEED  # Always bounce upwards

            # Ball and brick collision
            for brick in self.bricks[:]:
                if self.ball.rect.colliderect(brick.rect):
                    self.bricks.remove(brick)
                    self.ball.dy = -self.ball.dy
                    self.score += 1
                    break  # Break after one collision

            # Check if the ball goes out of bounds
            if self.ball.rect.bottom >= HEIGHT:
                self.game_over = True  # Set game over

    def reset(self):
        self.ball = Ball()
        self.paddle = Paddle()
        self.bricks = self.create_bricks()
        self.score = 0
        self.game_over = False

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Breakout Game')
    game = Game()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game.paddle.move(-PADDLE_SPEED)
        if keys[pygame.K_RIGHT]:
            game.paddle.move(PADDLE_SPEED)

        if not game.game_over:
            game.update()
        else:
            if keys[pygame.K_r]:  # Restart game
                game.reset()

        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
