import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GRAVITATIONAL SLINGSHOT EFFECT")

planet_mass = 150
ship_mass = 5
g = 10
FPS = 60
planet_size = 100
obj_size = 5
vel_scale = 100

bg = pygame.transform.scale(pygame.image.load("background.png"),(WIDTH, HEIGHT))
planet = pygame.transform.scale(pygame.image.load("planet.png"),(planet_size *2,planet_size * 2))

white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)

class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        win.blit(planet,(self.x - planet_size, self.y - planet_size))
class rocket:
    def __init__(self, x, y, vel_x, vel_y,mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet = None):
        distance = math.sqrt((self.x-planet.x)**2 + (self.y - planet.y)**2)
        force = (g * self.mass * planet.mass)/distance **2

        acc = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acc_x = acc * math.cos(angle)
        acc_y = acc * math.sin(angle)

        self.vel_x += acc_x
        self.vel_y += acc_y

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        pygame.draw.circle(win, red, (int(self.x), int(self.y)),obj_size)

def create_ship(location, mouse):
    t_x,t_y = location
    m_x,m_y = mouse
    vel_x = (m_x - t_x)/vel_scale
    vel_y = (m_y - t_y)/vel_scale
    obj = rocket(t_x,t_y,vel_x,vel_y, ship_mass)
    return  obj

def draw_input_fields():
    font = pygame.font.Font( None, 36)

    # Display labels
    label_planet_mass = font.render("Planet Mass :", True, white)
    label_ship_mass = font.render("Ship Mass :", True, white)
    label_g = font.render("Gravity (g) :", True, white)

    win.blit(label_planet_mass, (10, 10))
    win.blit(label_ship_mass, (10, 50))
    win.blit(label_g, (10, 90))

    # Create input fields
    input_field_planet_mass = font.render(str(planet_mass), True, white)
    input_field_ship_mass = font.render(str(ship_mass), True, white)
    input_field_g = font.render(str(g), True, white)

    win.blit(input_field_planet_mass, (200, 10))
    win.blit(input_field_ship_mass, (200, 50))
    win.blit(input_field_g, (200, 90))




def main():
    running = True
    clock = pygame.time.Clock()

    planet = Planet(WIDTH//2, HEIGHT//2, planet_mass)
    objects = []
    temp_obj_pos = None

    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:


                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        win.blit(bg,(0,0))

        if temp_obj_pos:
            pygame.draw.line(win,white, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, red, temp_obj_pos, obj_size)

        for obj in objects[:]:
            obj.draw()
            obj.move(planet)
            collide = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= planet_size

            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            if off_screen or collide:
                objects.remove(obj)

        planet.draw()
        draw_input_fields()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
