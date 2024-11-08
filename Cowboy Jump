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
X_POSITION, Y_POSITION = 400, 500  # Cowboy starts at (400, 500) in the window

# Set jumping state to False by default
jumping = False  # Variable to track if the cowboy is currently jumping

# Define gravity and jump height
Y_GRAVITY = 0.5  # Gravity to pull the cowboy down after a jump
JUMP_HEIGHT = 10  # Maximum height the cowboy can jump to
Y_Jumpspeed = JUMP_HEIGHT  # Set the initial jump speed to the defined jump height

# Load images and transform their size for the cowboy character's appearance
STANDING_SURFACE = pygame.transform.scale(pygame.image.load("stand 1.png"), (48, 64))  # Image when standing
JUMPING_SURFACE = pygame.transform.scale(pygame.image.load("jump 1.png"), (48, 64))  # Image when jumping

# Load the background image
BACKGROUND = pygame.image.load("background.png")

# Create a rectangle for the cowboy's position, starting with the standing surface
cowboy_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))

# Main game loop
while True:
    # Check for events in the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If quit event detected, exit the game
            pygame.quit()
            sys.exit()

    # Detect if the space key is pressed for jumping
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_SPACE]:  # Start jumping if space is pressed
        jumping = True

    # Draw the background image on the screen
    SCREEN.blit(BACKGROUND, (0, 0))

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

    # Update the display to show new positions and images
    pygame.display.update()
    CLOCK.tick(60)  # Cap the frame rate at 60 frames per second
