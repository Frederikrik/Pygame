# Initialize PyGame and the mixer for sound
pygame.init()
pygame.mixer.init()
# Load and play background music
pygame.mixer.music.load("sounds/background_music.mp3")  # Path to your music file
pygame.mixer.music.set_volume(0.5)  # Set volume level (0.0 to 1.0)
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

