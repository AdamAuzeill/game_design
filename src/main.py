import pygame

# One change
# Constants
CIEL = (0, 200, 255)
RED = (200, 0, 0)
GREEN = (0, 170, 0)
BROWN = (170, 100, 0)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
GRAVITY = 0.15
VELOCITY = 0.5
MAX_LEVEL_X = 700
MIN_LEVEL_X = -60
MAX_LEVEL_Y = 100
MIN_LEVEL_Y = -100
MAX_VEL_Y = 10

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Load images
cursor = pygame.image.load("assets/Images/mouse-pointer-icon-32x32.png")
# cursor = pygame.transform.scale(cursor, (30, 30))
personnage = pygame.image.load("assets/Images/personnage.png")
PERSONNAGE_HEIGHT = 100
PERSONNAGE_WIDTH = 100
personnage = pygame.transform.scale(personnage, (PERSONNAGE_WIDTH, PERSONNAGE_HEIGHT))

# Screen initialization
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class Player:
    def __init__(self, surface, pos_x, pos_y):
        self.surface = surface
        self.rect = surface.get_rect()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = self.rect.width
        self.height = self.rect.height
        self.vel_x = 0
        self.vel_y = 0
        self.can_jump = True

    def move_right(self):
        self.vel_x += VELOCITY

    def move_left(self):
        self.vel_x -= VELOCITY

    def jump(self):
        is_touching_ground = False
        for terrain in list_terrain:
            if terrain.rect.colliderect(self.pos_x, self.pos_y + self.height, self.width, 1):
                is_touching_ground = True
        if is_touching_ground and self.vel_y == 0:
            self.vel_y += -6

    def update_position(self):
        # updates velocities
        self.vel_x *= 0.9
        self.vel_y += GRAVITY

        if self.vel_y < -MAX_VEL_Y:
            self.vel_y = -MAX_VEL_Y
        if self.vel_y > MAX_VEL_Y:
            self.vel_y = MAX_VEL_Y

        # initiate
        dx = round(self.vel_x)
        dy = round(self.vel_y)

        # collision check
        for terrain in list_terrain:
            terrain_rect = pygame.Rect(terrain.pos_x, terrain.pos_y, terrain.width, terrain.height)

            # collision on the x axis
            if terrain_rect.colliderect(self.pos_x + dx, self.pos_y, self.width, self.height):
                if self.vel_x < 0:
                    self.vel_x = 0
                    dx = terrain.pos_x + terrain.width - self.pos_x

                elif self.vel_x >= 0:
                    self.vel_x = 0
                    dx = terrain.pos_x - (self.pos_x + self.width)

            # collision on the y axis
            if terrain_rect.colliderect(self.pos_x, self.pos_y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = terrain.pos_y + terrain.height - self.pos_y
                    self.vel_y = 0

                elif self.vel_y >= 0:
                    dy = terrain.pos_y - (self.pos_y + self.height)
                    self.vel_y = 0

        # applies change position
        self.pos_x += dx
        self.pos_y += dy


class Box:
    def __init__(self, pos_x, pos_y, width, height, color=(0, 0, 0), surface = False):
        if surface == False:
            self.surface = pygame.Surface((width, height))
            self.surface.fill(color)
        else:
            self.surface = surface
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.rect = self.surface.get_rect(topleft=(self.pos_x, self.pos_y))



# Initialize the player
Bob = Player(personnage, 100, 100)

# Initialize the terrain
ground = Box(-150, 400, WINDOW_WIDTH + 400, 80, GREEN)
box_1 = Box(300, 325, 75, 75, BROWN)
box_2 = Box(450, 300, 100, 100, RED)
box_3 = Box(570, 200, 50, 50)
list_terrain = [ground, box_1, box_2, box_3]


def main():
    camera_x = 0
    camera_y = 0

    loop = True
    while loop:
        if MIN_LEVEL_X < Bob.pos_x < MAX_LEVEL_X:
            camera_x = -Bob.pos_x + 270
        if MIN_LEVEL_Y < Bob.pos_y < MAX_LEVEL_Y:
            camera_y = -Bob.pos_y + 120

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            Bob.move_left()
        if keys[pygame.K_d]:
            Bob.move_right()
        if keys[pygame.K_SPACE]:
            Bob.jump()

        if keys[pygame.K_s]:
            Bob.vel_y = 0
        if keys[pygame.K_h]:
            Bob.pos_y -= 10

        Bob.update_position()

        draw_everything(camera_x, camera_y)

        pygame.display.flip()
        clock.tick(60)


def draw_everything(camera_x, camera_y):
    cam = (camera_x, camera_y)
    screen.fill(CIEL)
    for terrain in list_terrain:
        draw_object(terrain, cam)
    draw_object(Bob, cam)
    draw_cursor()


def draw_object(obj, cam=(0, 0)):
    screen.blit(obj.surface, (obj.pos_x + cam[0], obj.pos_y + cam[1]))


def draw_cursor():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.mouse.set_visible(False)
    screen.blit(cursor, (mouse_x, mouse_y))


if __name__ == '__main__':
    main()
