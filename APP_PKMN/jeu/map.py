import pygame
from wall import Wall
from door import Door
from interactive_object import InteractiveObject


class MapSelector:
    def __init__(self, screen, available_maps):
        self.screen = screen
        self.available_maps = available_maps
        self.font = pygame.font.Font(None, 36)
        self.menu_active = False

    def toggle_menu(self):
        self.menu_active = not self.menu_active

    def draw_menu(self):
        if not self.menu_active:
            return

        # Dessiner un fond pour le menu
        menu_background = pygame.Surface((400, 300))
        menu_background.fill((255, 255, 255))
        self.screen.blit(menu_background, (200, 150))

        # Afficher les options de cartes
        for i, map_name in enumerate(self.available_maps):
            map_text = self.font.render(f"{i + 1}. {map_name}", True, (0, 0, 0))
            self.screen.blit(map_text, (220, 180 + i * 40))

    def handle_event(self, event):
        if not self.menu_active:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and len(self.available_maps) >= 1:
                return self.available_maps[0]
            elif event.key == pygame.K_2 and len(self.available_maps) >= 2:
                return self.available_maps[1]
            elif event.key == pygame.K_3 and len(self.available_maps) >= 3:
                return self.available_maps[2]
            # Ajouter d'autres touches si nécessaire
        return None


class Map:
    def __init__(self, name, background_image, player_start_x, player_start_y, walls, doors, interactive_objects,
                 wall_alpha=255):
        self.name = name
        self.background = pygame.image.load(background_image).convert()
        self.player_start_x = player_start_x
        self.player_start_y = player_start_y
        self.walls = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.interactive_objects = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()

        for wall in walls:
            x, y, width, height = wall
            self.walls.add(Wall(x, y, width, height, alpha=wall_alpha))

        for door in doors:
            x, y, width, height, target_map, target_x, target_y, hitbox = door
            self.doors.add(Door(x, y, width, height, target_map, target_x, target_y, hitbox))

        for obj in interactive_objects:
            x, y, width, height, message, image_path, heal = obj
            self.interactive_objects.add(InteractiveObject(x, y, width, height, message, image_path, heal))

    def add_object(self, obj, x, y):
        obj.rect.topleft = (x, y)
        self.objects.add(obj)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.walls.draw(screen)
        self.doors.draw(screen)
        self.interactive_objects.draw(screen)
        self.objects.draw(screen)
