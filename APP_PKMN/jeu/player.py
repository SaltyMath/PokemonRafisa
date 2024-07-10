import pygame
from pokemon import Pokemon


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, pokemon_names):
        super().__init__()
        self.image = pygame.image.load('images_videos/drake.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.team = self.create_pokemon_team(pokemon_names)
        self.speed = 0.6

    def create_pokemon_team(self, pokemon_names):
        return [Pokemon(name, is_player=True) for name in pokemon_names]

    def has_available_pokemon(self):
        return any(pokemon.current_hp > 0 for pokemon in self.team)

    def update(self, keys, trainers, walls):
        old_rect = self.rect.copy()
        move_x, move_y = 0, 0

        if keys[pygame.K_LEFT]:
            move_x = -self.speed
        if keys[pygame.K_RIGHT]:
            move_x = self.speed
        if keys[pygame.K_UP]:
            move_y = -self.speed
        if keys[pygame.K_DOWN]:
            move_y = self.speed

        if move_x != 0 and move_y != 0:
            move_x *= 0.7071
            move_y *= 0.7071

        self.rect.x += move_x
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.x = old_rect.x

        self.rect.y += move_y
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.y = old_rect.y

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 816:
            self.rect.right = 816
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 816:
            self.rect.bottom = 816

    def heal_pokemon(self):
        for pokemon in self.team:
            pokemon.current_hp = pokemon.max_hp
