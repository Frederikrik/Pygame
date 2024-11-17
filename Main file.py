# Import the necessary modules
import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# General setup for clock and display
CLOCK = pygame.time.Clock()  # Set up the clock to control the game's frame rate
SCREEN = pygame.display.set_mode((800, 600))  # Create a display window of size 800x600
pygame.display.set_caption("Jumping in PyGame")  # Set the window title

# Initial position of the cowboy character
X_POSITION, Y_POSITION = 150, 500  # Shall cowboy start at (150, 500) or (400, 500) in the window?

# Define gravity and jump height
Y_GRAVITY = 0.5  # Gravity to pull the cowboy down after a jump
JUMP_HEIGHT = 15  # I adjusted the height so that the cowboy can jump over the cactus and the snake. 
Y_Jumpspeed = JUMP_HEIGHT  # Set the initial jump speed to the defined jump height

# Load images and transform their size for the cowboy character's appearance
STANDING_SURFACE = pygame.transform.scale(pygame.image.load("stand 1.png"), (88, 104))  # Image when standing
JUMPING_SURFACE = pygame.transform.scale(pygame.image.load("jump 1.png"), (88, 104))  # Image when jumping

# Load the background image
try:
    BACKGROUND = pygame.image.load("background.png").convert_alpha()
except pygame.error as e:
    print(f"Error loading image: {e}")
    exit()
BACKGROUND_WIDTH = BACKGROUND.get_width() #get the width of background for scrolling
x_offset = 0
SCROLL_SPEED =5 #speed for background scrolling, I can modify

# Create a rectangle for the cowboy's position, starting with the standing surface
cowboy_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))

# Set the cactus and snake images 
# snake_img = pygame.image.load("snake.png") 

# Set the background of cactus and snake transparent
# snake_img.set_colorkey((255, 255, 255))  

# Adjust the size of the cactus and snake
# cactus_img = pygame.transform.scale(cactus_img, (100, 100))  # Cactus height shall be lower than cowbot's jump height
# snake_img = pygame.transform.scale(snake_img, (100, 100))  # Same as above

# Get the rectangles of the cactus and snake
# cactus_rect = cactus_img.get_rect(x=1200, y=450)
# snake_rect = snake_img.get_rect(x=1600, y=450)

# Set the speed of the cactus and snake
#cactus_speed = 3
#snake_speed = 3

# Initialize score
# score = 0
game_started = False
# Game over sign
game_over = False

GROUND_HEIGHT = 500
 
# Randomly generated obstacles
class Obstacle():
    score = 0  # Initialize the score to 0
    move = 3  # Set the movement speed to 3
    obstacle_y = 500  # Set the y position of the obstacle to 500
    can_move = True

    def __init__(self):
        self.rect = pygame.Rect(0,0,0,0)  # Create a rectangle for collision checks
        images = [
            pygame.image.load("cactus.png").convert(),
            pygame.image.load("snake.png").convert()
        ]
        self.image = random.choice(images)  # Randomly select an image
        self.obstacle_class = images.index(self.image)
        
        # Set the size, position and background transparency of the obstacles and the size of the obstacle rectangle
        self.image = pygame.transform.scale(self.image, (110, 110))  # Set the size of the obstacles
        # self.rect.size = (50, 50) # Try to adjust the rectangle size by manual checking
        self.rect.size = self.image.get_size() 
        self.width, self.height = self.rect.size
        self.x = 800  # Set the initial position of the obstacles to the right side of the screen
        self.y = self.obstacle_y
        self.rect.center = (self.x ,self.y)
        self.image.set_colorkey((255, 255, 255))  
    
    # Obstacles move
    def obstacle_move(self):
        if self.can_move:
            self.rect.x -= self.move
	# Draw the obstacles
    def draw_obstacle(self):
        SCREEN.blit(self.image,(self.rect.x, self.rect.y))

# Create a font object to display the fraction
font = pygame.font.Font(None, 50)

# Main game loop
def game_loop(x_offset, jumping, score, obstacle_lst, obstacle_time):
    global Y_Jumpspeed, Y_POSITION, cowboy_rect, GROUND_HEIGHT
    game_over = False
    keys_pressed =pygame.key.get_pressed()
    if keys_pressed [pygame.K_SPACE]:
        jumping= True

    x_offset -= SCROLL_SPEED
    if x_offset <= -BACKGROUND_WIDTH:
        x_offset =0
    # SCREEN.blit(BACKGROUND, (0,0))
    # Draw the background image on the screen twice to cover the whole screen area
    SCREEN.blit(BACKGROUND, (x_offset, 0))
    SCREEN.blit(BACKGROUND, (x_offset + BACKGROUND_WIDTH, 0))

    # cactus_rect.x -= SCROLL_SPEED
    # snake_rect.x -= SCROLL_SPEED
    # Check for events in the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit()
    
    
    # If the cactus or snake moves off screen, reset the position
    # According to rules of the game, if the score is or lower than 0, a cactus will definitely appear
    #if cactus_rect.x < -cactus_rect.width:
    #   cactus_rect.x = 800 # Reset the position as background moves
    #  if score <= 0:  # If the score is or lower than 0, a cactus will definitely appear
    #     cactus_img = pygame.image.load("cactus.png")  # Reload the cactus
        #    cactus_img = pygame.image.load("cactus.png").convert()
        #    cactus_img.set_colorkey((255, 255, 255))
        #   cactus_rect = cactus_img.get_rect()
        #  cactus_rect.x = 400
        # cactus_rect.y = 400 - cactus_rect.height
    #if snake_rect.x < -snake_rect.width:
    #    snake_rect.x = 800 # Reset the position as background moves
    # Reset positions if off-screen
        # if cactus_rect.right < -cactus_rect.width:
        #     cactus_rect.x = 800 +400
        # if snake_rect.right < -snake_rect.width:
        #     snake_rect.x = 800 +800
    # # Draw cactus and snake
    #     SCREEN.blit(cactus_img, cactus_rect)
    #     SCREEN.blit(snake_img, snake_rect)

    # Genrate obstacles
    obstacle = Obstacle()
    if len(obstacle_lst) < 2 and time.time() >= obstacle_time + 5:
        obstacle_lst.append(obstacle)  # Add obstacles to the list
        obstacle_time = time.time()
    
    for i in range(len(obstacle_lst)):
        obstacle_lst[i].obstacle_move()
        obstacle_lst[i].draw_obstacle()
    
    # If the cowboy is in the middle of a jump
    if jumping:
        Y_POSITION -= Y_Jumpspeed  # Move the cowboy up by the current jump speed
        if Y_POSITION > GROUND_HEIGHT:
            Y_POSITION = GROUND_HEIGHT

        Y_Jumpspeed -= Y_GRAVITY  # Decrease the jump speed by gravity to simulate falling
        if Y_Jumpspeed < -JUMP_HEIGHT:  # If the peak of the jump is reached
            jumping = False  # Stop jumping
            Y_Jumpspeed = JUMP_HEIGHT  # Reset jump speed to initial jump height
        cowboy_rect = JUMPING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))  # Update the cowboy's rectangle for jumping
        SCREEN.blit(JUMPING_SURFACE, cowboy_rect)  # Draw the jumping image
    else:
        cowboy_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))  # Reset to standing position
        SCREEN.blit(STANDING_SURFACE, cowboy_rect)  # Draw the standing image

    for i, obstacle in enumerate(obstacle_lst):
        if cowboy_rect.colliderect(obstacle):
            game_over = True  # Game over if cowboy hits cactus
            break
        # Update score: Unsure, need to check
        elif obstacle.rect.right < cowboy_rect.left and obstacle.rect.y < Y_POSITION:  # When the cowboy successfully crosses the cactus
            obstacle_lst.remove(obstacle)
            if obstacle.obstacle_class == 0:
                score += 1  # Score plus 1
    
    if game_over:
        return False

    # Display score
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    SCREEN.blit(score_text, (10, 10))
    
    
        
    
    # if not jumping:
    #     if Y_POSITION > GROUND_HEIGHT:
    #         Y_POSITION = GROUND_HEIGHT

    # Update the display to show new positions and images
    pygame.display.update()
    CLOCK.tick(60)  # Cap the frame rate at 60 frames per second
#pygame.quit()  
        


    # Display score
    #score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    #SCREEN.blit(score_text, (10, 10))
    
    # Update score
    #if cactus_rect.right < cowboy_rect.left:  # When the cowboy successfully crosses the cactus
    #   score += 1  # Score plus 1

    # Check for collisions
    #if not game_over:  
    #   if cowboy_rect.colliderect(cactus_rect) or cowboy_rect.colliderect(snake_rect):
    #      game_over = True  
    #     game_over_text = font.render("Game Over!", True, (255, 0, 0))
        #    text_rect = game_over_text.get_rect(center=(800/2, 600/2))
        #   SCREEN.blit(game_over_text, text_rect)

    # Update the display to show new positions and images
    #pygame.display.update()
    #CLOCK.tick(60)  # Cap the frame rate at 60 frames per second

    # Game over Game prompt
    #if game_over:
    #   game_over = True
    #  game_over_text = font.render("Game Over!", True, (255, 0, 0))
    # text_rect = game_over_text.get_rect(center=(800/2, 600/2))
        #SCREEN.blit(game_over_text, text_rect)

        # Wait for the player to press the spacebar to restart the game
        # waiting_for_key = True
        # while waiting_for_key:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #             sys.exit()
        #         if event.type == pygame.KEYDOWN:
        #             waiting_for_key = False
        
        # Restart the game:
            # game_over = False  # Restart the game sings
            # score = 0  # Initialize the score
            # Other initialization codes
    
    # Update display
    # pygame.display.flip()
    return x_offset, jumping, score, obstacle_lst, obstacle_time
   

def game_start():
    # Display the start screen (here for the game instruction to display)
    SCREEN.fill((255, 255, 255))  # White background
    start_text = font.render("Welcome to the cowboy jumping game!", True, (0, 0, 0))
    text_rect = start_text.get_rect(center=(800 / 2, 600 / 2))
    SCREEN.blit(start_text, text_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                pygame.quit()
                sys.exit()
        
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:  # Start jumping if space is pressed
            return True

# Problem to do: Restart game
def game_restart():
    # show the game result
    game_over_text = font.render("GAME OVER!", True,(255,0,0))
    game_restart_text = font.render("Press R to restart", True, (255,0,0))
    game_over_rect = game_over_text.get_rect(center=(800/2, 600/2))
    game_restart_rect = game_over_text.get_rect(center=(350, 350))
    SCREEN.blit(game_over_text, game_over_rect)
    SCREEN.blit(game_restart_text, game_restart_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_r]:  # Start jumping if r is pressed
            return True


def game_round():
    # set initial state
    # initialize obstacle
    obstacle_lst = []
    obstacle_time = time.time() - 5

    # set score
    score = 0

    x_offset = 0
    
    # Set jumping state to False by default
    jumping = False  # Variable to track if the cowboy is currently jumping
    
    params = [x_offset, jumping, score, obstacle_lst, obstacle_time]
    while True:
        loop_result = game_loop(*params)
        if loop_result is False:
            return False
        else:
            params = loop_result


def main():
    #import mixer for music
    pygame.mixer.init()
    # Load and play background music
    pygame.mixer.music.load("western-theme-162884.mp3")  # Path to the music file
    pygame.mixer.music.set_volume(0.5)  # Set volume level (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

    game_start()
    while True:
        round_y = game_round()
        game_restart()

if __name__ == "__main__":
    main()
    pygame.quit()
        

# Quit Pygame

