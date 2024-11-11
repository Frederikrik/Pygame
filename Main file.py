# Import the necessary modules
import pygame
import sys

# Initialize Pygame
pygame.init()

# General setup for clock and display
CLOCK = pygame.time.Clock()  # Set up the clock to control the game's frame rate
SCREEN = pygame.display.set_mode((800, 600))  # Create a display window of size 800x600
pygame.display.set_caption("Jumping in PyGame")  # Set the window title

# Initial position of the cowboy character
X_POSITION, Y_POSITION = 100, 500  # Cowboy starts at (400, 500) in the window

# Set jumping state to False by default
jumping = False  # Variable to track if the cowboy is currently jumping

# Define gravity and jump height
Y_GRAVITY = 0.5  # Gravity to pull the cowboy down after a jump
JUMP_HEIGHT = 10  # I adjusted the height so that the cowboy can jump over the cactus and the snake. 
Y_Jumpspeed = JUMP_HEIGHT  # Set the initial jump speed to the defined jump height

# Load images and transform their size for the cowboy character's appearance
STANDING_SURFACE = pygame.transform.scale(pygame.image.load("stand 1.png"), (88, 104))  # Image when standing
JUMPING_SURFACE = pygame.transform.scale(pygame.image.load("jump 1.png"), (88, 104))  # Image when jumping

# Load the background image
BACKGROUND = pygame.image.load("background.png")
#BACKGROUND_WIDTH = BACKGROUND.get_width() #get the width of background for scrolling
#x_offset = 0
#SCROLL_SPEED =5 #speed for background scrolling, I can modify

# Create a rectangle for the cowboy's position, starting with the standing surface
cowboy_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))

# Set the cactus and snake images
cactus_img = pygame.image.load("cactus.png")  
snake_img = pygame.image.load("snake.png") 

# Set the background of cactus and snake transparent
cactus_img = pygame.image.load("cactus.png").convert() # Somehow cactus image needs the convert function (?)
cactus_img.set_colorkey((255, 255, 255))  
snake_img.set_colorkey((255, 255, 255))  

# Adjust the size of the cactus and snake
cactus_img = pygame.transform.scale(cactus_img, (100, 100))  # Cactus height shall be lower than cowbot's jump height
snake_img = pygame.transform.scale(snake_img, (100, 100))  # Same as above

# Get the rectangles of the cactus and snake
cactus_rect = cactus_img.get_rect()
snake_rect = snake_img.get_rect()

# Set the initial positions of the cactus and snake
cactus_rect.x = 600
cactus_rect.y = 450
snake_rect.x = 1000
snake_rect.y = 450

COWBOY_SPEED = 5
# Set the speed of the cactus and snake
#cactus_speed = 3
#snake_speed = 3

# Initialize score
score = 0

# Game over sign
game_over = False

# Create a font object to display the fraction
font = pygame.font.Font(None, 36)

# Main game loop
while True:
    # Check for events in the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit()

    # Detect if the space key is pressed for jumping
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_SPACE]:  # Start jumping if space is pressed
        jumping = True
    
    SCREEN.blit(BACKGROUND, (0,0))
    # Draw the background image on the screen twice to cover the whole screen area
    #SCREEN.blit(BACKGROUND, (x_offset, 0))
    #CREEN.blit(BACKGROUND, (x_offset + BACKGROUND_WIDTH, 0))
    
    # Move cowboy to the right and reset if he goes off-screen
    X_POSITION += COWBOY_SPEED
    if X_POSITION > SCREEN.get_width():
        X_POSITION = -STANDING_SURFACE.get_width()
    # If the cowboy is in the middle of a jump
    if jumping:
        Y_POSITION -= Y_Jumpspeed  # Move the cowboy up by the current jump speed
        Y_Jumpspeed -= Y_GRAVITY  # Decrease the jump speed by gravity to simulate falling
        if Y_Jumpspeed < -JUMP_HEIGHT:  # If the peak of the jump is reached
            jumping = False  # Stop jumping
            Y_Jumpspeed = JUMP_HEIGHT  # Reset jump speed to initial jump height
        cowboy_rect = JUMPING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))  # Update the cowboy's rectangle for jumping
        SCREEN.blit(JUMPING_SURFACE, cowboy_rect)  # Draw the jumping image
    else:
        cowboy_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))  # Reset to standing position
        SCREEN.blit(STANDING_SURFACE, cowboy_rect)  # Draw the standing image

    # Update cactus and snake positions
    cactus_rect.x -= COWBOY_SPEED  # Cactus and snakes shall move with the background
    snake_rect.x -= COWBOY_SPEED

    # If the cactus or snake moves off screen, reset the position
    # According to rules of the game, if the score is or lower than 0, a cactus will definitely appear
    #if cactus_rect.x < -cactus_rect.width:
     #   cactus_rect.x = 800 # Reset the position as background moves
      #  if score <= 0:  # If the score is or lower than 0, a cactus will definitely appear
       #     cactus_img = pygame.image.load("cactus.png")  # Reload the cactus
        #    cactus_img = pygame.image.load("cactus.png").convert()
         #   cactus_img.set_colorkey((255, 255, 255))
          #  cactus_rect = cactus_img.get_rect()
           # cactus_rect.x = 400
            #cactus_rect.y = 400 - cactus_rect.height
    #if snake_rect.x < -snake_rect.width:
     #   snake_rect.x = 800 # Reset the position as background moves
    
    if cactus_rect.right < 0:
        cactus_rect.x = SCREEN.get_width()
    if snake_rect.right < 0:
        snake_rect.x = SCREEN.get_width() + 200

    # Draw cactus and snake
    SCREEN.blit(cactus_img, cactus_rect)
    SCREEN.blit(snake_img, snake_rect)
     # Display score
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    SCREEN.blit(score_text, (10, 10))

     # Update score if cowboy passes a cactus or snake
    if cactus_rect.right < cowboy_rect.left:
        score += 1  
    if snake_rect.right < cowboy_rect.left:
        score += 1   
   
    
    # Move the cactus and snake
    #cactus_rect.x -= cactus_speed
    #snake_rect.x -= snake_speed

    # Display score
    #score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    #SCREEN.blit(score_text, (10, 10))
    
    # Update score
    #if cactus_rect.right < cowboy_rect.left:  # When the cowboy successfully crosses the cactus
     #   score += 1  # Score plus 1

    # Check for collisions
    if not game_over:  
        if cowboy_rect.colliderect(cactus_rect) or cowboy_rect.colliderect(snake_rect):
            game_over = True  
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(800/2, 600/2))
            SCREEN.blit(game_over_text, text_rect)

    # Update the display to show new positions and images
    pygame.display.update()
    CLOCK.tick(60)  # Cap the frame rate at 60 frames per second

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

# Quit Pygame
# pygame.quit()