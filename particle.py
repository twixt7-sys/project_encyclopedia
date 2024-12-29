import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
WHITE = (180, 180, 255)
BLACK = (0, 0, 0)
PARTICLE_RADIUS = 2
PARTICLE_COLOR = WHITE
PARTICLE_SPEED = 0
GRAVITY = 0.98
GRID_SIZE = 50
PARTITIONS = (25, 25)
RANDOM_OFFSET = 5
PARTICLE_COUNT = (35, 35)
ENERGY_LOSS = 0.95
MARGIN = (WIDTH/3.5, HEIGHT/9)

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
        self.check_bounds()

    def check_bounds(self):
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
    distance = math.hypot(dx, dy)
    return distance < p1.radius + p2.radius

def handle_collision(p1, p2):
    dx = p1.position[0] - p2.position[0]
    dy = p1.position[1] - p2.position[1]
    distance = math.hypot(dx, dy)
    if distance == 0:
        return
    overlap = 0.5 * (distance - p1.radius - p2.radius)
    p1.position[0] -= overlap * (dx / distance)
    p1.position[1] -= overlap * (dy / distance)
    p2.position[0] += overlap * (dx / distance)
    p2.position[1] += overlap * (dy / distance)

    collision_angle = math.atan2(dy, dx) + random.uniform(-RANDOM_OFFSET, RANDOM_OFFSET) * 0.01
    speed1 = math.hypot(p1.velocity[0], p1.velocity[1])
    speed2 = math.hypot(p2.velocity[0], p2.velocity[1])
    direction1 = math.atan2(p1.velocity[1], p1.velocity[0])
    direction2 = math.atan2(p2.velocity[1], p2.velocity[0])
    new_velocity_x1 = speed1 * math.cos(direction1 - collision_angle)
    new_velocity_y1 = speed1 * math.sin(direction1 - collision_angle)
    new_velocity_x2 = speed2 * math.cos(direction2 - collision_angle)
    new_velocity_y2 = speed2 * math.sin(direction2 - collision_angle)
    (new_velocity_x1, new_velocity_x2) = (new_velocity_x2, new_velocity_x1)
    energy_loss_factor = ENERGY_LOSS + random.uniform(-RANDOM_OFFSET, RANDOM_OFFSET) * 0.01
    p1.velocity[0] = (math.cos(collision_angle) * new_velocity_x1 + math.cos(collision_angle + math.pi / 2) * new_velocity_y1) * energy_loss_factor
    p1.velocity[1] = (math.sin(collision_angle) * new_velocity_x1 + math.sin(collision_angle + math.pi / 2) * new_velocity_y1) * energy_loss_factor
    p2.velocity[0] = (math.cos(collision_angle) * new_velocity_x2 + math.cos(collision_angle + math.pi / 2) * new_velocity_y2) * energy_loss_factor
    p2.velocity[1] = (math.sin(collision_angle) * new_velocity_x2 + math.sin(collision_angle + math.pi / 2) * new_velocity_y2) * energy_loss_factor

class Quadtree:
    def __init__(self, level, bounds):
        if len(bounds) != 4:
            raise ValueError("Bounds should be a tuple of (x, y, width, height)")
        self.level = level
        self.bounds = bounds
        self.objects = []
        self.nodes = []

    def clear(self):
        self.objects = []
        for node in self.nodes:
            node.clear()
        self.nodes = []

    def split(self):
        sub_width = self.bounds[2] // 2
        sub_height = self.bounds[3] // 2
        x, y = self.bounds[0], self.bounds[1]
        self.nodes = [
            Quadtree(self.level + 1, (x, y, sub_width, sub_height)),
            Quadtree(self.level + 1, (x + sub_width, y, sub_width, sub_height)),
            Quadtree(self.level + 1, (x, y + sub_height, sub_width, sub_height)),
            Quadtree(self.level + 1, (x + sub_width, y + sub_height, sub_width, sub_height))
        ]

    def get_index(self, particle):
        index = -1
        vertical_midpoint = self.bounds[0] + self.bounds[2] // 2
        horizontal_midpoint = self.bounds[1] + self.bounds[3] // 2

        top_quadrant = particle.position[1] < horizontal_midpoint
        bottom_quadrant = particle.position[1] > horizontal_midpoint

        if particle.position[0] < vertical_midpoint:
            if top_quadrant:
                index = 0
            elif bottom_quadrant:
                index = 2
        elif particle.position[0] > vertical_midpoint:
            if top_quadrant:
                index = 1
            elif bottom_quadrant:
                index = 3

        return index

    def insert(self, particle):
        if self.nodes:
            index = self.get_index(particle)
            if index != -1:
                self.nodes[index].insert(particle)
                return

        self.objects.append(particle)

        if len(self.objects) > 10 and self.level < 5:
            if not self.nodes:
                self.split()
            i = 0
            while i < len(self.objects):
                index = self.get_index(self.objects[i])
                if index != -1:
                    self.nodes[index].insert(self.objects.pop(i))
                else:
                    i += 1

    def handle_collisions(self):
        for i in range(len(self.objects)):
            for j in range(i + 1, len(self.objects)):
                if check_collision(self.objects[i], self.objects[j]):
                    handle_collision(self.objects[i], self.objects[j])
        for node in self.nodes:
            node.handle_collisions()

class GameScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Particle Collision Simulation")
        self.particles = [
            Particle((j/PARTITIONS[0] * WIDTH // 3) + MARGIN[0], (i/PARTITIONS[1] * HEIGHT // 3) + MARGIN[1], PARTICLE_RADIUS, PARTICLE_COLOR, PARTICLE_SPEED)
            for i in range(PARTICLE_COUNT[0])
            for j in range(PARTICLE_COUNT[1])
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

            quadtree = Quadtree(0, (0, 0, WIDTH, HEIGHT))
            for particle in self.particles:
                quadtree.insert(particle)

            quadtree.handle_collisions()

            self.screen.fill(BLACK)
            for particle in self.particles:
                particle.draw(self.screen)
            pygame.display.flip()

            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    game_screen = GameScreen()
    game_screen.run()
    pygame.quit()