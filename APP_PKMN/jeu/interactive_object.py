import pygame


class InteractiveObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, message, image_path=None, heal=False):
        super().__init__()
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill((255, 255, 0))  # Couleur jaune par défaut
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.message = message
        self.heal = heal  # Attribut pour indiquer si l'objet peut soigner

    def interact(self, player):
        if self.heal:
            player.heal_pokemon()
        return self.message
