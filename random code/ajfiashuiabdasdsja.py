import pygame


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


# Example usage
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    surface1 = pygame.Surface((50, 50))
    surface1.fill((255, 0, 0))
    surface2 = pygame.Surface((50, 50))
    surface2.fill((0, 255, 0))

    x1, y1 = 100, 100
    x2, y2 = 130, 130  # Overlapping positions for demonstration

    collision = check_collision(surface1, x1, y1, surface2, x2, y2)
    print("Collision:", collision)  # Should print True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((255, 255, 255))
        screen.blit(surface1, (x1, y1))
        screen.blit(surface2, (x2, y2))
        pygame.display.flip()
