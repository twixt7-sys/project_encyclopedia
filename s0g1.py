# S0 - 1st gen    |    Circle Sprite
# The first sprite in the encyclopedia
# fields: name, color, radius, x, y, vx, vy

import pygame
import sys

pygame.init()

#environment fields
screen_size = [800, 600]
bg_color = (255, 255, 255)

#sprite fields
circle_color = (0, 0, 0)
circle_radius = 20
circle_pos = [screen_size[0] // 2, screen_size[1] // 2]
speed = 5

screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
pygame.display.set_caption("Circle Sprite: S0 - 1st gen")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and circle_pos[0] - circle_radius > 0:
        circle_pos[0] -= speed
    if keys[pygame.K_RIGHT] and circle_pos[0] + circle_radius < screen_size[0]:
        circle_pos[0] += speed
    if keys[pygame.K_UP] and circle_pos[1] - circle_radius > 0:
        circle_pos[1] -= speed
    if keys[pygame.K_DOWN] and circle_pos[1] + circle_radius < screen_size[1]:
        circle_pos[1] += speed

    screen.fill(bg_color)
    pygame.draw.circle(screen, circle_color, circle_pos, circle_radius)
    pygame.display.flip()
    pygame.time.Clock().tick(60)