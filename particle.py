import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
WHITE = (180, 180, 255)
BLACK = (0, 0, 0)
PARTICLE_RADIUS = 3
PARTICLE_COLOR = WHITE
PARTICLE_SPEED = 5
GRAVITY = 1
GRID_SIZE = 50

class Particle:
    def __init__(self, x, y, radius, color, speed):
        self.position = [x, y]
        self.radius = radius
        self.color = color
        self.velocity = [speed, speed]
        self.acceleration = [0, GRAVITY]

    def move(self):
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        if self.position[0] - self.radius < 0:
            self.position[0] = self.radius
            self.velocity[0] = -self.velocity[0]
        elif self.position[0] + self.radius > WIDTH:
            self.position[0] = WIDTH - self.radius
            self.velocity[0] = -self.velocity[0]
        if self.position[1] - self.radius < 0:
            self.position[1] = self.radius
            self.velocity[1] = -self.velocity[1]
        elif self.position[1] + self.radius > HEIGHT:
            self.position[1] = HEIGHT - self.radius
            self.velocity[1] = -self.velocity[1]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

def check_collision(p1, p2):
    dx = p1.position[0] - p2.position[0]
    dy = p1.position[1] - p2.position[1]
    distance = (dx ** 2 + dy ** 2) ** 0.5
    return distance < p1.radius + p2.radius + random.randrange(-1, 1)

def handle_collision(p1, p2):
    dx = p1.position[0] - p2.position[0]
    dy = p1.position[1] - p2.position[1]
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if distance == 0:
        return
    overlap = 0.5 * (distance - p1.radius - p2.radius)
    p1.position[0] -= overlap * (p1.position[0] - p2.position[0]) / distance
    p1.position[1] -= overlap * (p1.position[1] - p2.position[1]) / distance
    p2.position[0] += overlap * (p1.position[0] - p2.position[0]) / distance
    p2.position[1] += overlap * (p1.position[1] - p2.position[1]) / distance

    collision_angle = math.atan2(dy, dx)
    collision_angle += random.uniform(-0.1, 0.1)
    speed1 = math.sqrt(p1.velocity[0] ** 2 + p1.velocity[1] ** 2)
    speed2 = math.sqrt(p2.velocity[0] ** 2 + p2.velocity[1] ** 2)
    direction1 = math.atan2(p1.velocity[1], p1.velocity[0])
    direction2 = math.atan2(p2.velocity[1], p2.velocity[0])
    new_velocity_x1 = speed1 * math.cos(direction1 - collision_angle)
    new_velocity_y1 = speed1 * math.sin(direction1 - collision_angle)
    new_velocity_x2 = speed2 * math.cos(direction2 - collision_angle)
    new_velocity_y2 = speed2 * math.sin(direction2 - collision_angle)
    (new_velocity_x1, new_velocity_x2) = (new_velocity_x2, new_velocity_x1)
    energy_loss_factor = 0.9
    p1.velocity[0] = (math.cos(collision_angle) * new_velocity_x1 + math.cos(collision_angle + math.pi / 2) * new_velocity_y1) * energy_loss_factor
    p1.velocity[1] = (math.sin(collision_angle) * new_velocity_x1 + math.sin(collision_angle + math.pi / 2) * new_velocity_y1) * energy_loss_factor
    p2.velocity[0] = (math.cos(collision_angle) * new_velocity_x2 + math.cos(collision_angle + math.pi / 2) * new_velocity_y2) * energy_loss_factor
    p2.velocity[1] = (math.sin(collision_angle) * new_velocity_x2 + math.sin(collision_angle + math.pi / 2) * new_velocity_y2) * energy_loss_factor

class GameScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Particle Collision Simulation")
        self.particles = [
            Particle(j/10 * WIDTH // 3, i/10 * HEIGHT // 3, PARTICLE_RADIUS, PARTICLE_COLOR, PARTICLE_SPEED)
            for i in range(10)
            for j in range(30)
        ]
        for particle in self.particles:
            particle.acceleration = [0, GRAVITY]
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            for particle in self.particles:
                particle.move()

            grid = {}
            for particle in self.particles:
                grid_x = int(particle.position[0] // GRID_SIZE)
                grid_y = int(particle.position[1] // GRID_SIZE)
                if (grid_x, grid_y) not in grid:
                    grid[(grid_x, grid_y)] = []
                grid[(grid_x, grid_y)].append(particle)

            for (grid_x, grid_y), cell_particles in grid.items():
                for i in range(len(cell_particles)):
                    for j in range(i + 1, len(cell_particles)):
                        if check_collision(cell_particles[i], cell_particles[j]):
                            handle_collision(cell_particles[i], cell_particles[j])
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            neighbor_particles = grid.get((grid_x + dx, grid_y + dy), [])
                            for neighbor_particle in neighbor_particles:
                                if check_collision(cell_particles[i], neighbor_particle):
                                    handle_collision(cell_particles[i], neighbor_particle)

            self.screen.fill(BLACK)
            for particle in self.particles:
                particle.draw(self.screen)
            pygame.display.flip()

            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    game_screen = GameScreen()
    game_screen.run()
    pygame.quit()