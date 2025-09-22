import pygame
import random
import math

#------------------------------------------------------------------------------
fps = 30

dt = 0.01

screen_width, screen_height = 1800, 1000

center_x = screen_width // 2
center_y = screen_height // 2

scale_radius = 0.5

#------------------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Orbit Simulation")
clock = pygame.time.Clock()

#------------------------------------------------------------------------------

class Planet: # Class to represent a planet
    AU = 149.6e6 * 1000  # Astronomical unit in meters
    G = 6.67428e-11  # Gravitational constant
    SCALE = 50 / AU  # Define AU which can be changed
    TIMESTEP = 3600 * 24  # 1 day in seconds

    def __init__(self, x, y, radius, color, mass): #define initial values
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
    
    def draw(self, screen): #draw the planet
        x = self.x * self.SCALE + center_x
        y = self.y * self.SCALE + center_y

        if len(self.orbit) > 2: #if orbit has more than 2 points
            updated_points = [] #list to store updated points
            for point in self.orbit: #for each point in orbit
                x, y = point 
                x = x * self.SCALE + center_x #scale and center the coordinates
                y = y * self.SCALE + center_y 
                updated_points.append((x, y)) #add updated point to list

            pygame.draw.lines(screen, self.color, False, updated_points, 2) #draw orbit line

        pygame.draw.circle(screen, self.color, (x, y), self.radius * scale_radius) #draw the planet

        if not self.sun:
            FONT = pygame.font.SysFont("comicsans", max(12, int(16 * (Planet.SCALE * 1e9))))
            distance_text = FONT.render(f"{round(self.distance_from_sun / 149597870700, 5)}au", 1, (255, 255, 255))
            screen.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

            speed_text = FONT.render(f"{round(math.sqrt(self.x_vel**2 + self.y_vel**2), 2)}km/s", 1, (255, 255, 255))
            screen.blit(speed_text, (x - speed_text.get_width()/2, y + speed_text.get_height()/2))
        
    def attraction(self, other): #PHYSICS PART
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2) # Pythagorean theorem to find distance between two planets

        if other.sun:
            self.distance_from_sun = distance  # in km

        force = self.G * self.mass * other.mass / distance**2 # F = G * (m1*m2) / r^2, Newton's law of universal gravitation
        theta = math.atan2(distance_y, distance_x) # angle between the two planets, find angle of pull

        force_x = math.cos(theta) * force # F_x = F * cos(theta)
        force_y = math.sin(theta) * force # F_y = F * sin(theta)
        return force_x, force_y 
    
    def update_position(self, planets):
        total_fx = total_fy = 0 # total force in x and y direction
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet) # get force exerted by each planet
            total_fx += fx # sum up all forces in x direction
            total_fy += fy # sum up all forces in y direction

        self.x_vel += total_fx / self.mass * self.TIMESTEP # F = m * a  =>  a = F / m  =>  v = a * t
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP # delta x = v_x * t =>  new x = old x + delta x
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    running = True

    #------------------------------------------------------------------------------ PLANETS-
    #Argument: x, y, radius, color, mass
    #AU => Astronomical Unit = distance from Earth to Sun = 149.6 million km

    sun = Planet(0, 0, 15, (255, 255, 0), 1.98892 * 10**30)
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 8, (80, 78, 81), 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000  # 47.4

    venus = Planet(0.723 * Planet.AU, 0, 14, (255, 255, 255), 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000  # 35.02

    earth = Planet(-1 * Planet.AU, 0, 16, (100, 149, 237), 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000  # 29.783 km/s

    mars = Planet(-1.52 * Planet.AU, 0, 12, (188, 39, 50), 6.39 * 10**24)
    mars.y_vel = 24.077 * 1000

    ceres = Planet(-2.77 * Planet.AU, 0, 10, (255, 255, 255), 9.393e20)
    ceres.y_vel = 17.9 * 1000
    
    jupiter = Planet(5.2 * Planet.AU, 0, 22, (255, 165, 0), 1.898 * 10**27)
    jupiter.y_vel = -13.06 * 1000

    saturn = Planet(9.58 * Planet.AU, 0, 20, (210, 180, 140), 5.683 * 10**26)
    saturn.y_vel = -9.68 * 1000

    uranus = Planet(19.2 * Planet.AU, 0, 18, (0, 255, 255), 8.681 * 10**25)
    uranus.y_vel = -6.80 * 1000

    neptune = Planet(30 * Planet.AU, 0, 18, (0, 0, 255), 1.024 * 10**26)
    neptune.y_vel = -5.43 * 1000

    pluto = Planet(39.48 * Planet.AU, 0, 10, (255, 255, 255), 1.30900 * 10**22)
    pluto.y_vel = -4.74 * 1000

    #------------------------------------------------------------------------------ PLANETS-

    planets = [sun, mercury, venus, earth, mars, ceres, jupiter, saturn, uranus, neptune, pluto]

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

                closest_planet = min(planets, key=lambda p: math.hypot(p.x * Planet.SCALE + center_x - mouse_x, p.y * Planet.SCALE + center_y - mouse_y))

                newspd = random.uniform(-5000, 5000)

                closest_planet.x_vel += newspd
                closest_planet.y_vel += newspd

                # Create a new planet with random color, radius, and mass
                ''' 
                new_planet = Planet(
                    sim_x, sim_y,
                    random.randint(5, 15),
                    (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
                    random.uniform(1e23, 1e25)  # Mass between 10^23 and 10^25 kg
                )

                # Assign random initial velocities
                new_planet.y_vel = random.uniform(-30000, 30000)
                new_planet.x_vel = random.uniform(-30000, 30000)
                planets.append(new_planet)
                '''
            
            if event.type == pygame.MOUSEWHEEL: # Zoom in/out with mouse wheel
                if event.y > 0:
                    Planet.SCALE *= 1.1
                elif event.y < 0:
                    Planet.SCALE /= 1.1

                Planet.SCALE = max(10 / Planet.AU, min(Planet.SCALE, 1000 / Planet.AU)) # Limit zoom levels

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Pause/unpause with spacebar
                    if Planet.TIMESTEP != 0:
                        Planet.TIMESTEP = 0
                    else:
                        Planet.TIMESTEP = 3600 * 24


        for planet in planets: # Update and draw each planet
            planet.update_position(planets)
            planet.draw(screen)

        periapsis = 0
        apoapsis = 0

        pygame.display.update() # Update the display

    pygame.quit()

main()

''' TO BE FIXED LATER
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
'''# TO BE FIXED LATER
