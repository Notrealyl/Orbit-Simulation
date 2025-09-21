import pygame
import random
import math

#------------------------------------------------------------------------------
fps = 30

dt = 0.01

screen_width, screen_height = 1800, 1000

center_x = screen_width // 2
center_y = screen_height // 2
#------------------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Orbit Simulation")
clock = pygame.time.Clock()

#------------------------------------------------------------------------------

class Planet:
    AU = 149.6e6 * 1000  # Astronomical unit in meters
    G = 6.67428e-11  # Gravitational constant
    SCALE = 250 / AU  # 1 AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day in seconds

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_from_sun = 0

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, screen):
        x = self.x * self.SCALE + center_x
        y = self.y * self.SCALE + center_y

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + center_x
                y = y * self.SCALE + center_y
                updated_points.append((x, y))

            pygame.draw.lines(screen, self.color, False, updated_points, 2)

        pygame.draw.circle(screen, self.color, (x, y), self.radius)

        if not self.sun:
            FONT = pygame.font.SysFont("comicsans", 16)
            distance_text = FONT.render(f"{round(self.distance_from_sun / 149597870700, 5)}au", 1, (255, 255, 255))
            screen.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

            speed_text = FONT.render(f"{round(math.sqrt(self.x_vel**2 + self.y_vel**2), 2)}km/s", 1, (255, 255, 255))
            screen.blit(speed_text, (x - speed_text.get_width()/2, y + speed_text.get_height()/2))
        
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_from_sun = distance  # in km

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    running = True

    sun = Planet(0, 0, 30, (255, 255, 0), 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, (100, 149, 237), 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000  # 29.783 km/s

    mars = Planet(-1.52 * Planet.AU, 0, 12, (188, 39, 50), 6.39 * 10**24)
    mars.y_vel = 24.077 * 1000

    planets = [sun, earth, mars]

    while running:
        clock.tick(60)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                mouse_x, mouse_y = event.pos
                # Convert screen coordinates to simulation coordinates
                sim_x = (mouse_x - center_x) / Planet.SCALE
                sim_y = (mouse_y - center_y) / Planet.SCALE
                # Create a new planet with random color, radius, and mass
                new_planet = Planet(
                    sim_x, sim_y,
                    random.randint(5, 15),
                    (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
                    random.uniform(1e23, 1e25)  # Mass between 10^23 and 10^25 kg
                )
                # Optionally, set an initial velocity
                new_planet.y_vel = random.uniform(-30000, 30000)
                new_planet.x_vel = random.uniform(-30000, 30000)
                planets.append(new_planet)

        for planet in planets:
            planet.update_position(planets)
            planet.draw(screen)

        periapsis = 0
        apoapsis = 0

        pygame.display.update()

    pygame.quit()

main()

'''
        for planet in planets:
            if planet.sun and len(planet) > 0:
                continue
            if planet != sun:
                distance_x = sun.x - planet[len(planet)].x 
                distance_y = sun.y - planet[len(planet)].y

                distance = math.sqrt(distance_x**2 + distance_y**2)

            if not hasattr(planet, "distances"):
                planet.distances = []
                planet.distances.append(distance)

            for planet in planets:
                if planet.sun:
                    continue
                periapsis = min(planet.distances)
                apoapsis = max(planet.distances)
             print(f"{planet} periapsis: {periapsis}, apoapsis: {apoapsis}")
'''
