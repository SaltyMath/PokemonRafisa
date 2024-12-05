import pygame
import os
import sqlite3
import time
from title_screen import TitleScreen
from player import Player
from trainer import (Trainer1, Trainer2, Trainer3, Trainer4, Trainer5, Trainer6,
                     Trainer7, Trainer8, Trainer9, Trainer10, Trainer11, Trainer12,
                     Trainer13, Eleve1, Eleve2, Eleve3, Eleve4, Eleve5, Eleve6, Eleve7, Eleve8, Eleve9,
                     Eleve10, Prof1, Prof2, Prof3, Prof4, Prof5, Prof6, Prof7, Doyen)
from dialogue import DialogueBox
from combat import Combat
from map import Map, MapSelector

from interactive_object import InteractiveObject


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path=None):
        super().__init__()
        self.image = pygame.Surface((width, height))
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
        else:
            self.image.fill((0, 0, 0))  # Noir par défaut si aucune image n'est fournie
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def make_transparent(self):
        self.image.set_alpha(0)  # Rends l'image complètement transparente si la condition est remplie
        self.kill()  # Supprime l'obstacle du groupe de sprites si la condition est remplie


class Canape(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 50, 'images_videos/canapé.png')


class Dalle(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, 'images_videos/sol.png')


class InteractiveBus(pygame.sprite.Sprite):
    def __init__(self, x, y, game_instance):
        super().__init__()
        self.image = pygame.image.load('images_videos/bus.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.game_instance = game_instance

    def interact(self, game_instance):
        if game_instance.trainers_defeated[Trainer11]:
            current_map = game_instance.current_map.name
            if current_map == 'Rafisa (extérieur)':
                # Change directement la carte à 'EPSIC (entrée)' avec les coordonnées spécifiées
                game_instance.change_map('EPSIC (entrée)', (384, 1083))
            elif current_map == 'EPSIC (entrée)':
                # Change directement la carte à 'Rafisa (extérieur)' avec les coordonnées spécifiées
                game_instance.change_map('Rafisa (extérieur)', (528, 698))
            return "Vous prenez le bus pour voyager vers un autre endroit."
        else:
            return "Avance dans l'histoire pour me déblo... euh non attends... euh... je suis en panne, reviens plus tard !!"


class SecretDoor(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def interact(self, game_instance):
        # Afficher une image pleine écran et fermer le jeu après 15 secondes
        full_screen_image = pygame.image.load('images_videos/crédits.png').convert()
        game_instance.screen.blit(full_screen_image, (0, 0))
        pygame.display.flip()
        time.sleep(15)  # Attend 15 secondes avant de fermer le jeu
        pygame.quit()
        exit()


class Game:
    def __init__(self, screen, win_width, win_height):
        self.screen = screen
        self.WIN_WIDTH = win_width
        self.WIN_HEIGHT = win_height
        self.all_sprites = pygame.sprite.Group()
        self.trainers = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.current_map = None
        self.maps = {}
        self.dialogue_box = DialogueBox(screen)
        self.in_dialogue = False
        self.in_combat = False
        self.current_trainer = None
        self.battled_trainers = 0  # Nombre de dresseurs battus
        self.trainers_defeated = {  # Initialisation des dresseurs vaincus
            Trainer1: False, Trainer2: False, Trainer3: False, Trainer4: False,
            Trainer5: False, Trainer6: False, Trainer7: False, Trainer8: False,
            Trainer9: False, Trainer10: False, Trainer11: False, Trainer12: False,
            Trainer13: False, Prof1: False, Prof2: False, Prof3: False, Prof4: False,
            Prof5: False, Prof6: False, Prof7: False, Eleve1: False, Eleve2: False,
            Eleve3: False, Eleve4: False, Eleve5: False, Eleve6: False, Eleve7: False,
            Eleve8: False, Eleve9: False, Eleve10: False, Doyen: False
        }

        self.show_title_screen()

        self.trainer11_defeated = False

        # Initialise les cartes
        self.init_maps()

        # Initialise le sélecteur de cartes
        self.map_selector = MapSelector(screen, list(self.maps.keys()))

        # Initialise l'objet bus interactif
        self.init_interactive_bus()

        self.db_path = os.path.join(os.path.dirname(__file__), 'pokemon.db')
        self.player_team = self.select_team_from_db()

        # Initialise le joueur après avoir défini la carte initiale
        self.player = Player(400, 300, self.player_team)  # Position initiale arbitraire
        self.all_sprites.add(self.player)

        # Changer la carte initiale
        self.change_map('Rafisa (extérieur)')

        # Police pour le compteur de dresseurs
        self.font = pygame.font.Font(None, 36)

    def show_title_screen(self):
        title_screen = TitleScreen(self.screen)
        clock = pygame.time.Clock()

        running = True
        while not title_screen.start_game and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            title_screen.update()
            title_screen.draw()
            pygame.display.flip()
            clock.tick(60)

        if not running:
            pygame.quit()
            exit()

    def connect_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def fetch_pokemon_from_db(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM PlayerPokemon")
            pokemon_list = [row[0] for row in cursor.fetchall()]
            conn.close()
            return pokemon_list
        return []

    def select_team_from_db(self):
        available_pokemon = self.fetch_pokemon_from_db()
        if not available_pokemon:
            print("Pokémon introuvable")
            return []

        selected_team = []
        font = pygame.font.Font(None, 30)
        max_columns = 2
        max_pokemon_per_column = 9
        column_width = self.WIN_WIDTH // max_columns
        pokemon_rects = []

        while True:
            self.screen.fill((255, 255, 255))
            pokemon_rects = []

            for i, pokemon in enumerate(available_pokemon):
                column = i // max_pokemon_per_column
                row = i % max_pokemon_per_column
                if column >= max_columns:
                    break
                x = column * column_width + 50
                y = 100 + row * 40
                text_surface = font.render(pokemon, True, (0, 0, 0))

                text_rect = text_surface.get_rect(center=(x + column_width // 2, y))

                self.screen.blit(text_surface, text_rect)

                pokemon_rects.append((text_rect, pokemon))

            selected_team_text = font.render(f"{', '.join(selected_team)}", True, (0, 0, 0))
            selected_team_rect = selected_team_text.get_rect(
                center=(self.WIN_WIDTH // 2, 50))
            self.screen.blit(selected_team_text, selected_team_rect)

            if len(selected_team) >= 1:
                validation_text = font.render("Appuyez sur Entrée pour valider", True, (0, 255, 0))
                remove_info_text = font.render("Appuyez sur 'Supprimer' pour retirer le dernier Pokémon choisi", True,
                                               (0, 255, 0))
            else:
                validation_text = font.render("Choisissez entre 1 et 6 Pokémon en cliquant dessus", True, (255, 0, 0))
                remove_info_text = font.render("Appuyez sur 'Supprimer' pour retirer le dernier Pokémon choisi", True,
                                               (255, 0, 0))

            validation_text_rect = validation_text.get_rect(center=(self.WIN_WIDTH // 2, self.WIN_HEIGHT - 60))

            remove_info_text_rect = remove_info_text.get_rect(
                center=(self.WIN_WIDTH // 2, validation_text_rect.bottom + 20))

            self.screen.blit(validation_text, validation_text_rect)
            self.screen.blit(remove_info_text, remove_info_text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = event.pos
                        if len(selected_team) < 6:
                            for rect, pokemon in pokemon_rects:
                                if rect.collidepoint(mouse_pos):
                                    selected_team.append(pokemon)
                                    break

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and 1 <= len(selected_team) <= 6:
                        return selected_team

                    elif event.key == pygame.K_BACKSPACE and selected_team:
                        selected_team.pop()

    # Position des murs, portes et autres objets
    def init_maps(self):
        # Initialisation des cartes
        outside_walls = [
            (10, -5, 816, 10),  # Mur supérieur
            (15, 811, 816, 10),  # Mur inférieur
            (-5, 0, 10, 816),  # Mur gauche
            (811, 0, 10, 816),  # Mur droit
            (160, 230, 175, 200),  # Forêt 1
            (495, 280, 120, 160),  # Forêt 2
            (540, 320, 60, 180),  # Forêt 3
            (565, 420, 50, 100),  # Forêt 4
            (180, 180, 490, 50),  # hitbox bâtiment
            (0, 130, 220, 50),  # Parking
            (60, 575, 275, 5),  # fleurs b
            (0, 530, 98, 5),  # fleurs h
            (770, 180, 50, 50),  # hitbox voiture retournée 1
            (720, 130, 50, 50),  # hitbox voiture retournée 2
            (670, 80, 50, 50),  # hitbox voiture retournée 3
            (529, 700, 90, 5)
        ]
        outside_doors = [
            (382, 238, 50, 50, 'Rafisa (intérieur)', 310, 645, (0, 0, 30, 5))  # Porte vers l'intérieur
        ]
        inside_walls = [
            (0, 0, 800, 40),  # Mur supérieur
            (-510, 771, 800, 60),  # Mur inférieur gauche
            (380, 771, 800, 60),  # Mur inférieur droit
            (5, 0, 40, 802),  # Mur gauche
            (770, 0, 10, 802),  # Mur de droite
            (245, 481, 40, 802),  # Séparation coin miam-open space (droite)
            (140, 522, 145, 40),  # Séparation cuisine-salle à manger (milieu)
            (-10, 290, 300, 40),  # Séparation salle à manger-open space (haut)
            (580, 240, 400, 40),  # Mur inférieur bureau Tania
            (444, -522, 35, 802),  # Mur côté bureau Tania
            (390, 441, 40, 259),  # Caisses
        ]
        inside_doors = [
            (290, 770, 90, 100, 'Rafisa (extérieur)', 382, 300, (0, 25, 90, 25))  # Porte vers l'extérieur
        ]
        #
        interactive_objects = [
            (144, 626, 48, 46, "Vous avez soigné votre équipe.", 'images_videos/cuisine.png', True),
            (672, 528, 48, 46,
             "C'est mon bureau, le fond d'écran du PC représente le combat qui oppose le général Radahn à Malenia, l'épée de Miquella",
             'images_videos/desk.png', False),
            (624, 528, 48, 46,
             "C'est le bureau de Karim, les dossiers sur son PC forment un crewmate d'Among Us, ou peut-être est-ce l'imposteur ?",
             'images_videos/desk.png', False),
            (672, 478, 48, 46, "C'est le bureau de Nathan, il est propre et bien rangé.", 'images_videos/desk.png',
             False),
            (624, 478, 48, 46, "C'est le bureau de Guillaume, une photo d'Alphacast trône fièrement à côté de son PC.",
             'images_videos/desk.png', False),
            (672, 383, 48, 46, "C'est le bureau de Mario, il travaille très dur sur son site web!",
             'images_videos/desk.png', False),
            (624, 383, 48, 46, "C'est le bureau de Zhi, son PC est en veille.", 'images_videos/desk.png', False),
            (672, 333, 48, 46, "C'est le bureau de Jérôme, un livre de blagues et de jeux de mots est posé sur sa tour.",
             'images_videos/desk.png', False),
            (624, 333, 48, 46, "C'est le bureau de Dylan, il est en train de créer un site web pour un client!",
             'images_videos/desk.png', False),
            (672, 673, 48, 46, "C'est le bureau de Kamilla, un casque anti bruit est posé devant son clavier.",
             'images_videos/desk.png', False),
            (624, 673, 48, 46, "C'était le bureau de Nicolas avant qu'il ne quitte Rafisa.", 'images_videos/desk.png',
             False),
            (672, 623, 48, 46,
             "C'est le bureau d'Angel, ses Blatgel y ont élu domicile! Tout ira bien tant qu'ils ne s'échappent pas à nouveau.",
             'images_videos/desk.png', False),
            (624, 623, 48, 46,
             "C'est le bureau utilisé par les stagiaires, je me demande où est passé celui qui devrait être là cette semaine...",
             'images_videos/desk.png', False),
            (144, 96, 96, 49, "C'est le bureau de Cédric, il est plein de dossiers et de papiers en tout genres.",
             'images_videos/C_desk.png', False),
            (480, 96, 96, 49, "C'est le bureau de Tania, une pile de rapports d'apprentis y est soigneusement posée.",
             'images_videos/T_desk.png', False),
            (95, 175, 49, 96,
             "C'est le bureau de Miguel, évidemment que mettre deux chaises sur son bureau était volontaire !! è_é (signé le dev)",
             'images_videos/M_desk.png', False),
            (145, 432, 48, 46,
             "Le plat sent bon, je me demande si je pourrais préparer un repas pour soigner mon équipe.",
             'images_videos/miam.png', False),
        ]
        epsic_walls = [
            (0, -20, 1440, 65),  # Mur supérieur
            (0, 1200, 1440, 40),  # Mur inférieur
            (-20, 0, 65, 1200),  # Mur gauche
            (1440, 0, 40, 1200),  # Mur droite
            (528, 260, 47, 120),  # Petit mur entrée
            (528, 577, 47, 350),  # Grand mur entrée
            (145, 288, 47, 140),  # Grd mur escalier
            (190, 288, 50, 50),  # Petit mur escalier
            (0, 865, 575, 80),  # Mur inférieur bâtiment
            (-20, 673, 255, 80),  # Mur cuisine
            (528, 240, 1200, 45),  # Mur ext biblio
            (0, 1025, 818, 45),  # Collisions
            (912, 1025, 600, 45),  # Collisions
        ]
        epsic_doors = [
            (192, 390, 28, 37, 'EPSIC (étage 7)', 600, 1200, (0, 0, 10, 10))
        ]
        new_interactive_objects = [  # Objets interactifs
            (48, 767, 48, 46, "Vous avez soigné votre équipe.", 'images_videos/cuisine2.png', True)
        ]
        etage_epsic_walls = [
            (0, 0, 1680, 40),  # Mur supérieur
            (0, 1346, 1680, 40),  # Mur inférieur
            (0, 0, 40, 1440),  # Mur gauche
            (1640, 0, 40, 1440),  # Mur droite
            (670, 1248, 47, 120),  # Escalier milieu
            (530, 1248, 47, 120),  # Escalier gauche
            (810, 1248, 47, 120),  # Escalier droite
            (290, 0, 40, 140),  # Salle 1 bas
            (0, 340, 300, 40),  # Salle 2 haut
            (290, 340, 40, 140),  # Salle 2 bas
            (0, 676, 300, 40),  # Salle 3 haut
            (290, 676, 40, 140),  # Salle 3 bas
            (530, 0, 40, 140),  # Salle 4 bas
            (530, 340, 300, 40),  # Salle 5 haut
            (530, 340, 40, 140),  # Salle 5 bas
            (530, 676, 300, 40),  # Salle 6 haut
            (530, 676, 40, 140),  # Salle 6 bas
            (0, 1008, 330, 60),  # Salle 3 inf
            (530, 1008, 370, 40),  # Salle 6 inf
            (820, 0, 330, 1048),  # Grand mur
            (1350, 0, 40, 140),  # Salle 7 bas
            (1350, 340, 300, 40),  # Salle 8 haut
            (1350, 340, 40, 140),  # Salle 8 bas
            (1350, 676, 300, 40),  # Salle 9 haut
            (1350, 676, 40, 140),  # Salle 9 bas
            (1350, 1012, 300, 40),  # Salle 10 haut
            (1350, 1012, 40, 140),  # Salle 10 bas
        ]
        etage_epsic_doors = [
            (600, 1300, 50, 25, 'EPSIC (entrée)', 250, 352, (0, 0, 50, 25))
                             ]

        etage_epsic_interactive_objects = [
            (721, 1248, 28, 37, "Mieux vaut ne pas monter au neuvième aujourd'hui.", 'images_videos/escaliers2.png', False),
            (675, 1050, 35, 71, "Bonjour !! Je vais soigner votre équipe, ça ne prendra qu'un instant !", 'images_videos/doctorf.png', True),
            (60, 600, 38, 61, "C'est long...", 'images_videos/roxanne.png', False),
            (150, 600, 32, 59, "Ce cours est très intéressant", 'images_videos/wally.png', False),
            (230, 600, 46, 63, "Je me suis trompée de classe mais je n'ose pas le dire, donc je vais attendre...", 'images_videos/beauty.png', False),
            (50, 500, 38, 58, "Il est lent ce lait... enfin ce cours, mais t'as la ref.", 'images_videos/lass.png', False),
            (150, 500, 44, 62, "Laisse moi tranquille je joue à Tetris !", 'images_videos/pokemonrangerm.png', False),
            (240, 500, 43, 61, "À la pause je fonce au neuvième", 'images_videos/Ebrendan.png', False),
            (200, 400, 43, 67, "Et c'est comme ça qu'on fait une roulette russe qui delete System32 si vous perdez.", 'images_videos/steven.png', False),
            (1400, 500, 42, 68, "Attends mais j'étais chez moi y'a 3 secondes c'est quoi ce bazar ?", 'images_videos/norman.png', False),
            (1490, 500, 41, 61, "Zzzzzz...", 'images_videos/Emay.png', False)

        ]

        self.maps['Rafisa (extérieur)'] = Map('Rafisa (extérieur)', 'images_videos/Map001.png', 400, 300, outside_walls, outside_doors, [])
        self.maps['Rafisa (intérieur)'] = Map('Rafisa (intérieur)', 'images_videos/Map002.png', 400, 300, inside_walls, inside_doors, interactive_objects)
        self.maps['EPSIC (entrée)'] = Map('EPSIC (entrée)', 'images_videos/Map003.png', 400, 300, epsic_walls, epsic_doors, new_interactive_objects)
        self.maps['EPSIC (étage 7)'] = Map('EPSIC (étage 7)', 'images_videos/Map004.png', 400, 300, etage_epsic_walls, etage_epsic_doors, etage_epsic_interactive_objects)

        # Ajoute une image sur les cartes
        logo_rafisa = pygame.image.load('images_videos/rafisa_logo.png').convert_alpha()
        logo = pygame.sprite.Sprite()
        logo.image = logo_rafisa
        logo.rect = logo.image.get_rect()
        self.maps['Rafisa (extérieur)'].add_object(logo, 300, 100)  # Position de l'image

        escaliers = pygame.image.load('images_videos/escaliers.png').convert_alpha()
        logo = pygame.sprite.Sprite()
        logo.image = escaliers
        logo.rect = logo.image.get_rect()
        self.maps['EPSIC (entrée)'].add_object(logo, 192, 382)

        escaliers2 = pygame.image.load('images_videos/escaliers2.png').convert_alpha()
        logo = pygame.sprite.Sprite()
        logo.image = escaliers2
        logo.rect = logo.image.get_rect()
        self.maps['EPSIC (étage 7)'].add_object(logo, 577, 1248)

        # Initialise les dresseurs
        self.init_trainers()

        # Ajoute un canapé et une dalle aux obstacles sur la carte 'Rafisa (intérieur)'
        self.canape = Canape(480, 270)
        self.dalle = Dalle(660, 190)
        self.maps['Rafisa (intérieur)'].add_object(self.canape, 480, 270)
        self.maps['Rafisa (intérieur)'].add_object(self.dalle, 660, 190)
        self.obstacles.add(self.canape, self.dalle)

        # Ajoute les obstacles aux murs de la carte 'Rafisa (intérieur)'
        self.maps['Rafisa (intérieur)'].walls.add(self.canape, self.dalle)

    def init_interactive_bus(self):
        self.bus_object = InteractiveBus(528, 698, self)  # Bus à Rafisa (extérieur)
        self.maps['Rafisa (extérieur)'].add_object(self.bus_object, 528, 698)
        self.maps['Rafisa (extérieur)'].interactive_objects.add(self.bus_object)  # Ajoute le bus aux objets interactifs

        self.bus_object = InteractiveBus(384, 1083, self)  # Bus à EPSIC (entrée)
        self.maps['EPSIC (entrée)'].add_object(self.bus_object, 384, 1083)
        self.maps['EPSIC (entrée)'].interactive_objects.add(self.bus_object)

    # Position des dresseurs
    def init_trainers(self):
        trainer_positions = [
            (570, 290, Trainer1, 'Rafisa (extérieur)'), (50, 660, Trainer2, 'Rafisa (intérieur)'),
            (50, 410, Trainer3, 'Rafisa (intérieur)'), (530, 500, Trainer4, 'Rafisa (extérieur)'),
            (180, 150, Trainer5, 'Rafisa (intérieur)'), (700, 710, Trainer6, 'Rafisa (extérieur)'),
            (320, 500, Trainer7, 'Rafisa (intérieur)'), (150, 480, Trainer8, 'Rafisa (extérieur)'),
            (500, 350, Trainer9, 'Rafisa (intérieur)'), (740, 320, Trainer10, 'Rafisa (intérieur)'),
            (675, 120, Trainer11, 'Rafisa (intérieur)'), (500, 550, Trainer12, 'Rafisa (intérieur)'),
            (550, 640, Trainer13, 'Rafisa (intérieur)'), (100, 80, Eleve1, 'EPSIC (entrée)'),
            (680, 600, Eleve2, 'EPSIC (étage 7)'), (770, 250, Eleve3, 'EPSIC (étage 7)'),
            (1250, 500, Eleve4, 'EPSIC (entrée)'), (570, 500, Eleve5, 'EPSIC (étage 7)'),
            (1250, 80, Eleve6, 'EPSIC (étage 7)'), (570, 270, Eleve7, 'EPSIC (étage 7)'),
            (60, 900, Eleve8, 'EPSIC (étage 7)'), (1074, 100, Eleve9, 'EPSIC (entrée)'),
            (674, 885, Eleve10, 'EPSIC (étage 7)'), (192, 382, Prof1, 'EPSIC (entrée)'),
            (-50, -50, Prof2, 'EPSIC (étage 7)'), (820, 900, Prof3, 'EPSIC (entrée)'),
            (570, 80, Prof4, 'EPSIC (étage 7)'), (200, 750, Prof5, 'EPSIC (étage 7)'),
            (1200, 1200, Prof6, 'EPSIC (étage 7)'), (1350, 530, Prof7, 'EPSIC (étage 7)'),
            (100, 1150, Doyen, 'EPSIC (étage 7)')
        ]
        for x, y, TrainerClass, map_name in trainer_positions:
            if TrainerClass == Doyen:
                self.doyen = TrainerClass(x, y, map_name, self)  # Passer l'instance du jeu et stocker le Doyen
                self.trainers.add(self.doyen)
            else:
                trainer = TrainerClass(x, y, map_name)
                self.trainers.add(trainer)

    def change_map(self, map_name, destination=None):
        self.current_map = self.maps[map_name]

        # Filtre les dresseurs pour ne garder que ceux de la carte où le joueur est présent
        self.map_trainers = [trainer for trainer in self.trainers if trainer.map_name == map_name]
        self.all_sprites.empty()
        self.all_sprites.add(*self.current_map.objects)  # Ajoute les objets de la carte utilisée
        self.all_sprites.add(*self.map_trainers)
        self.all_sprites.add(
            *self.current_map.interactive_objects)  # Ajoute les objets interactifs de la carte utilisée
        self.all_sprites.add(self.player)

        # Ajoute les obstacles si la condition n'est pas remplie et que la carte est 'Rafisa (intérieur)'
        if map_name == 'Rafisa (intérieur)' and not self.all_trainers_defeated():
            self.all_sprites.add(self.obstacles)
            self.current_map.walls.add(self.obstacles)

        # Positionne le joueur aux coordonnées de destination si spécifiées
        if destination:
            self.player.rect.topleft = destination

    # Check toutes les interactions
    def are_all_pre_doyen_trainers_defeated(self):
        required_trainers = [Prof1, Prof3, Prof4, Prof5, Prof6, Prof7, Eleve1, Eleve2, Eleve3, Eleve4, Eleve5, Eleve6, Eleve7, Eleve8, Eleve9, Eleve10]
        return all(self.trainers_defeated[trainer] for trainer in required_trainers)

    def check_interaction(self):
        for trainer in self.map_trainers:
            if self.player.rect.colliderect(trainer.rect):
                if not trainer.is_defeated():
                    if isinstance(trainer, Doyen):
                        if not self.are_all_pre_doyen_trainers_defeated():
                            self.dialogue_box.set_dialogue(
                                "Bonjour, non je n'ai pas le temps pour un combat désolé !",
                                trainer.name
                            )
                        else:
                            self.dialogue_box.set_dialogue(trainer.talk(post_defeat=self.trainers_defeated[Prof2]),
                                                           trainer.name)
                        self.in_dialogue = True
                        self.current_trainer = trainer
                        return
                    else:
                        self.dialogue_box.set_dialogue(trainer.talk(), trainer.name)
                        self.in_dialogue = True
                        self.current_trainer = trainer
                        return

        for door in self.current_map.doors:
            if self.player.rect.colliderect(door.hitbox):
                self.change_map(door.target_map, (door.target_x, door.target_y))
                return

    # Interactions avec dresseurs
    def interact_with_trainers(self):
        for trainer in self.map_trainers:
            if self.player.rect.colliderect(trainer.rect) and trainer.is_defeated():
                self.dialogue_box.set_dialogue(trainer.talk(post_defeat=self.trainers_defeated[Trainer11]), trainer.name)
                self.in_dialogue = True
                self.current_trainer = trainer
                return

    # Interactions avec objets
    def interact_with_objects(self):
        for obj in self.current_map.interactive_objects:
            if self.player.rect.colliderect(obj.rect):
                # Passer self (Game) pour SecretDoor ou InteractiveBus, sinon self.player (Player)
                if isinstance(obj, (SecretDoor, InteractiveBus)):
                    message = obj.interact(self)
                else:
                    message = obj.interact(self.player)

                if message:
                    self.dialogue_box.set_dialogue(message, "???")
                self.in_dialogue = True
                return

    def get_camera_pos(self, player_pos):
        map_width, map_height = self.current_map.rect.size
        x = max(0, min(player_pos[0] - self.WIN_WIDTH // 2, map_width - self.WIN_WIDTH))
        y = max(0, min(player_pos[1] - self.WIN_HEIGHT // 2, map_height - self.WIN_HEIGHT))
        return x, y

    def update(self):
        keys = pygame.key.get_pressed()

        if not self.in_dialogue and not self.in_combat:
            self.player.update(keys, self.map_trainers, self.current_map.walls)
            self.check_interaction()

            # Vérifie la collision avec la porte secrète (SecretDoor)
            self.check_secret_door_collision()

            if keys[pygame.K_e]:  # Appuyer sur la touche 'E' pour interagir
                self.interact_with_objects()
                self.interact_with_trainers()
        elif self.in_dialogue and not self.in_combat:
            if keys[pygame.K_RETURN]:  # Appuyer sur Entrée pour fermer le dialogue
                self.in_dialogue = False
                if self.current_trainer and not self.current_trainer.is_defeated():
                    self.start_combat()

        # Mettre à jour la position de la caméra après avoir mis à jour le joueur
        self.camera_pos = self.get_camera_pos(self.player.rect.topleft)

    def check_secret_door_collision(self):
        # Vérifie la collision avec chaque objet interactif pour détecter la SecretDoor
        for obj in self.current_map.interactive_objects:
            if isinstance(obj, SecretDoor) and self.player.rect.colliderect(obj.rect):
                obj.interact(self)
                return

    def draw(self):
        self.current_map.draw(self.screen, self.camera_pos)
        for sprite in self.all_sprites:
            # Ajuster la position des sprites par rapport à la caméra
            screen_pos = (sprite.rect.topleft[0] - self.camera_pos[0], sprite.rect.topleft[1] - self.camera_pos[1])
            self.screen.blit(sprite.image, screen_pos)
        if self.in_dialogue:
            self.dialogue_box.draw()

        # Affiche le compteur de dresseurs vaincus
        counter_text = f"Dresseurs vaincus: {self.battled_trainers}"
        counter_surface = self.font.render(counter_text, True, (0, 0, 0))
        self.screen.blit(counter_surface, (10, 10))

        # Affiche le menu de sélection de carte
        self.map_selector.draw_menu()

    def start_combat(self):
        if self.current_trainer and not self.current_trainer.is_defeated():
            if isinstance(self.current_trainer, Doyen) and not self.are_all_pre_doyen_trainers_defeated():
                self.dialogue_box.set_dialogue(
                    "Revenez après avoir battu tout le monde ici je devrais pouvoir vous accorder un peu de mon temps.",
                    self.current_trainer.name
                )
                self.in_dialogue = True
                return

            combat = Combat(self.screen, self.player.team, self.current_trainer.pokemon_team,
                            self.get_background_image())
            result = combat.run()
            self.in_combat = False
            self.in_dialogue = False
            self.current_trainer.set_defeated()
            self.battled_trainers += 1
            self.trainers_defeated[type(self.current_trainer)] = True

            if isinstance(self.current_trainer, Trainer11):
                self.update_trainers_positions_and_dialogues()  # Mise à jour des positions après la défaite de Trainer11

            if isinstance(self.current_trainer, Prof2):
                self.add_secret_door()  # Ajouter la porte secrète après la défaite de Prof2
                self.load_post_defeat_dialogue(self.doyen)  # Activer le dialogue post-défaite du Doyen

            if isinstance(self.current_trainer, Doyen):
                self.update_doyen_related_trainers_positions_and_dialogues()
                self.trainers_defeated[Doyen] = True
                for trainer in self.trainers:
                    self.load_post_defeat_dialogue(
                        trainer)  # Activer le dialogue post-défaite pour les autres dresseurs

            self.current_trainer = None

            if not any(pokemon.current_hp > 0 for pokemon in self.player.team):
                self.reset_game()
            elif self.all_trainers_defeated():
                self.canape.make_transparent()
                self.dalle.make_transparent()
                self.current_map.walls.remove(self.canape, self.dalle)

    def load_post_defeat_dialogue(self, trainer):
        # Charger le dialogue post-défaite pour le dresseur
        if isinstance(trainer, (Prof1, Prof3, Prof4, Prof5, Prof6, Prof7, Eleve1, Eleve2, Eleve3, Eleve4, Eleve5,
                                Eleve6, Eleve7, Eleve8, Eleve9, Eleve10, Doyen)):
            trainer.post_defeat_condition_met = True

    def add_secret_door(self):
        # Ajouter une porte secrète à EPSIC (entrée)
        secret_door = SecretDoor(553, 432, 'images_videos/secret_door.png')
        self.maps['EPSIC (entrée)'].add_object(secret_door, 553, 432)
        self.maps['EPSIC (entrée)'].interactive_objects.add(secret_door)

    def get_background_image(self):
        if self.current_map.name == 'Rafisa (extérieur)':
            return 'images_videos/combat_outside1.jpg'
        elif self.current_map.name == 'Rafisa (intérieur)':
            return 'images_videos/combat_inside.jfif'
        elif self.current_map.name == 'EPSIC (entrée)':
            return 'images_videos/combat_epsic1.png'
        elif self.current_map.name == 'EPSIC (étage 7)':
            return 'images_videos/combat_epsic2.jpg'

    def reset_game(self):
        player_team = ["Vaultra", "Alderiate", "Feudkan", "Lorneax"]  # Noms des Pokémon de l'équipe du joueur (ajouter noms pour ajouter a l'équipe)
        self.player = Player(self.current_map.player_start_x, self.current_map.player_start_y, player_team)
        self.battled_trainers = 0  # Reset the number of defeated trainers
        self.all_sprites.empty()
        self.trainers.empty()
        self.obstacles.empty()
        self.all_sprites.add(self.player)
        self.init_maps()
        self.change_map('Rafisa (extérieur)')

    def update_trainers_positions_and_dialogues(self):
        # Nouvelles positions des dresseurs après la défaite de Trainer11
        new_positions = {
            Trainer1: (570, 290),
            Trainer2: (672, 280),
            Trainer3: (672, 428),
            Trainer4: (530, 500),
            Trainer5: (500, 350),
            Trainer6: (700, 710),
            Trainer7: (160, 175),
            Trainer8: (330, 300),
            Trainer9: (500, 50),
            Trainer10: (147, 383),
            Trainer12: (672, 580),
            Trainer13: (550, 478)
        }
        for trainer in self.trainers:
            trainer_class = type(trainer)
            if trainer_class in new_positions:
                trainer.rect.topleft = new_positions[trainer_class]

    def update_doyen_related_trainers_positions_and_dialogues(self):
        # Nouvelles positions des professeurs et élèves après la défaite du Doyen
        new_positions = {
            Prof1: (-50, -50),
            Prof2: (500, 1130),  # Nouvelle position du Prof2 après la défaite du Doyen
            Prof3: (820, 900),
            Prof4: (570, 80),
            Prof5: (200, 750),
            Prof6: (1500, 1080),
            Prof7: (1450, 430),
            Eleve1: (100, 80),
            Eleve2: (680, 600),
            Eleve3: (770, 250),
            Eleve4: (1250, 500),
            Eleve5: (570, 500),
            Eleve6: (1480, 1180),
            Eleve7: (570, 270),
            Eleve8: (60, 900),
            Eleve9: (1074, 100),
            Eleve10: (674, 885)
        }
        for trainer in self.trainers:
            trainer_class = type(trainer)
            if trainer_class in new_positions:
                trainer.rect.topleft = new_positions[trainer_class]

    def all_trainers_defeated(self):
        trainers_to_defeat = [Trainer1, Trainer2, Trainer3, Trainer4, Trainer5, Trainer6,
                              Trainer7, Trainer8, Trainer9, Trainer10, Trainer12, Trainer13]
        defeated_count = sum(
            1 for trainer in self.trainers if type(trainer) in trainers_to_defeat and trainer.is_defeated())
        return defeated_count == len(trainers_to_defeat)
