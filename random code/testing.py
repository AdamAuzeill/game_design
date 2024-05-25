import pygame

# Before you can do much with pygame, you will need to initialize it
pygame.init()
# Init de clock
clock = pygame.time.Clock()

CIEL = 0, 200, 255  # parenthèses inutiles, l'interpréteur reconnaît un tuple

def main():
    fenetre = pygame.display.set_mode((640, 480))

    cursor = pygame.image.load(".venv/cursor-alt-pointer-mouse-icon-2048x2048-b26lpbta.png")
    cursor = pygame.transform.scale(cursor, (30, 30))
    personnage = pygame.image.load(".venv/pixil-frame-0 (1).png")
    personnage_height = 100
    personnage_width = 100
    personnage = pygame.transform.scale(personnage, (personnage_height, personnage_width))
    sol = pygame.rect

    # loop
    loop = True
    # Création d'une image de la taille de la fenêtre
    background = pygame.Surface(fenetre.get_size())
    personnage_x = 100
    personnage_y = 100
    gravity = 0.15
    dy = 0


    while loop:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False



        # Superposition du fond ciel
        background.fill(CIEL)
        fenetre.blit(background, (0, 0))

        # sol
        sol = pygame.Surface((640, 80))
        sol_pos = (100, 200)
        sol_x, sol_y = sol_pos
        fenetre.blit(sol, sol_pos)
        sol_rect = sol.get_rect(topleft=sol_pos)
        sol_toucher = check_collision(sol, sol_x, sol_y, personnage, personnage_x, personnage_y)
        if sol_toucher:
            personnage_y = sol_y - personnage_height
            dy = 0

        if not sol_toucher:
            dy += gravity

        # personnage
        keys = pygame.key.get_pressed()
        personnage_x, personnage_y = mouvement_personnage(keys, personnage_x, personnage_y, sol_toucher, gravity, dy)
        fenetre.blit(personnage, (personnage_x, personnage_y))

        if keys[pygame.K_SPACE] and sol_toucher:
            dy = -6


        # souris
        pygame.mouse.set_visible(False)
        fenetre.blit(cursor, (mouse_x, mouse_y))

        # Rafraîchissement de l'écran
        pygame.display.flip()
        # By calling Clock.tick(10) once per frame, the program will never run
        # at more than 10 frames per second
        clock.tick(60)

def mouvement_personnage(key_list, personnage_x, personnage_y, sol_toucher, gravity, dy):
    new_personnage_x = personnage_x
    new_personnage_y = personnage_y

    if not sol_toucher:
        new_personnage_y += dy


    if key_list[pygame.K_w]:
        new_personnage_y -= 5
    if key_list[pygame.K_s]:
        new_personnage_y += 2
    if key_list[pygame.K_a]:
        new_personnage_x -= 2
    if key_list[pygame.K_d]:
        new_personnage_x += 2

    return new_personnage_x, new_personnage_y

def check_collision(surface1, x1, y1, surface2, x2, y2):
    """
    Check if two surfaces are colliding.

    Args:
        surface1 (pygame.Surface): The first surface.
        x1 (int): The x-coordinate of the first surface.
        y1 (int): The y-coordinate of the first surface.
        surface2 (pygame.Surface): The second surface.
        x2 (int): The x-coordinate of the second surface.
        y2 (int): The y-coordinate of the second surface.

    Returns:
        bool: True if the surfaces are touching, False otherwise.
    """
    rect1 = surface1.get_rect(topleft=(x1, y1))
    rect2 = surface2.get_rect(topleft=(x2, y2))

    return rect1.colliderect(rect2)


if __name__ == '__main__':
    main()