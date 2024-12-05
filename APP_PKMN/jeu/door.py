import pygame


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, target_map, target_x, target_y, hitbox=None):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 0))  # Une couleur visible pour la porte (peut être remplacée par une image).
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.target_map = target_map
        self.target_x = target_x
        self.target_y = target_y

        # Utilise une hitbox personnalisée si fournie, sinon ça utilise la taille de l'image
        if hitbox:
            self.hitbox = pygame.Rect(x + hitbox[0], y + hitbox[1], hitbox[2], hitbox[3])
        else:
            self.hitbox = self.rect

    def update(self):
        # Pour mettre à jour la hitbox indépendamment de l'image
        self.hitbox.topleft = self.rect.topleft
