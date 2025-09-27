import pygame
import random
import math
import time
import matplotlib.pyplot as plt

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

    def __init__(self, x, y, radius, color, mass, name="unknown"): #define initial values
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_from_sun = 0
        self.previous_orbit_angle = None
        self.orbit_completed = 0

        self.eccentricity = 0
        self.eccentricity_history = []
        self.periapsis = 0
        self.apoapsis = 0

        self.time_history = []  # To track time 
        self.speed_history = []
        self.distance_from_sun_history = []
        self.acceleration_history = []

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

            speed_text = FONT.render(f"{round(math.sqrt(self.x_vel**2 + self.y_vel**2) / 1000, 2)}km/s", 1, (255, 255, 255))
            screen.blit(speed_text, (x - speed_text.get_width()/2, y + speed_text.get_height()/2))
        
    def attraction(self, other, x, y): #PHYSICS PART
        distance_x = other.x - x
        distance_y = other.y - y
        distance = math.sqrt(distance_x**2 + distance_y**2) # Pythagorean theorem to find distance between two planets

        if other.sun:
            self.distance_from_sun = distance  # in km

        force = self.G * self.mass * other.mass / distance**2 # F = G * (m1*m2) / r^2, Newton's law of universal gravitation
        theta = math.atan2(distance_y, distance_x) # angle between the two planets, find angle of pull

        force_x = math.cos(theta) * force # F_x = F * cos(theta)
        force_y = math.sin(theta) * force # F_y = F * sin(theta)
        return force_x, force_y 
    
    def derivative(self, planets, x, y, vx, vy): # Calculate derivatives for RK4 method
        total_fx = total_fy = 0 # total force in x and y direction

        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet, x, y) # get force exerted by each planet
            total_fx += fx # sum up all forces in x direction
            total_fy += fy # sum up all forces in y direction

        ax = total_fx / self.mass # F = m * a  =>  a = F / m
        ay = total_fy / self.mass # acceleration in y direction

        return (vx, vy, ax, ay) # return derivatives: dx/dt = vx, dy/dt = vy, dvx/dt = ax, dvy/dt = ay
    
    def rk4_step(self, planets, dt): # Runge-Kutta 4th order method for updating position and velocity
        x, y, vx, vy = self.x, self.y, self.x_vel, self.y_vel # current state
        dt = self.TIMESTEP

        dx1, dy1, dvx1, dvy1 = self.derivative(planets, x, y, vx, vy) # K1 FIRST STEP

        dx2, dy2, dvx2, dvy2 = self.derivative(planets, x + 0.5 * dx1 * dt, y + 0.5 * dy1 * dt, vx + 0.5 * dvx1 * dt, vy + 0.5 * dvy1 * dt) # K2 SECOND STEP, Take half step using K1

        dx3, dy3, dvx3, dvy3 = self.derivative(planets, x + 0.5 * dx2 * dt, y + 0.5 * dy2 * dt, vx + 0.5 * dvx2 * dt, vy + 0.5 * dvy2 * dt) # K3 THIRD STEP, Take half step using K2

        dx4, dy4, dvx4, dvy4 = self.derivative(planets, x + dx3 * dt, y + dy3 * dt, vx + dvx3 * dt, vy + dvy3 * dt) # K4 FOURTH STEP, Take full step using K3

        self.x += (dx1 + 2 * dx2 + 2 * dx3 + dx4) / 6 * dt # Average the slopes to get new position and velocity
        self.y += (dy1 + 2 * dy2 + 2 * dy3 + dy4) / 6 * dt
        self.x_vel += (dvx1 + 2 * dvx2 + 2 * dvx3 + dvx4) / 6 * dt
        self.y_vel += (dvy1 + 2 * dvy2 + 2 * dvy3 + dvy4) / 6 * dt
    
    def update_position(self, planets):
        if Planet.TIMESTEP == 0:
            return  # Skip updating position if paused

        self.rk4_step(planets, Planet.TIMESTEP) # Update position using RK4 method
        self.orbit.append((self.x, self.y))

def main():
    running = True

    #------------------------------------------------------------------------------ PLANETS-
    #Argument: x, y, radius, color, mass
    #AU => Astronomical Unit = distance from Earth to Sun = 149.6 million km

    sun = Planet(0, 0, 15, (255, 255, 0), 1.98892 * 10**30, "Sun")
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 8, (80, 78, 81), 3.30 * 10**23, "Mercury")
    mercury.y_vel = -47.4 * 1000  # 47.4

    venus = Planet(0.723 * Planet.AU, 0, 14, (255, 255, 255), 4.8685 * 10**24, "Venus")
    venus.y_vel = -35.02 * 1000  # 35.02

    earth = Planet(-1 * Planet.AU, 0, 16, (100, 149, 237), 5.9742 * 10**24, "Earth")
    earth.y_vel = 29.783 * 1000  # 29.783 km/s

    mars = Planet(-1.52 * Planet.AU, 0, 12, (188, 39, 50), 6.39 * 10**24, "Mars")
    mars.y_vel = 24.077 * 1000

    ceres = Planet(-2.77 * Planet.AU, 0, 10, (255, 255, 255), 9.393e20, "Ceres")
    ceres.y_vel = 17.9 * 1000
    
    jupiter = Planet(5.2 * Planet.AU, 0, 22, (255, 165, 0), 1.898 * 10**27, "Jupiter")
    jupiter.y_vel = -13.06 * 1000

    saturn = Planet(9.58 * Planet.AU, 0, 20, (210, 180, 140), 5.683 * 10**26, "Saturn")
    saturn.y_vel = -9.68 * 1000

    uranus = Planet(19.2 * Planet.AU, 0, 18, (0, 255, 255), 8.681 * 10**25, "Uranus")
    uranus.y_vel = -6.80 * 1000

    neptune = Planet(30 * Planet.AU, 0, 18, (0, 0, 255), 1.024 * 10**26, "Neptune")
    neptune.y_vel = -5.43 * 1000

    pluto = Planet(39.48 * Planet.AU, 0, 10, (255, 255, 255), 1.30900 * 10**22, "Pluto")
    pluto.y_vel = -4.74 * 1000

    #------------------------------------------------------------------------------ PLANETS-

    planet_data = {
            "name": [],
            "eccentricity": [],
            "periapsis_AU": [],
            "apoapsis_AU": []
    }

    #------------------------------------------------------------------------------ MAIN LOOP-

    planets = [sun, mercury, venus, earth, mars, ceres, jupiter, saturn, uranus, neptune, pluto]

    while running:
        clock.tick(60)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not planet.sun:

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

                # Assign random initial velocities
                new_planet.y_vel = random.uniform(-30000, 30000)
                new_planet.x_vel = random.uniform(-30000, 30000)
                new_planet.name = f"Planet{len(planets)}"
                planets.append(new_planet)
                print(f"Added new planet {new_planet.name} at ({sim_x/Planet.AU:.2f} AU, {sim_y/Planet.AU:.2f} AU) with mass {new_planet.mass:.2e} kg and velocity ({new_planet.x_vel:.2f}, {new_planet.y_vel:.2f}) m/s")
            
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

            orbit_angle = math.atan2(planet.y - sun.y, planet.x - sun.x) # Angle of the planet in its orbit around the sun, Calculate if the planet has completed an orbit
            if not planet.sun:
                if planet.previous_orbit_angle is not None:
                    if (planet.previous_orbit_angle < 0 and orbit_angle >= 0) or (planet.previous_orbit_angle > 0 and orbit_angle <= 0):
                        #print(f"{planet.name} completed an orbit around the sun." f" Total orbits: {planet.orbit_completed + 1}")
                        planet.orbit_completed += 1

                planet.previous_orbit_angle = orbit_angle

            if not planet.sun and planet.orbit_completed >= 1: # Calculate eccentricity, periapsis, and apoapsis after one complete orbit
                planet.periapsis = min(math.sqrt(x**2 + y**2) for x, y in planet.orbit)
                planet.apoapsis = max(math.sqrt(x**2 + y**2) for x, y in planet.orbit)

                planet.eccentricity = (planet.apoapsis - planet.periapsis) / (planet.apoapsis + planet.periapsis)
                #print(f"{planet.name} Eccentricity: {planet.eccentricity}, Periapsis: {planet.periapsis/Planet.AU} AU, Apoapsis: {planet.apoapsis/Planet.AU} AU")

                planet.orbit = planet.orbit[-(5000):] # Keep only the last 5000 points to optimize performance

                planet.eccentricity_history.append(planet.eccentricity)
                
                planet.speed_history.append(math.sqrt(planet.x_vel**2 + planet.y_vel**2))  # Speed in km/s
                planet.distance_from_sun_history.append(planet.distance_from_sun / Planet.AU)  # Distance in AU

                planet.time_history.append(len(planet.time_history) * (Planet.TIMESTEP / 86400))  # Time in days

                if planet.name not in planet_data["name"]: # Store data for plotting
                    planet_data["name"].append(planet.name)
                    planet_data["eccentricity"].append(planet.eccentricity)
                    planet_data["periapsis_AU"].append(planet.periapsis / Planet.AU)
                    planet_data["apoapsis_AU"].append(planet.apoapsis / Planet.AU)

        pygame.display.update() # Update the display

    pygame.quit()

    #<[---------------------------------------------------------------------------------------------------------]>
    #<[---------------------------------------------PLOTTTING PART---------------------------------------------]>
    #<[---------------------------------------------PLOTTTING PART---------------------------------------------]>
    #<[---------------------------------------------------------------------------------------------------------]>

    planet1 = mercury
    planet2 = venus
    planet3 = earth

    #------------------------------------------------------Speed over time-----------------------------------------------------------------------------------
    plt.plot(planet1.time_history, planet1.speed_history, color='blue', label=planet1.name)
    plt.plot(planet2.time_history, planet2.speed_history, color='red', label=planet2.name)
    plt.plot(planet3.time_history, planet3.speed_history, color='green', label=planet3.name)

    plt.xlabel("Time (days)")
    plt.ylabel("Speed")
    plt.title(f"Speed of {planet1.name}, {planet2.name} and {planet3.name}  Over Time")
    plt.grid(True)
    plt.legend()
    plt.show()

    #-------------------------------------------------------Eccentricity over time----------------------------------------------------------------------------------
    plt.plot(planet1.time_history, planet1.eccentricity_history, color='blue', label=planet1.name)
    plt.plot(planet2.time_history, planet2.eccentricity_history, color='red', label=planet2.name)
    plt.plot(planet3.time_history, planet3.eccentricity_history, color='green', label=planet3.name)

    plt.xlabel("Time (days)")
    plt.ylabel("Eccentricity")
    plt.title(f"Eccentricity of {planet1.name}, {planet2.name} and {planet3.name} Over Time")
    plt.grid(True)
    plt.legend()
    plt.show()

    #------------------------------------------------------------Distance from sun over time-----------------------------------------------------------------------------
    plt.plot(planet1.time_history, planet1.distance_from_sun_history, color='blue', label=planet1.name)
    plt.plot(planet2.time_history, planet2.distance_from_sun_history, color='red', label=planet2.name)
    plt.plot(planet3.time_history, planet3.distance_from_sun_history, color='green', label=planet3.name)

    plt.xlabel("Time (days)")
    plt.ylabel("Distance from Sun (AU)")
    plt.title(f"Distance from Sun of {planet1.name}, {planet2.name} and {planet3.name} Over Time")
    plt.grid(True)
    plt.legend()
    plt.show()

main()
