import pygame
import sys
import random

pygame.init()

# Game Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
Y_GRAVITY = 0.5
JUMP_HEIGHT = 15
SCROLL_SPEED = 5

# Initialize the game screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cowboy Jumping Game")
clock = pygame.time.Clock()

# Load assets
STANDING_SURFACE = pygame.transform.scale(pygame.image.load("stand 1.png"), (88, 104))
JUMPING_SURFACE = pygame.transform.scale(pygame.image.load("jump 1.png"), (88, 104))
BACKGROUND_IMAGE = pygame.image.load("background.png")
cactus_img = pygame.transform.scale(pygame.image.load("cactus.png").convert(), (100, 100))
snake_img = pygame.transform.scale(pygame.image.load("snake.png").convert(), (100, 100))
cactus_img.set_colorkey((255, 255, 255))
snake_img.set_colorkey((255, 255, 255))

font = pygame.font.Font(None, 50)

# Classes
class Player:
    def __init__(self, x, y):
        self.image = STANDING_SURFACE
        self.rect = self.image.get_rect(center=(x, y))
        self.jumping = False
        self.jump_speed = JUMP_HEIGHT

    def jump(self):
        if not self.jumping:
            self.jumping = True

    def update(self):
        if self.jumping:
            self.rect.y -= self.jump_speed
            self.jump_speed -= Y_GRAVITY
            if self.jump_speed < -JUMP_HEIGHT:
                self.jumping = False
                self.jump_speed = JUMP_HEIGHT
            self.image = JUMPING_SURFACE
        else:
            self.image = STANDING_SURFACE

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Obstacle:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.has_been_cleared = False

    def update(self):
        self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH + random.randint(300, 600)  # Respawn off-screen
            self.has_been_cleared = False
    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Background:
    def __init__(self, image):
        self.image = image
        self.x_offset = 0
        self.width = self.image.get_width()

    def update(self):
        self.x_offset -= SCROLL_SPEED
        if self.x_offset <= -self.width:
            self.x_offset = 0

    def draw(self, surface):
        surface.blit(self.image, (self.x_offset, 0))
        surface.blit(self.image, (self.x_offset + self.width, 0))


class Game:
    def __init__(self):
        self.player = Player(100, SCREEN_HEIGHT - 150)
        self.cactus = Obstacle(cactus_img, 1200, 450)
        self.snake = Obstacle(snake_img, 1600, 450)
        self.background = Background(BACKGROUND_IMAGE)
        self.score = 0
        self.game_over = False
        self.game_started = False

    def reset(self):
        self.player = Player(100, SCREEN_HEIGHT - 150)
        self.cactus = Obstacle(cactus_img, 1200, 450)
        self.snake = Obstacle(snake_img, 1600, 450)
        self.background = Background(BACKGROUND_IMAGE)
        self.score = 0
        self.game_over = False

    def check_collision(self, obstacle):
        # Check for pixel-perfect collision between player and an obstacle
        offset_x = obstacle.rect.x - self.player.rect.x
        offset_y = obstacle.rect.y - self.player.rect.y
        if self.player.mask.overlap(obstacle.mask, (offset_x, offset_y)):
            return True
        return False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if not self.game_started:
            if keys[pygame.K_SPACE]:
                self.game_started = True
        elif not self.game_over and keys[pygame.K_SPACE]:
            self.player.jump()

    def update(self):
        if self.game_started and not self.game_over:
            self.player.update()
            self.cactus.update()
            self.snake.update()
            self.background.update()

            # Check collisions
            if self.player.rect.colliderect(self.cactus.rect):
                self.game_over = True
            elif self.player.rect.colliderect(self.snake.rect):
                self.score = max(0, self.score - 1)  # Avoid negative score
           # elif self.cactus.rect.right < self.player.rect.left:
            #    self.score += 1
            if not self.cactus.has_been_cleared and self.cactus.rect.right < self.player.rect.left:
                self.score += 1
                self.cactus.has_been_cleared = True
            # Increase speed after a certain time
            if pygame.time.get_ticks() > 20000:
                global SCROLL_SPEED
                SCROLL_SPEED = 7

    def draw(self):
        if not self.game_started:
            screen.fill(BACKGROUND_COLOR)
            start_text = font.render("Press SPACE to start!", True, (0, 0, 0))
            screen.blit(start_text, start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
        elif self.game_over:
            game_over_text = font.render("GAME OVER!", True, (255, 0, 0))
            screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
        else:
            self.background.draw(screen)
            self.cactus.draw(screen)
            self.snake.draw(screen)
            self.player.draw(screen)
            score_text = font.render("Score: " + str(self.score), True, (0, 0, 0))
            screen.blit(score_text, (10, 10))

# Main game loop
game = Game()
while True:
    game.handle_events()
    game.update()
    game.draw()
    pygame.display.update()
    clock.tick(60)
