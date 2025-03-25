
import pygame
import sys

# Initialize Pygame
pygame.init()

# Game Settings
WIDTH, HEIGHT = 640, 480  # Window size
FPS = 60  # Frames per second

# Load SpriteSheet Function
def load_spritesheet(path, frame_width, frame_height):
    spritesheet = pygame.image.load(path).convert_alpha()
    frames = []
    for i in range(spritesheet.get_width() // frame_width):
        frame = spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animated Sprite Example")

# Load Sprite Animation
SPRITE_PATH = "sprite_sheet.png"  # Replace with your sprite sheet
FRAME_WIDTH, FRAME_HEIGHT = 32, 32  # Size of each frame in pixels
animation_frames = load_spritesheet(SPRITE_PATH, FRAME_WIDTH, FRAME_HEIGHT)

# Animation Variables
current_frame = 0
frame_delay = 100  # Time per frame in milliseconds
last_update = pygame.time.get_ticks()

# Main Loop
clock = pygame.time.Clock()
while True:
    screen.fill((30, 30, 30))  # Background color
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Animation Logic
    now = pygame.time.get_ticks()
    if now - last_update > frame_delay:
        current_frame = (current_frame + 1) % len(animation_frames)
        last_update = now
    
    # Draw Sprite
    screen.blit(animation_frames[current_frame], (WIDTH//2 - FRAME_WIDTH//2, HEIGHT//2 - FRAME_HEIGHT//2))
    
    pygame.display.flip()
    clock.tick(FPS)
