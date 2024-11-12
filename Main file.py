
import pygame
import sys


pygame.init()

# General setup for clock and display
CLOCK = pygame.time.Clock()  # Set up the clock to control the game's frame rate
SCREEN = pygame.display.set_mode((800, 600))  # Create a display window of size 800x600
pygame.display.set_caption("Jumping in PyGame")  # Set the window title

class Cowboy:
    def __init__(self, position):
        self.position = position(400,500)

    def initiate_position(self):
        cowboy_rect = 



# Set jumping state to False by default
jumping = False  # Variable to track if the cowboy is currently jumping

# Define gravity and jump height
Y_GRAVITY = 0.5  # Gravity to pull the cowboy down after a jump
JUMP_HEIGHT = 15  # I adjusted the height so that the cowboy can jump over the cactus and the snake. 
Y_Jumpspeed = JUMP_HEIGHT  # Set the initial jump speed to the defined jump height

# Load images and transform their size for the cowboy character's appearance
STANDING_SURFACE = pygame.transform.scale(pygame.image.load("stand 1.png"), (88, 104))  # Image when standing
JUMPING_SURFACE = pygame.transform.scale(pygame.image.load("jump 1.png"), (88, 104))  # Image when jumping
# Create a rectangle for the cowboy's position, starting with the standing surface
cowboy_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))

# Load the background image
BACKGROUND = pygame.image.load("background.png")
BACKGROUND_WIDTH = BACKGROUND.get_width() #get the width of background for scrolling
x_offset = 0
SCROLL_SPEED =5 #speed for background scrolling, I can modify


# Set the cactus and snake images
cactus_img = pygame.image.load("cactus.png").convert()  
snake_img = pygame.image.load("snake.png") 

# Set the background of cactus and snake transparent
cactus_img.set_colorkey((255, 255, 255))  
snake_img.set_colorkey((255, 255, 255))  

# Adjust the size of the cactus and snake
cactus_img = pygame.transform.scale(cactus_img, (100, 100))  # Cactus height shall be lower than cowbot's jump height
snake_img = pygame.transform.scale(snake_img, (100, 100))  # Same as above

# Get the rectangles of the cactus and snake
cactus_rect = cactus_img.get_rect(x=1200, y=450)
snake_rect = snake_img.get_rect(x=1600, y=450)

# Set the speed of the cactus and snake
#cactus_speed = 3
#snake_speed = 3

# Initialize score
score = 0
game_started = False
# Game over sign
game_over = False

# Create a font object to display the fraction
font = pygame.font.Font(None, 50)

# Main game loop
while True:
    # Check for events in the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit()
    if not game_started:
    # Detect if the space key is pressed for jumping
    
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:  # Start jumping if space is pressed
            game_started = True
        # Display the start screen (here for the game instruction to display)
        SCREEN.fill((255, 255, 255))  # White background
        start_text = font.render("Welcome to the Cowboy jumping game!", True, (0, 0, 0))
        text_rect = start_text.get_rect(center=(800 / 2, 600 / 2))
        SCREEN.blit(start_text, text_rect)
        pygame.display.update()
        continue  # Skip the rest of the loop until the game starts
    
    if not game_over:
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
    
        cactus_rect.x -= SCROLL_SPEED
        snake_rect.x -= SCROLL_SPEED
    
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
        if cactus_rect.right < -cactus_rect.width:
            cactus_rect.x = 800 +400
        if snake_rect.right < -snake_rect.width:
            snake_rect.x = 800 +800
    # Draw cactus and snake
        SCREEN.blit(cactus_img, cactus_rect)
        SCREEN.blit(snake_img, snake_rect)

    
    
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

    # Check collisions
        if cowboy_rect.colliderect(cactus_rect):
            game_over = True  # Game over if cowboy hits cactus
        elif cowboy_rect.colliderect(snake_rect):
            score -= 1  # Decrease score if cowboy hits snake
        # Update score
        elif cactus_rect.right < cowboy_rect.left:  # When the cowboy successfully crosses the cactus
            score += 1  # Score plus 1

    # Display score
        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        SCREEN.blit(score_text, (10, 10))
    
    else:
        game_over_text= font.render("GAME OVER! ", True,(255,0,0))
        text_rect = game_over_text.get_rect (center=(800/2, 600/2))
        SCREEN.blit(game_over_text, text_rect )
    # Update the display to show new positions and images
    pygame.display.update()
    CLOCK.tick(60)  # Cap the frame rate at 60 frames per second
  
    
   

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

# Quit Pygame

