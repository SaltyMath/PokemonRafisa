import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, alpha=255):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((63, 51, 37))  # Couleur brune pour les murs
        self.image.set_alpha(alpha)  # Mur transparent
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
