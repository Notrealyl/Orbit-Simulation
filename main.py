import pygame
import random
import math

#------------------------------------------------------------------------------
fps = 30

dt = 0.01

screen_width, screen_height = 1200, 600

center_x = screen_width // 2
center_y = screen_height // 2
#------------------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Orbit Simulation")
clock = pygame.time.Clock()
running = True

#----------------------------------Gravitational Force Function----------------------------------------
def gravitational_force(m1, m2, r):
    G = 6.67430e-11 # gravitational constant in m^3 kg^-1 s^-2
    return G * (m1 * m2) / r**2

def base_velocity(m1, r):
    G = 6.67430e-11 # gravitational constant in m^3 kg^-1 s^-2
    return math.sqrt(G * m1 / r)
#------------------------------------------------------------------------------------

#---------------------------------Celestial Bodies-----------------------------------------
distance_from_sun = center_x

sun_diameter = 1391400 / 15000 # scale down by 15000, 15000:1
sun_radius = int(sun_diameter / 2)

mercury_diameter = 4879 / 1000 # scale down by 1000, 1000:1
mercury_radius = int(mercury_diameter / 2)

venus_diameter = 12104 / 1000 # scale down by 1000, 1000:1
venus_radius = int(venus_diameter / 2)

earth_diameter = 12742 / 1000 # scale down by 1000, 1000:1
earth_radius = int(earth_diameter / 2)
#-------------------------------------Celestial Bodies Mass-----------------------------------------------------
sun_mass = 1.989e30 # in kg
mercury_mass = 3.285e23 # in kg
venus_mass = 4.867e24 # in kg
earth_mass = 5.972e24 # in kg
#----------------------------------Celestial Bodies Vector--------------------------------------------------------
sun_pos = pygame.Vector2(distance_from_sun, 300)
mercury_pos = pygame.Vector2(distance_from_sun + 57, 300)
venus_pos = pygame.Vector2(distance_from_sun + 108, 300)
earth_pos = pygame.Vector2(distance_from_sun + 150, 300)
#-------------------------------------------------------------------------------------------------------------


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    pygame.display.flip()
    clock.tick(fps) #FPS