import pygame
from pokemon import Pokemon
import time


class Combat:
    def __init__(self, screen, player_team, trainer_team, background_image):
        self.screen = screen
        self.player_team = player_team
        self.trainer_team = trainer_team
        self.current_player_pokemon_index = 0
        self.current_trainer_pokemon_index = 0
        self.current_player_pokemon = player_team[self.current_player_pokemon_index]
        self.current_trainer_pokemon = trainer_team[self.current_trainer_pokemon_index]
        self.font = pygame.font.Font(None, 36)
        self.in_battle = True

        # Charger les sprites des Pokémon
        self.player_sprites = [pygame.image.load(pokemon.image_path).convert_alpha() for pokemon in player_team]
        self.trainer_sprites = [pygame.image.load(pokemon.image_path).convert_alpha() for pokemon in trainer_team]

        # Charger l'image de background
        self.background_image = pygame.image.load(background_image).convert_alpha()

        # Texte temporaire pour afficher le nom de l'attaque
        self.attack_message = ""
        self.message_timer = 0
        self.message_duration = 2  # Durée en secondes pendant laquelle le message est affiché

        # Variables pour gérer la fin du combat
        self.end_battle_message = ""
        self.end_battle_timer = 0
        self.end_battle_duration = 3  # Durée en secondes avant la fin du combat

    def run(self):
        while self.in_battle:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.in_battle = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.player_attack(0)
                    elif event.key == pygame.K_2:
                        self.player_attack(1)
                    elif event.key == pygame.K_3:
                        self.player_attack(2)
                    elif event.key == pygame.K_4:
                        self.player_attack(3)

            self.update()
            self.draw()
            pygame.display.flip()

            if self.is_game_over():
                self.in_battle = False
                return 'game_over'

    def update(self):
        if self.current_trainer_pokemon.is_ko():
            self.current_trainer_pokemon_index += 1
            if self.current_trainer_pokemon_index < len(self.trainer_team):
                self.current_trainer_pokemon = self.trainer_team[self.current_trainer_pokemon_index]
            else:
                self.in_battle = False

        if self.current_player_pokemon.is_ko():
            self.current_player_pokemon_index += 1
            if self.current_player_pokemon_index < len(self.player_team):
                self.current_player_pokemon = self.player_team[self.current_player_pokemon_index]
            else:
                self.in_battle = False

        # Mettre à jour le timer pour le message d'attaque
        if self.message_timer > 0:
            self.message_timer -= 1

    def player_attack(self, attack_index):
        if attack_index < len(self.current_player_pokemon.attacks):
            attack = self.current_player_pokemon.attacks[attack_index]
            damage = attack.calculate_damage(self.current_player_pokemon, self.current_trainer_pokemon)
            self.current_trainer_pokemon.take_damage(damage)
            self.set_attack_message(f"{self.current_player_pokemon.name} used {attack.name}!")
            if not self.current_trainer_pokemon.is_ko():
                self.trainer_attack()

    def trainer_attack(self):
        attack = self.current_trainer_pokemon.attacks[0]
        damage = attack.calculate_damage(self.current_trainer_pokemon, self.current_player_pokemon)
        self.current_player_pokemon.take_damage(damage)
        self.set_attack_message(f"{self.current_trainer_pokemon.name} used {attack.name}!")

    def set_attack_message(self, message):
        self.attack_message = message
        self.message_timer = self.message_duration * 240  # Convertir la durée en frames (en supposant 60 FPS)

    def draw(self):
        # Afficher l'image de background
        self.screen.blit(self.background_image, (0, 0))

        # Afficher les informations de combat avec un rectangle blanc pour les PV
        if self.current_player_pokemon_index < len(self.player_team):
            player_text = f"{self.current_player_pokemon.name}: {self.current_player_pokemon.current_hp}/{self.current_player_pokemon.max_hp} HP"
            player_text_surface = self.font.render(player_text, True, (0, 0, 0))
            player_text_rect = player_text_surface.get_rect(topleft=(50, 350))
            pygame.draw.rect(self.screen, (255, 255, 255), player_text_rect.inflate(10, 10))
            self.screen.blit(player_text_surface, player_text_rect)

        if self.current_trainer_pokemon_index < len(self.trainer_team):
            trainer_text = f"{self.current_trainer_pokemon.name}: {self.current_trainer_pokemon.current_hp}/{self.current_trainer_pokemon.max_hp} HP"
            trainer_text_surface = self.font.render(trainer_text, True, (0, 0, 0))
            trainer_text_rect = trainer_text_surface.get_rect(topleft=(560, 120))
            pygame.draw.rect(self.screen, (255, 255, 255), trainer_text_rect.inflate(10, 10))
            self.screen.blit(trainer_text_surface, trainer_text_rect)

        # Afficher les sprites des Pokémon actuels (descendre les sprites)
        if self.current_player_pokemon_index < len(self.player_sprites):
            player_sprite = self.player_sprites[self.current_player_pokemon_index]
            player_sprite_rect = player_sprite.get_rect(center=(150, 556))
            self.screen.blit(player_sprite, player_sprite_rect)

        if self.current_trainer_pokemon_index < len(self.trainer_sprites):
            trainer_sprite = self.trainer_sprites[self.current_trainer_pokemon_index]
            trainer_sprite_rect = trainer_sprite.get_rect(center=(680, 270))
            self.screen.blit(trainer_sprite, trainer_sprite_rect)

        # Afficher les textes des attaques en bas de l'écran
        for i, attack in enumerate(self.current_player_pokemon.attacks):
            attack_text = self.font.render(f"{i + 1}. {attack.name}", True, (0, 0, 0))
            attack_text_rect = attack_text.get_rect(topleft=(50, 690 + i * 30))
            pygame.draw.rect(self.screen, (255, 255, 255), attack_text_rect.inflate(10, 10))
            self.screen.blit(attack_text, attack_text_rect)

        # Afficher le message d'attaque
        if self.message_timer > 0:
            message_surface = self.font.render(self.attack_message, True, (0, 0, 0))
            message_rect = message_surface.get_rect(center=(self.screen.get_width() / 2, 550))
            pygame.draw.rect(self.screen, (255, 255, 255), message_rect.inflate(20, 20))
            self.screen.blit(message_surface, message_rect)

    def is_game_over(self):
        return all(pokemon.is_ko() for pokemon in self.player_team)
