import pygame
from player import Player
from trainer import (Trainer1, Trainer2, Trainer3, Trainer4, Trainer5, Trainer6,
                     Trainer7, Trainer8, Trainer9, Trainer10, Trainer11, Trainer12,
                     Trainer13)
from dialogue import DialogueBox
from combat import Combat
from map import Map, MapSelector

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
        self.image.set_alpha(0)  # Rendre l'image complètement transparente
        self.kill()  # Supprimer l'obstacle du groupe de sprites

class Canape(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 50, 'images_videos/canapé.png')

class Dalle(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, 'images_videos/sol.png')

class InteractiveBus(pygame.sprite.Sprite):
    def __init__(self, x, y, map_selector, destinations):
        super().__init__()
        self.image = pygame.image.load('images_videos/bus.png').convert_alpha()  # Remplacez par le chemin de l'image de votre bus
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.map_selector = map_selector
        self.destinations = destinations

    def interact(self, game_instance):
        game_instance.bus.travel_to_map(game_instance, self.destinations)
        return "Vous prenez le bus pour voyager vers une autre carte."


class Bus:
    def __init__(self, map_selector):
        self.map_selector = map_selector

    def travel_to_map(self, game_instance, destinations):
        self.map_selector.toggle_menu()  # Activer le menu de sélection de carte
        while self.map_selector.menu_active:
            for event in pygame.event.get():
                selected_map = self.map_selector.handle_event(event)
                if selected_map:
                    game_instance.change_map(selected_map, destinations[selected_map])
                    self.map_selector.toggle_menu()
                    break
            game_instance.draw()
            pygame.display.flip()


class Game:
    def __init__(self, screen):
        self.screen = screen
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

        # Initialiser les cartes
        self.init_maps()

        # Initialiser le sélecteur de cartes
        self.map_selector = MapSelector(screen, list(self.maps.keys()))

        # Initialiser l'objet bus
        self.bus = Bus(self.map_selector)  # Ajout de cette ligne

        # Initialiser l'objet bus interactif
        self.init_interactive_bus()

        # Initialiser le joueur après avoir défini la carte initiale
        player_team = ["Vaultra", "Spectradoc"]  # Noms des Pokémon de l'équipe du joueur
        self.player = Player(400, 300, player_team)  # Position initiale arbitraire
        self.all_sprites.add(self.player)

        # Changer la carte initiale
        self.change_map('Rafisa (extérieur)')

        # Police pour le compteur de dresseurs
        self.font = pygame.font.Font(None, 36)

    def init_maps(self):
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
            (0, 0, 800, 40),  # Mur supérieur ok
            (-510, 771, 800, 60),  # Mur inférieur gauche
            (380, 771, 800, 60),  # Mur inférieur droit
            (5, 0, 40, 802),  # Mur gauche ok
            (770, 0, 10, 802),  # Mur droit ok
            (245, 481, 40, 802),  # Séparation coin miam - open space (droite) ok
            (140, 522, 145, 40),  # Séparation cuisine - salle à manger (milieu)
            (-10, 290, 300, 40),  # Séparation salle à manger - open space (haut) ok
            (580, 240, 400, 40),  # Mur inférieur bureau Tania ok
            (444, -522, 35, 802),  # Mur côté bureau Tania ok
            (390, 441, 40, 259),  # Caisses
        ]
        inside_doors = [
            (290, 770, 90, 100, 'Rafisa (extérieur)', 382, 300, (0, 25, 90, 25))  # Porte vers l'extérieur
        ]

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

        self.maps['Rafisa (extérieur)'] = Map('Rafisa (extérieur)', 'images_videos/Map001.png', 400, 300, outside_walls, outside_doors, [])
        self.maps['Rafisa (intérieur)'] = Map('Rafisa (intérieur)', 'images_videos/Map002.png', 400, 300, inside_walls, inside_doors,
                                  interactive_objects)

        # Ajout de la nouvelle carte
        new_map_walls = [
            (0, 0, 800, 40),  # Exemple de mur supérieur
            (0, 760, 800, 40),  # Exemple de mur inférieur
            (0, 0, 40, 800),  # Exemple de mur gauche
            (760, 0, 40, 800)  # Exemple de mur droit
        ]
        new_map_doors = []  # Ajouter les portes si nécessaire
        new_interactive_objects = []  # Ajouter les objets interactifs si nécessaire
        self.maps['ne cliquez pas (vraiment)'] = Map('coming_soon', 'images_videos/comingsoon.png', 400, 300, new_map_walls, new_map_doors, new_interactive_objects)

        # Ajouter une image sur la carte 'Rafisa (extérieur)'
        logo_rafisa = pygame.image.load('images_videos/rafisa_logo.png').convert_alpha()
        logo = pygame.sprite.Sprite()
        logo.image = logo_rafisa
        logo.rect = logo.image.get_rect()
        self.maps['Rafisa (extérieur)'].add_object(logo, 300, 100)  # Position de l'image sur la carte

        # Initialiser les dresseurs
        self.init_trainers()

        # Ajouter canapé et dalle aux obstacles seulement sur la carte 'Rafisa (intérieur)'
        self.canape = Canape(480, 270)
        self.dalle = Dalle(660, 190)
        self.maps['Rafisa (intérieur)'].add_object(self.canape, 480, 270)
        self.maps['Rafisa (intérieur)'].add_object(self.dalle, 660, 190)
        self.obstacles.add(self.canape, self.dalle)

        # Ajouter les obstacles aux murs de la carte 'Rafisa (intérieur)'
        self.maps['Rafisa (intérieur)'].walls.add(self.canape, self.dalle)

    def init_interactive_bus(self):
        destinations = {
            'Rafisa (extérieur)': (400, 300),  # Coordonnées de destination sur la carte 'Rafisa (extérieur)'
            'Rafisa (intérieur)': (310, 645),   # Coordonnées de destination sur la carte 'Rafisa (intérieur)'
            'ne cliquez pas (vraiment)': (500, 500)   # Coordonnées de destination sur la nouvelle carte
        }
        self.bus_object = InteractiveBus(528, 698, self.map_selector, destinations)  # Position de l'objet bus sur la carte
        self.maps['Rafisa (extérieur)'].add_object(self.bus_object, 528, 698)
        self.maps['Rafisa (extérieur)'].interactive_objects.add(self.bus_object)  # Ajouter aux objets interactifs

    def init_trainers(self):
        trainer_positions = [
            (570, 290, Trainer1, 'Rafisa (extérieur)'), (50, 660, Trainer2, 'Rafisa (intérieur)'), (50, 410, Trainer3, 'Rafisa (intérieur)'),
            (530, 500, Trainer4, 'Rafisa (extérieur)'), (180, 150, Trainer5, 'Rafisa (intérieur)'), (700, 710, Trainer6, 'Rafisa (extérieur)'),
            (320, 500, Trainer7, 'Rafisa (intérieur)'), (150, 480, Trainer8, 'Rafisa (extérieur)'), (500, 350, Trainer9, 'Rafisa (intérieur)'),
            (740, 320, Trainer10, 'Rafisa (intérieur)'), (675, 120, Trainer11, 'Rafisa (intérieur)'), (500, 550, Trainer12, 'Rafisa (intérieur)'),
            (550, 640, Trainer13, 'Rafisa (intérieur)')
        ]
        for x, y, TrainerClass, map_name in trainer_positions:
            trainer = TrainerClass(x, y, map_name)
            self.trainers.add(trainer)

    def change_map(self, map_name, destination=None):
        self.current_map = self.maps[map_name]

        # Filtrer les dresseurs pour ne garder que ceux de la carte actuelle
        self.map_trainers = [trainer for trainer in self.trainers if trainer.map_name == map_name]
        self.all_sprites.empty()
        self.all_sprites.add(*self.current_map.objects)  # Ajouter les objets de la carte actuelle
        self.all_sprites.add(*self.map_trainers)
        self.all_sprites.add(
            *self.current_map.interactive_objects)  # Ajouter les objets interactifs de la carte actuelle
        self.all_sprites.add(self.player)

        # Ajouter les obstacles si la condition n'est pas remplie et que la carte est 'Rafisa (intérieur)'
        if map_name == 'Rafisa (intérieur)' and not self.all_trainers_defeated():
            self.all_sprites.add(self.obstacles)
            self.current_map.walls.add(self.obstacles)

        # Positionner le joueur aux coordonnées de destination si spécifiées
        if destination:
            self.player.rect.topleft = destination

    def check_interaction(self):
        for trainer in self.map_trainers:
            if self.player.rect.colliderect(trainer.rect) and not trainer.is_defeated():
                self.dialogue_box.set_dialogue(trainer.talk(), trainer.name)
                self.in_dialogue = True
                self.current_trainer = trainer
                return

        for door in self.current_map.doors:
            if self.player.rect.colliderect(door.hitbox):
                self.change_map(door.target_map, (door.target_x, door.target_y))
                return

    def interact_with_trainers(self):
        for trainer in self.map_trainers:
            if self.player.rect.colliderect(trainer.rect) and trainer.is_defeated():
                self.dialogue_box.set_dialogue(trainer.talk(), trainer.name)
                self.in_dialogue = True
                return

    def interact_with_objects(self):
        for obj in self.current_map.interactive_objects:
            if self.player.rect.colliderect(obj.rect):
                message = obj.interact(self)
                self.dialogue_box.set_dialogue(message, "Info")
                self.in_dialogue = True
                return

    def update(self):
        keys = pygame.key.get_pressed()

        if not self.in_dialogue and not self.in_combat:
            self.player.update(keys, self.map_trainers, self.current_map.walls)
            self.check_interaction()
            if keys[pygame.K_e]:  # Appuyer sur la touche 'E' pour interagir
                self.interact_with_objects()
                self.interact_with_trainers()

        elif self.in_dialogue and not self.in_combat:
            if keys[pygame.K_RETURN]:  # Appuyer sur Entrée pour fermer le dialogue
                self.in_dialogue = False
                if self.current_trainer and not self.current_trainer.is_defeated():
                    self.start_combat()

    def draw(self):
        self.current_map.draw(self.screen)
        self.all_sprites.draw(self.screen)  # Dessiner tous les sprites, le joueur inclus
        if self.in_dialogue:
            self.dialogue_box.draw()

        # Afficher le compteur de dresseurs vaincus
        counter_text = f"Dresseurs vaincus: {self.battled_trainers}"
        counter_surface = self.font.render(counter_text, True, (0, 0, 0))
        self.screen.blit(counter_surface, (10, 10))

        # Afficher le menu de sélection de carte
        self.map_selector.draw_menu()

    def start_combat(self):
        if self.current_trainer and not self.current_trainer.is_defeated():
            combat = Combat(self.screen, self.player.team, self.current_trainer.pokemon_team,
                            self.get_background_image())
            result = combat.run()
            self.in_combat = False
            self.in_dialogue = False
            self.current_trainer.set_defeated()
            self.battled_trainers += 1
            self.current_trainer = None
            if not any(pokemon.current_hp > 0 for pokemon in self.player.team):
                self.reset_game()
            elif self.all_trainers_defeated():
                self.canape.make_transparent()  # Rendre le canapé transparent et supprimer collisions
                self.dalle.make_transparent()  # Rendre la dalle transparente et supprimer collisions
                self.current_map.walls.remove(self.canape, self.dalle)  # Supprimer des murs

    def get_background_image(self):
        if self.current_map.name == 'Rafisa (extérieur)':
            return 'images_videos/combat_outside1.jpg'
        elif self.current_map.name == 'Rafisa (intérieur)':
            return 'images_videos/combat_inside.jfif'

    def reset_game(self):
        player_team = ["Vaultra", "Spectradoc"]  # Noms des Pokémon de l'équipe du joueur
        self.player = Player(self.current_map.player_start_x, self.current_map.player_start_y, player_team)
        self.battled_trainers = 0  # Reset the number of defeated trainers
        self.all_sprites.empty()
        self.trainers.empty()
        self.obstacles.empty()
        self.all_sprites.add(self.player)
        self.init_maps()
        self.change_map('Rafisa (extérieur)')

    def all_trainers_defeated(self):
        trainers_to_defeat = [Trainer1, Trainer2, Trainer3, Trainer4, Trainer5, Trainer6,
                              Trainer7, Trainer8, Trainer9, Trainer10, Trainer12, Trainer13]
        defeated_count = sum(
            1 for trainer in self.trainers if type(trainer) in trainers_to_defeat and trainer.is_defeated())
        return defeated_count == len(trainers_to_defeat)
