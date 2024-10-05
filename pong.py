import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
FPS = 60
BALL_SPEED = 5
PADDLE_SPEED = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ball Class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 15, 15)
        self.dx = BALL_SPEED
        self.dy = BALL_SPEED

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off the top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy = -self.dy

    def reset(self):
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2
        self.dx = BALL_SPEED * (-1 if self.dx > 0 else 1)
        self.dy = BALL_SPEED

# Paddle Class
class Paddle:
    def __init__(self, x):
        self.rect = pygame.Rect(x, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dy):
        self.rect.y += dy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Game Class
class Game:
    def __init__(self):
        self.ball = Ball()
        self.paddle1 = Paddle(10)
        self.paddle2 = Paddle(WIDTH - 20)
        self.score1 = 0
        self.score2 = 0

    def draw(self, screen):
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, self.paddle1.rect)
        pygame.draw.rect(screen, BLACK, self.paddle2.rect)
        pygame.draw.ellipse(screen, BLACK, self.ball.rect)
        self.display_score(screen)

    def display_score(self, screen):
        font = pygame.font.SysFont('Arial', 24)
        score_text = f'{self.score1}  {self.score2}'
        score_surface = font.render(score_text, True, BLACK)
        screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, 10))

    def update(self):
        self.ball.move()

        # Ball collision with paddles
        if self.ball.rect.colliderect(self.paddle1.rect) or self.ball.rect.colliderect(self.paddle2.rect):
            self.ball.dx = -self.ball.dx

        # Ball goes out of bounds
        if self.ball.rect.left <= 0:
            self.score2 += 1
            self.ball.reset()
        if self.ball.rect.right >= WIDTH:
            self.score1 += 1
            self.ball.reset()

        # AI for player 2
        if self.ball.rect.centery < self.paddle2.rect.centery:
            self.paddle2.move(-PADDLE_SPEED)
        elif self.ball.rect.centery > self.paddle2.rect.centery + PADDLE_HEIGHT:
            self.paddle2.move(PADDLE_SPEED)

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pong Game with AI')
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # Move paddle 1 up
            game.paddle1.move(-PADDLE_SPEED)
        if keys[pygame.K_s]:  # Move paddle 1 down
            game.paddle1.move(PADDLE_SPEED)

        game.update()
        game.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
