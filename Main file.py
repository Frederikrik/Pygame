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
pygame.display.set_caption("COWBOY JUMP")  # Set the window title

# Initial position of the cowboy character
X_POSITION, Y_POSITION = 150, 500  
# Define gravity and jump height
Y_GRAVITY = 0.5  # Gravity to pull the cowboy down after a jump
JUMP_HEIGHT = 15  
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
SCROLL_SPEED =5 #speed for background scrolling

# Create a rectangle for the cowboy's position, starting with the standing surface
cowboy_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))


game_started = False
# Game over sign
game_over = False

GROUND_HEIGHT = 500
 
# Randomly generated obstacles
class Obstacle():
    score = 0  # Initialize the score to 0
    move = 5  # Set the movement speed to 3
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
        self.mask= pygame.mask.from_surface(self.image)
        
        # Set the size, position and background transparency of the obstacles and the size of the obstacle rectangle
        self.image = pygame.transform.scale(self.image, (100, 100))  # Set the size of the obstacles
        self.rect.size = self.image.get_size()  # Adjust the rectangle size
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
def game_loop(x_offset, jumping, score, obstacle_lst, obstacle_time, start_time):
    global Y_Jumpspeed, Y_POSITION, cowboy_rect, GROUND_HEIGHT, SCROLL_SPEED
    
    collision_times = {}
    game_over = False
    keys_pressed =pygame.key.get_pressed()
    if keys_pressed [pygame.K_SPACE]:
        jumping= True
    # increase speed after some time  
    elapsed_time= time.time() - start_time
    if elapsed_time > 10:
        SCROLL_SPEED =7
        for obstacle in obstacle_lst:
            obstacle.move = 7
    if elapsed_time > 20:
        SCROLL_SPEED = 9
        for obstacle in obstacle_lst:
            obstacle.move = 9
    if elapsed_time > 25:
        SCROLL_SPEED = 10
        for obstacle in obstacle_lst:
            obstacle.move = 10            
    x_offset -= SCROLL_SPEED
    if x_offset <= -BACKGROUND_WIDTH:
        x_offset =0
    # Draw the background image on the screen twice to cover the whole screen area
    SCREEN.blit(BACKGROUND, (x_offset, 0))
    SCREEN.blit(BACKGROUND, (x_offset + BACKGROUND_WIDTH, 0))

    # Check for events in the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit()


    # Generate obstacles
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
        cowboy_mask= pygame.mask.from_surface(JUMPING_SURFACE)
        SCREEN.blit(JUMPING_SURFACE, cowboy_rect)  # Draw the jumping image
    else:
        cowboy_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))  # Reset to standing position
        cowboy_mask = pygame.mask.from_surface(STANDING_SURFACE)
        SCREEN.blit(STANDING_SURFACE, cowboy_rect)  # Draw the standing image

    for obstacle in obstacle_lst:
        offset = (obstacle.rect.x - cowboy_rect.x, obstacle.rect.y - cowboy_rect.y)
        collision = cowboy_mask.overlap(obstacle.mask, offset)
        if collision:
            if obstacle.obstacle_class ==0:
                if not jumping:
                    game_over =True
            elif obstacle.obstacle_class ==1:
                if not jumping:
                    if score >0:
                        score-= 1
                    else:
                        game_over= True # avoid score below zero
            obstacle_lst.remove(obstacle)
        elif obstacle.obstacle_class ==0 and obstacle.rect.right < cowboy_rect.left and jumping:
            score += 1
            print ("Score increased! Current score: ", score)
            obstacle_lst.remove(obstacle)
    
    if game_over:
        return False

    # Display score
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    SCREEN.blit(score_text, (10, 10))
    
    # Update the display to show new positions and images
    pygame.display.update()
    CLOCK.tick(60)  # Cap the frame rate at 60 frames per second

    return x_offset, jumping, score, obstacle_lst, obstacle_time, start_time
   

def game_start():
    # Display the start screen (here for the game instruction to display)
    SCREEN.fill ((255, 255, 255))
    texts = [
        ("Welcome to the COWBOY JUMP game!", (255, 0, 0)),
        ("Press SPACE to start", (0, 0, 0)),
        ("Jump over CACTUS to collect points", (0, 0, 0)),
        ("Avoid SNAKES or you'll lose points", (0, 0, 0)),
    ]
    
    y_start = 200  # Starting Y-coordinate for the first text
    y_gap = 50     # Space between lines
    
    for i, (text, color) in enumerate(texts):
        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(center=(800 // 2, y_start + i * y_gap))
        SCREEN.blit(rendered_text, text_rect)
    
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                pygame.quit()
                sys.exit()
        
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:  # Start jumping if space is pressed
            return True

def game_restart():
    global SCROLL_SPEED
    SCROLL_SPEED = 5
    game_over_text = font.render("GAME OVER!", True,(255,0,0))
    game_restart_text = font.render("Press R to restart", True, (255,0,0))
    game_over_rect = game_over_text.get_rect(center=(800/2, 100))
    game_restart_rect = game_over_text.get_rect(center=(800/2, 150))
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
    
    jumping = False   
    start_time = time.time()
    params = [x_offset, jumping, score, obstacle_lst, obstacle_time, start_time]
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

