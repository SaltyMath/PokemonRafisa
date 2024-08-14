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

        # Déterminer qui attaque en premier en fonction de la vitesse
        if self.current_player_pokemon.speed > self.current_trainer_pokemon.speed:
            self.is_player_turn = True
        elif self.current_player_pokemon.speed < self.current_trainer_pokemon.speed:
            self.is_player_turn = False
        else:
            # Si les vitesses sont égales, le joueur commence
            self.is_player_turn = True

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
                    self.handle_quit_event()
                elif event.type == pygame.KEYDOWN:
                    if self.is_player_turn:
                        if event.key == pygame.K_1:
                            self.player_attack(0)
                        elif event.key == pygame.K_2:
                            self.player_attack(1)
                        elif event.key == pygame.K_3:
                            self.player_attack(2)
                        elif event.key == pygame.K_4:
                            self.player_attack(3)
                        elif event.key in [pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                            self.change_player_pokemon(event.key)

            self.update()
            self.draw()
            pygame.display.flip()

            if not self.is_player_turn:
                pygame.time.wait(1000)  # Attendre un moment avant que le dresseur attaque
                self.trainer_attack()

            if self.is_game_over():
                self.in_battle = False
                return 'game_over'

    def handle_quit_event(self):
        self.show_quit_confirmation()

    def show_quit_confirmation(self):
        # Créer une surface semi-transparente pour le fond
        overlay = pygame.Surface(self.screen.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)  # 200/255 de transparence

        # Afficher un message de confirmation
        self.screen.blit(overlay, (0, 0))
        font = pygame.font.Font(None, 74)
        confirm_text = font.render('Voulez-vous quitter le combat ?', True, (255, 255, 255))
        self.screen.blit(confirm_text, (self.screen.get_width() // 2 - confirm_text.get_width() // 2,
                                        self.screen.get_height() // 2 - confirm_text.get_height() // 2))

        # Afficher les options
        font_small = pygame.font.Font(None, 36)
        yes_text = font_small.render('Oui [Y]', True, (255, 255, 255))
        no_text = font_small.render('Non [N]', True, (255, 255, 255))
        self.screen.blit(yes_text, (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 50))
        self.screen.blit(no_text, (self.screen.get_width() // 2 + 50, self.screen.get_height() // 2 + 50))

        pygame.display.flip()

        # Boucle pour gérer la réponse
        waiting_for_response = True
        while waiting_for_response:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        self.in_battle = False  # Quitter le combat
                        pygame.quit()  # Fermer Pygame
                        exit()  # Quitter le programme
                    elif event.key == pygame.K_n:
                        waiting_for_response = False  # Revenir au combat

    def change_player_pokemon(self, key):
        key_to_index = {
            pygame.K_5: 0,
            pygame.K_6: 1,
            pygame.K_7: 2,
            pygame.K_8: 3,
            pygame.K_9: 4,
            pygame.K_0: 5
        }

        index = key_to_index.get(key)
        if index is not None and index < len(self.player_team):
            if not self.player_team[index].is_ko():
                self.current_player_pokemon_index = index
                self.current_player_pokemon = self.player_team[self.current_player_pokemon_index]
                # Met à jour les sprites si nécessaire, en fonction du Pokémon sélectionné
                self.is_player_turn = False  # Passer au tour du dresseur après le changement

    def update(self):
        if self.current_trainer_pokemon.is_ko():
            self.current_trainer_pokemon_index += 1
            if self.current_trainer_pokemon_index < len(self.trainer_team):
                self.current_trainer_pokemon = self.trainer_team[self.current_trainer_pokemon_index]
            else:
                # L'équipe du dresseur est KO, le joueur a gagné
                self.in_battle = False
                self.end_battle_message = "You won the battle!"
                return

        if self.current_player_pokemon.is_ko():
            available_pokemon = [pokemon for pokemon in self.player_team if not pokemon.is_ko()]
            if available_pokemon:
                # Si le Pokémon actuel est KO et qu'il y a d'autres Pokémon disponibles,
                # basculer vers le prochain Pokémon disponible
                self.current_player_pokemon = available_pokemon[0]
                self.current_player_pokemon_index = self.player_team.index(self.current_player_pokemon)
            else:
                # Si aucun Pokémon n'est disponible, le joueur a perdu
                self.in_battle = False
                self.end_battle_message = "You lost the battle!"

        # Met à jour le timer pour le message d'attaque
        if self.message_timer > 0:
            self.message_timer -= 1

    def player_attack(self, attack_index):
        if attack_index < len(self.current_player_pokemon.attacks):
            attack = self.current_player_pokemon.attacks[attack_index]
            damage = attack.calculate_damage(self.current_player_pokemon, self.current_trainer_pokemon)
            self.current_trainer_pokemon.take_damage(damage)
            self.set_attack_message(f"{self.current_player_pokemon.name} used {attack.name}!")

            if not self.current_trainer_pokemon.is_ko():
                self.is_player_turn = False  # Le joueur a terminé son tour

    def trainer_attack(self):
        if len(self.current_trainer_pokemon.attacks) > 0:
            attack = self.current_trainer_pokemon.attacks[0]  # Choisis la première attaque disponible
            damage = attack.calculate_damage(self.current_trainer_pokemon, self.current_player_pokemon)
            self.current_player_pokemon.take_damage(damage)
            self.set_attack_message(f"{self.current_trainer_pokemon.name} used {attack.name}!")

            self.is_player_turn = True  # Retour au tour du joueur après l'attaque du dresseur

    def set_attack_message(self, message):
        self.attack_message = message
        self.message_timer = self.message_duration * 240  # Converti la durée en frames (en supposant 60 FPS)

    def draw(self):
        # Affiche l'image de background
        self.screen.blit(self.background_image, (0, 0))

        # Affiche les informations de combat avec un rectangle blanc pour les PV
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

        # Affiche les sprites des Pokémon actuels (descendre les sprites)
        if self.current_player_pokemon_index < len(self.player_sprites):
            player_sprite = self.player_sprites[self.current_player_pokemon_index]
            player_sprite_rect = player_sprite.get_rect(center=(150, 556))
            self.screen.blit(player_sprite, player_sprite_rect)

        if self.current_trainer_pokemon_index < len(self.trainer_sprites):
            trainer_sprite = self.trainer_sprites[self.current_trainer_pokemon_index]
            trainer_sprite_rect = trainer_sprite.get_rect(center=(680, 270))
            self.screen.blit(trainer_sprite, trainer_sprite_rect)

        # Affiche les textes des attaques en bas de l'écran
        for i, attack in enumerate(self.current_player_pokemon.attacks):
            attack_text = self.font.render(f"{i + 1}. {attack.name}", True, (0, 0, 0))
            attack_text_rect = attack_text.get_rect(topleft=(50, 690 + i * 30))
            pygame.draw.rect(self.screen, (255, 255, 255), attack_text_rect.inflate(10, 10))
            self.screen.blit(attack_text, attack_text_rect)

        # Affiche le message d'attaque
        if self.message_timer > 0:
            message_surface = self.font.render(self.attack_message, True, (0, 0, 0))
            message_rect = message_surface.get_rect(center=(self.screen.get_width() / 2, 550))
            pygame.draw.rect(self.screen, (255, 255, 255), message_rect.inflate(20, 20))
            self.screen.blit(message_surface, message_rect)

    def is_game_over(self):
        return all(pokemon.is_ko() for pokemon in self.player_team)
