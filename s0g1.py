# The first sprite in the encyclopedia
# fields: name, color, radius, x, y, vx, vy

import pygame
import sys

pygame.init()

screen_width = 800
screen_height = 600
white = (255, 255, 255)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sprite Movement")

circle_color = (0, 0, 0)
circle_radius = 20
circle_pos = [screen_width // 2, screen_height // 2]

speed = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and circle_pos[0] - circle_radius > 0:
        circle_pos[0] -= speed
    if keys[pygame.K_RIGHT] and circle_pos[0] + circle_radius < screen_width:
        circle_pos[0] += speed
    if keys[pygame.K_UP] and circle_pos[1] - circle_radius > 0:
        circle_pos[1] -= speed
    if keys[pygame.K_DOWN] and circle_pos[1] + circle_radius < screen_height:
        circle_pos[1] += speed

    screen.fill(white)
    pygame.draw.circle(screen, circle_color, circle_pos, circle_radius)
    pygame.display.flip()
    pygame.time.Clock().tick(60)