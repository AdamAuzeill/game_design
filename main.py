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
cursor = pygame.image.load("mouse-pointer-icon-32x32.png")
#cursor = pygame.transform.scale(cursor, (30, 30))
personnage = pygame.image.load("personnage.png")
PERSONNAGE_HEIGHT = 100
PERSONNAGE_WIDTH = 100
personnage = pygame.transform.scale(personnage, (PERSONNAGE_WIDTH, PERSONNAGE_HEIGHT))

# Screen initialization
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

class Player:
    def __init__(self, surface, pos_x, pos_y, width, height):
        self.surface = surface
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.vel_x = 0
        self.vel_y = 0
        self.can_jump = True

    def upper_hitbox(self):
        return pygame.Rect(self.pos_x + self.width * 0.05, self.pos_y, self.width * 0.9, self.height * 0.05)

    def lower_hitbox(self):
        return pygame.Rect(self.pos_x + self.width * 0.05, self.pos_y + self.height * 0.95, self.width * 0.9, self.height * 0.05)

    def left_hitbox(self):
        return pygame.Rect(self.pos_x, self.pos_y + self.height * 0.1, self.width * 0.1, self.height * 0.8)

    def right_hitbox(self):
        return pygame.Rect(self.pos_x + self.width * 0.9, self.pos_y + self.height * 0.1, self.width * 0.1, self.height * 0.8)

    def get_surface(self):
        return self.surface

    def get_x(self):
        return self.pos_x

    def set_x(self, new_x):
        self.pos_x = new_x

    def get_y(self):
        return self.pos_y

    def set_y(self, new_y):
        self.pos_y = new_y

    def move_right(self):
        self.vel_x += VELOCITY

    def move_left(self):
        self.vel_x -= VELOCITY

    def jump(self):
        if self.can_jump:
            self.vel_y = -6
            self.can_jump = False

    def update_position(self):
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

        self.vel_x *= 0.9
        self.vel_y += GRAVITY
        if self.vel_y < -MAX_VEL_Y:
            self.vel_y = -MAX_VEL_Y
        if self.vel_y > MAX_VEL_Y:
            self.vel_y = MAX_VEL_Y

class Box:
    def __init__(self, pos_x, pos_y, width, height, color=(0, 0, 0)):
        self.surface = pygame.Surface((width, height))
        self.surface.fill(color)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

    def check_collision(self, player):
        player_rect = pygame.Rect(player.get_x(), player.get_y(), player.width, player.height)
        box_rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

        if player_rect.colliderect(box_rect):
            if player.vel_y > 0 and player.lower_hitbox().colliderect(box_rect):
                player.set_y(self.pos_y - player.height)
                player.vel_y = 0
                player.can_jump = True
            elif player.vel_y < 0 and player.upper_hitbox().colliderect(box_rect):
                player.set_y(self.pos_y + self.height)
                player.vel_y = 0
            elif player.vel_x > 0 and player.right_hitbox().colliderect(box_rect):
                player.set_x(self.pos_x - player.width)
                player.vel_x = 0
            elif player.vel_x < 0 and player.left_hitbox().colliderect(box_rect):
                player.set_x(self.pos_x + self.width)
                player.vel_x = 0

    def get_surface(self):
        return self.surface

    def get_x(self):
        return self.pos_x

    def get_y(self):
        return self.pos_y

# Initialize the player
Bob = Player(personnage, 100, 100, PERSONNAGE_WIDTH, PERSONNAGE_HEIGHT)

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
        if MIN_LEVEL_X < Bob.get_x() < MAX_LEVEL_X:
            camera_x = -Bob.get_x() + 270
        if MIN_LEVEL_Y < Bob.get_y() < MAX_LEVEL_Y:
            camera_y = -Bob.get_y() + 120

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

        for terrain in list_terrain:
            terrain.check_collision(Bob)

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
    screen.blit(obj.get_surface(), (obj.get_x() + cam[0], obj.get_y() + cam[1]))

def draw_cursor():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.mouse.set_visible(False)
    screen.blit(cursor, (mouse_x, mouse_y))

if __name__ == '__main__':
    main()
