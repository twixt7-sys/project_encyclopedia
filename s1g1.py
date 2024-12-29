import pygame

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Particle:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.vx = speed
        self.vy = speed

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vx = -self.vx
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.vy = -self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

def check_collision(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    distance = (dx ** 2 + dy ** 2) ** 0.5
    return distance < p1.radius + p2.radius

def handle_collision(p1, p2):
    p1.vx, p2.vx = p2.vx, p1.vx
    p1.vy, p2.vy = p2.vy, p1.vy

class GameScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Particle Collision Simulation")
        self.particles = [
            Particle(WIDTH // 4, HEIGHT // 2, 20, WHITE, 5),
            Particle(3 * WIDTH // 4, HEIGHT // 2, 20, WHITE, 5)
        ]
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            for particle in self.particles:
                particle.move()

            if check_collision(self.particles[0], self.particles[1]):
                handle_collision(self.particles[0], self.particles[1])

            self.screen.fill(BLACK)
            for particle in self.particles:
                particle.draw(self.screen)
            pygame.display.flip()

            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    game_screen = GameScreen()
    game_screen.run()
    pygame.quit()